from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views


v1_router = DefaultRouter()
v1_router.register('search', views.SearchView, basename='search')
v1_router.register('report', views.ReportViewSet, basename='report')
v1_router.register('theme', views.ThemeViewSet, basename='theme')
v1_router.register('template', views.TemplateViewSet, basename='template')
v1_router.register('report_block', views.ReportBlockViewSet, basename='report_block')

urlpatterns = [
    path('auth/', obtain_auth_token, name='auth'),
    path('', include(v1_router.urls)),
    path(
        'schema/',
        SpectacularAPIView.as_view(api_version='api/v1'),
        name='schema'
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='api:schema'),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='api:schema'),
        name='redoc',
    ),
]