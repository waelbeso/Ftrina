
from django.conf.urls import url
from messenger import views


urlpatterns = [
	url(r'', views.message_detail),
	url(r'^(?P<pk>\w+|[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', views.message_detail),
	#url(r'^mes/(?P<pk>\w+)$', views.user_detail),
	#url(r'^mes/(?P<pk>[0-9a-z]+)$', views.user_detail),
	#url(r'^ChangePassword/$', views.user_change_password),
	

	]