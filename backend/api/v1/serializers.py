import pickle
from django.db import models
from django.db.transaction import atomic
from django.forms import model_to_dict
from extract.process_df import preprocess_entity
from search import ya_search, find_youtube_video
from analyst.settings import BASE_DIR, YANDEX_SEARCH_API_TOKEN
from rest_framework import serializers

from accounts.models import (
    WebPage, Data, MetaBlock, Report,
    ReportBlock, SearchQuery, Template, Theme
)
from accounts.tasks import add_data_to_report_block, add_video_data_to_report_block, add_search_data_to_report_block
from extract.reports import get_one_figure_by_entity


search_engine = None
try:
    search_engine = pickle.load(open(f'{BASE_DIR}/search.pkl', 'rb'))
except FileNotFoundError:
    print('No search.pkl file found')


class DataSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    snippet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Data
        fields = (
            'id',
            'name',
            'type',
            'url',
            'snippet'
        )

    def get_snippet(self, obj):
        return 'Пример сниппета'

    def get_name(self, obj):
        return obj.name

    def get_url(self, obj):
        return obj.url


class MetaBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaBlock
        fields = ('id', 'query_template', 'position', 'type')


class TemplateSerializer(serializers.ModelSerializer):
    meta_blocks = MetaBlockSerializer(many=True)

    class Meta:
        model = Template
        fields = ('id', 'name', 'meta_blocks')


class CreateTemplateSerializer(serializers.ModelSerializer):
    meta_blocks = MetaBlockSerializer(many=True)

    class Meta:
        model = Template
        fields = ('theme', 'name', 'meta_blocks')

    @atomic
    def create(self, validated_data):
        name = validated_data.get('name')
        theme = validated_data.get('theme')
        meta_blocks = validated_data.get('meta_blocks')

        template = Template.objects.create(name=name, theme=theme)

        meta_blocks = [
            MetaBlock(
                query_template=block.get('query_template'),
                position=block.get('position'),
                type=block.get('type', MetaBlock.PLOTLY),
                template=template
            )
            for block in meta_blocks
        ]

        MetaBlock.objects.bulk_create(objs=meta_blocks)

        return template


class ThemeSerializer(serializers.ModelSerializer):
    templates = TemplateSerializer(many=True)

    class Meta:
        model = Theme
        fields = ('id', 'name', 'templates')


