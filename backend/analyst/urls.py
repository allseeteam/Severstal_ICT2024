from django.contrib import admin
from django.urls import include, path
# from accounts.views import search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('search', search)
]
