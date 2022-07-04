from django.contrib import admin
from .models import OneTimeInfo, CryptoWallet


class OneTimeAdmin(admin.ModelAdmin):
    list_display = ("text", "password")
    list_filter = ("password",)


class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ("name", "wallet")


admin.site.register(OneTimeInfo, OneTimeAdmin)
admin.site.register(CryptoWallet, CryptoWalletAdmin)
