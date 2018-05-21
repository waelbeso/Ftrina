from django.contrib import admin
# Register your models here.
from leaflet.admin import LeafletGeoAdmin
from profile.models import Profile,Address

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'mobile',
        'date_joined',

   )
    
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Address,LeafletGeoAdmin,)