import pickle
from django.db import models
from django.db.transaction import atomic
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Data, Report, SearchQuery
from .serializers import CreateReportSerializer, DataSearchSerializer, ReportSerializer


search_engine = None
try:
    search_engine = pickle.load(open('search.pkl', 'rb'))
except FileNotFoundError:
    print('No search.pkl file found')

class SearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DataSearchSerializer
    

    def list(self, request):
        search_query = self.request.query_params.get('q')
        queryset = Data.objects.none()
        if search_query:
            if search_engine:
                result = search_engine.search(search_query)
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
    

class ReportViewSet(viewsets.ModelViewSet):
    model = Report

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReportSerializer
        return ReportSerializer
    
    @atomic
    def create(self, request, *args, **kwargs):
        serializer = CreateReportSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        serializer = ReportSerializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