class CreateReportSerializer(serializers.ModelSerializer):
    template = serializers.IntegerField()
    search_query = serializers.CharField()

    class Meta:
        model = Report
        fields = (
            'template',
            'search_query'
        )

    def get_data_from_search_engine(self, search_query_text):
        if search_engine:
            result = search_engine.search(
                search_query_text
            )
            index_ids = list(map(lambda x: x[0], result))
            data = Data.objects.filter(
                id__in=index_ids
            ).all()
            if data.count() > 0:
                data = data[0]
            else:
                data = None
            return data

    def represent_data_obj(self, data_obj, block_type):
        if data_obj:
            if block_type == MetaBlock.TEXT or block_type == MetaBlock.VIDEO:
                return {'text': data_obj.data}
            entity = model_to_dict(data_obj)
            entity['frame'] = entity['data']
            entity['meta'] = entity['meta_data'].get('title', '')
            entity = preprocess_entity(entity)
            representation = get_one_figure_by_entity(
                entity=entity,
                return_plotly_format=True if block_type == MetaBlock.PLOTLY else False
            )
            return representation.to_dict()
        return {}

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        template = Template.objects.get(id=validated_data.get('template'))
        raw_search_query: str = validated_data.get('search_query')

        search_query, _ = SearchQuery.objects.get_or_create(
            user=user,
            text=raw_search_query
        )

        report = Report.objects.create(
            user=user,
            search_query=search_query,
            template=template
        )

        for meta_block in template.meta_blocks.all():
            urls_to_parse: list[str] = []
            video_to_summarize: str = []

            search_query_text = f'{meta_block.query_template} {search_query}'
            data_obj: Data | None = None
            if meta_block.type == MetaBlock.PLOTLY:
                data_obj = self.get_data_from_search_engine(search_query_text)
                representation = self.represent_data_obj(
                    data_obj, meta_block.type)

            elif meta_block.type == MetaBlock.TEXT:
                search = ya_search(
                    search_query,
                    YANDEX_SEARCH_API_TOKEN
                )

                urls = [r.get('url') for r in search]
                parsed_pages = WebPage.objects.filter(url__in=urls).all()
                parsed_urls = [page.url for page in parsed_pages]
                indexed_data = Data.objects.filter(
                    type=Data.TEXT, page__in=parsed_pages).all()
                if indexed_data:
                    representation = self.represent_data_obj(
                        indexed_data[0], MetaBlock.TEXT)
                else:
                    urls_to_parse += list(set(urls).difference(set(parsed_urls)))
                    representation = {}
            elif meta_block.type == MetaBlock.VIDEO:
                video = find_youtube_video(f'{search_query_text} аналитика')
                # print(video)
                url = video['url']
                video_page = WebPage.objects.filter(url=url).first()
                all_yt = WebPage.objects.filter(url__startswith='https://youtube.com/').all()
                print(url, video_page, len(all_yt), all_yt[0].url)
                if video_page:
                    data_obj = Data.objects.filter(page=video_page).first()
                    print(f'В базе найдено видео: {data_obj}')
                    if not data_obj:
                        data_obj = None
                    # if len(data_obj) == 0:
                        # data_obj = None
                    representation = self.represent_data_obj(data_obj, MetaBlock.VIDEO)
                else:
                    video_to_summarize = url
                    representation = {}
            else:
                raise ValueError(
                    f'No type meta_block type: {meta_block.type}. Only allowed {MetaBlock.TYPES}')

            print(meta_block.type)
            print(representation)
            # if not isinstance(data_obj, Data):
            #     data_obj = None
            block = ReportBlock.objects.create(
                report=report,
                data=data_obj,
                type=meta_block.type,
                representation=representation,
                position=meta_block.position,
                readiness=ReportBlock.READY if data_obj else ReportBlock.NOT_READY
            )

            if representation == {}:
                if video_to_summarize:
                    add_video_data_to_report_block.apply_async(
                        args=(block.id, meta_block.id, video_to_summarize),
                        countdown=15
                    )
                elif urls_to_parse:
                    add_search_data_to_report_block.apply_async(
                        args=(block.id, urls_to_parse),
                        countdown=15
                    )

            if not data_obj:
                add_data_to_report_block.apply_async(
                    args=(block.id, meta_block.id),
                    countdown=15
                )

        return report


class UpdateReportBlockComment(serializers.ModelSerializer):
    class Meta:
        model = ReportBlock
        fields = ('comment',)


class ReportBlockSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = ReportBlock
        fields = (
            'id',
            'source',
            'readiness',
            'type',
            'representation',
            'position',
            'comment',
            'summary',
        )

    def get_source(self, obj):
        return obj.source
    

class ReportBlockSummaryModelSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=(
            ('yandexgpt', 'yandexgpt'),
            ('yandexgpt-lite', 'yandexgpt-lite')
        )
    )

    class Meta:
        model = ReportBlock
        fields = ('type',)


class ReportLightSerializer(serializers.ModelSerializer):
    search_query = serializers.StringRelatedField()
    theme = serializers.SerializerMethodField()
    template = serializers.StringRelatedField()
    readiness = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'date', 'readiness'
        )

    def get_theme(self, obj):
        return str(obj.theme)
    
    def get_readiness(self, obj):
        # В проде надо такое оптимизировать
        return not ReportBlock.objects.filter(readiness=ReportBlock.NOT_READY).exists()


class ReportSerializer(ReportLightSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'blocks', 'date',
            'readiness'
        )

    def get_blocks(self, obj):
        return ReportBlockSerializer(
            obj.blocks.all().annotate(
                source=models.F('data__page__url')
            ),
            many=True
        ).data


class ReportFileFormatSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=(
            ('pdf', 'pdf'),
            ('msword', 'word'),
            ('vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'excel')
        )
    )

    class Meta:
        model = Report
        fields = ('type',)
