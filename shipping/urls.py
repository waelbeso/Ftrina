from django.conf.urls import url
from shipping import views


urlpatterns = [
	#url(r'^me', views.Api_vendor_view),
	url(r'^(?P<pk>\w+|[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', views.shop_shipping),
	]