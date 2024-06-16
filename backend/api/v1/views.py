from django.http import HttpResponse, HttpResponseBadRequest
from drf_spectacular import utils as spectacular_utils
from django.db import models
from django.db.transaction import atomic
from rest_framework import decorators, viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Data, Report, ReportBlock, SearchQuery, Template, Theme
from analyst.settings import YANDEX_SEARCH_API_TOKEN
from search.yagpt import ask_yagpt
from . import serializers


@spectacular_utils.extend_schema_view(
    list=spectacular_utils.extend_schema(
        parameters=[
            spectacular_utils.OpenApiParameter(
                name='q', description='Поисковый запрос', type=str
            ),
        ]
    )
)
class SearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DataSearchSerializer
    

    def list(self, request):
        search_query = self.request.query_params.get('q')
        queryset = Data.objects.none()
        if search_query:
            if serializers.search_engine:
                result = serializers.search_engine.search(search_query)
                index_ids = list(map(lambda x: x[0], result))
                queryset = Data.objects.filter(
                    index_id__in=index_ids
                )
            else:
                queryset = Data.objects.all()
            SearchQuery.objects.get_or_create(
                user=request.user,
                text=search_query
            )
            queryset = queryset \
                .annotate(
                    name=models.F('page__title')
                ) \
                .annotate(
                    url=models.F('page__url')
                )
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

class ThemeViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    model = Theme
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer


class TemplateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Template.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateTemplateSerializer
        return serializers.TemplateSerializer


class ReportBlockViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        return ReportBlock.objects \
            .annotate(
                source=models.F('data__page__url')
            )

    def get_serializer_class(self):
        if self.action == 'add_comment':
            return serializers.UpdateReportBlockComment
        if self.action == 'generate_summary':
            return serializers.ReportBlockSummaryModelSerializer
        return serializers.ReportBlockSerializer
    

    @decorators.action(
        methods=('post',),
        detail=True,
        url_name='add_comment'
    )
    def add_comment(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @decorators.action(
        methods=('post',),
        detail=True,
        url_name='generate_summary'
    )
    def generate_summary(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_id = serializer.data.get('type')

        try:
            prompt = instance.data.data + '\nКомментарий от пользователя:' + instance.comment
            print(prompt)
            instance.summary = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                model_id

            )
            instance.save()
        except Exception as e:
            print(e)
            pass
        serializer = serializers.ReportBlockSerializer(instance)
        return Response(serializer.data)


class ReportViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        user = self.request.user
        return Report.objects \
            .filter(user=user) \
            .annotate(
                theme=models.F('template__theme__name')
            )

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateReportSerializer
        if self.action == 'list':
            return serializers.ReportLightSerializer
        if self.action == 'download_report':
            return serializers.ReportFileFormatSerializer
        return serializers.ReportSerializer
    
    @atomic
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateReportSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        instance.theme = str(instance.template.theme)
        serializer = serializers.ReportSerializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @decorators.action(
        methods=('post',),
        detail=True,
        url_name='download_report'
    )
    def download_report(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report_type = serializer.data.get('type')
        
        if report_type == 'pdf':
            file = instance.get_pdf()
        elif report_type == 'msword':
            file = instance.get_word()
        elif report_type == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            file = instance.get_excel()

        return HttpResponse(
            file,
            content_type=f'application/{report_type}',
            headers={'Content-Disposition': f'attachment; filename={file.name}'}
        ) 

