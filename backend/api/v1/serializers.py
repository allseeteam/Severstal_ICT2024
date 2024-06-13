import pickle
from typing import List
from django.db.transaction import atomic
from django.forms import model_to_dict
from rest_framework import serializers

from accounts.models import Data, MetaBlock, Report, ReportBlock, SearchQuery, Template, Theme
from extract.reports import get_all_possible_charts, plot_entity, plotly_obj_to_json
from extract.process_df import preprocess_entities


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
            search_query=search_query
        )

        raw_blocks = []

        for meta_block in template.meta_blocks.all():
            data_obj: Data | None
            if search_engine:
                result = search_engine.search(search_query)
                index_ids = list(map(lambda x: x[0], result))
                data = Data.objects.filter(
                    index_id__in=index_ids
                )
                if data.count() > 0:
                    data_obj = data[0]
            else:
                data_obj = Data.objects.last()

            block = ReportBlock(
                report=report,
                data=data_obj,
                type='График',  # Святу подумать
                representation={},  # Тут надо Святу подумать, один блок на entity создаем?
                position=meta_block.position,
                readiness=ReportBlock.READY if data_obj else ReportBlock.NOT_READY
            )
            raw_blocks.append(block)

            if not data_obj:
                pass
                # тут будем запускать таску на загрузку из поиска

        ReportBlock.objects.bulk_create(
            objs=raw_blocks
        )

        return report


class ReportBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportBlock
        fields = (
            'id',
            'readiness',
            'type',
            'representation',
            'position'
        )


class ReportSerializer(serializers.ModelSerializer):
    search_query = serializers.StringRelatedField()
    blocks = ReportBlockSerializer(many=True)

    class Meta:
        model = Report
        fields = ('id', 'search_query', 'blocks', 'date')
