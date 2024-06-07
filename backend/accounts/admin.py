from django.contrib import admin

from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WebPage)
class WebPageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WebVideo)
class WebVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserFiles)
class UserFilesAdmin(admin.ModelAdmin):
    pass
