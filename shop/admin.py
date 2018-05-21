#from django.contrib import admin

from django.contrib.gis import admin
from models import Shop,Seller,WareHouse,Branch,Product,Coverage,Coupon,Order,Collection

from leaflet.admin import LeafletGeoAdmin
#from leaflet.admin import LeafletGeoAdminMixin
from shop.forms import ShopUpdateForm
#admin.site.register(Shop, LeafletGeoAdmin,)
#admin.site.register(LeafletGeoAdmin)
admin.site.register(Collection,)
admin.site.register(Seller,)
admin.site.register(Product,)

admin.site.register(Branch,LeafletGeoAdmin,)
admin.site.register(WareHouse,LeafletGeoAdmin,)
admin.site.register(Coverage,LeafletGeoAdmin,)

admin.site.register(Coupon,)
admin.site.register(Order,)


#@admin.register(Shop)
class ShopAdmin(LeafletGeoAdmin, admin.ModelAdmin):
	form = ShopUpdateForm
	def date_joined(self, obj):
		return obj.owner.date_joined
	def username(self, obj):
		return obj.owner.username

	list_display = ('name', 'username', 'date_joined')

admin.site.register(Shop, ShopAdmin)



