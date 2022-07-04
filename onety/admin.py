from django.contrib import admin
from .models import OnetyModel


class OnetyModelAdmin(admin.ModelAdmin):
    list_display = ("text", "email")
    list_filter = ("email",)


admin.site.register(OnetyModel, OnetyModelAdmin)
