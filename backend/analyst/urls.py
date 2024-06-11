from django.contrib import admin
from django.urls import include, path
# from accounts.views import search
from accounts.views import make_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('make_report/', make_report)
    # path('search', search)
]
