from django.contrib import admin

from .models import MobileNumbers


class MobileNumbersAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'key', 'set_at', 'confirmed_at')
    search_fields = ('mobile', 'key')

admin.site.register((MobileNumbers,), MobileNumbersAdmin)
