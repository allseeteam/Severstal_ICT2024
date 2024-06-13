from django.contrib import admin

from . import models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MetaBlock)
class MetaBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Data)
class DataAdmin(admin.ModelAdmin):
    readonly_fields = ('page', 'file')


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WebPage)
class WebPageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    pass
