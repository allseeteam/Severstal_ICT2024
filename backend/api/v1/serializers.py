from typing import List
from rest_framework import serializers

from accounts.models import Data, Report, ReportBlock, SearchQuery


class DataSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    url  = serializers.SerializerMethodField(read_only=True)
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


class CreateReportSerializer(serializers.ModelSerializer):
    data_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
    search_query = serializers.CharField()

    class Meta:
        model = Report
        fields = (
            'data_ids',
            'search_query'
        )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        data_ids: List[int] = validated_data.get('data_ids')
        raw_search_query: str = validated_data.get('search_query')
        search_query, _ = SearchQuery.objects.get_or_create(
            user=user,
            text=raw_search_query
        )

        report = Report.objects.create(
            user=user,
            search_query=search_query
        )

        data = Data.objects.filter(id__in=data_ids)
        blocks = [
            ReportBlock(
                report=report,
                data=d,
                position=i+1
            )
            for i, d in enumerate(data) 
        ]
        ReportBlock.objects.bulk_create(
            objs=blocks
        )

        return report
    

class ReportBlockSerializer(serializers.ModelSerializer):
    represent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReportBlock
        fields = (
            'represent', 'position'
        )

    def get_represent(self, obj):
        return obj.data.data
        entity = {
            'meta': obj.data.meta_data,
            'url': obj.page.url if obj.page else '',
            'frame': obj.data.data
        }


class ReportSerializer(serializers.ModelSerializer):
    blocks = ReportBlockSerializer(many=True)
    class Meta:
        model = Report
        fields = ('user', 'blocks')
