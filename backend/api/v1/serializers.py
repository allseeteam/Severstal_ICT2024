import pickle
from django.db import models
from django.db.transaction import atomic
from django.forms import model_to_dict
from rest_framework import serializers

from accounts.models import (
    Data, MetaBlock, Report,
    ReportBlock, SearchQuery, Template, Theme
)
from accounts.tasks import add_data_to_report_block
from extract.reports import get_one_figure_by_entity


search_engine = None
try:
    search_engine = pickle.load(open('search.pkl', 'rb'))
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
        fields = ('id', 'query_template', 'position')


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
            data_obj: Data | None = None
            if search_engine:
                result = search_engine.search(
                    f'{meta_block.query_template} {search_query}'
                )
                index_ids = list(map(lambda x: x[0], result))
                data = Data.objects.filter(
                    index_id__in=index_ids
                )
                if data.count() > 0:
                    data_obj = data[0]

            if data_obj:
                entity = model_to_dict(data_obj)
                entity['frame'] = entity['data']
                entity['meta'] = entity['meta_data']['title']
                representation = get_one_figure_by_entity(
                    entity=entity,
                    return_plotly_format=True if meta_block.type == MetaBlock.PLOTLY else False
                )
            else:
                representation = {}

            block = ReportBlock.objects.create(
                report=report,
                data=data_obj,
                type=meta_block.type, # По сути type из мета блока брать нужно
                representation=representation, 
                position=meta_block.position,
                readiness=ReportBlock.READY if data_obj else ReportBlock.NOT_READY
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

class ReportLightSerializer(serializers.ModelSerializer):
    search_query = serializers.StringRelatedField()
    theme = serializers.SerializerMethodField()
    template = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'date'
        )

    def get_theme(self, obj):
        return obj.theme


class ReportSerializer(ReportLightSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'theme', 'template',
            'search_query',
            'blocks', 'date'
        )

    def get_blocks(self, obj):
        return ReportBlockSerializer(
            obj.blocks.all().annotate(
                source=models.F('data__page__url')
            ),
            many=True
        ).data

