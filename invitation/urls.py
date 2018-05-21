from django.conf.urls import url
from invitation import views


urlpatterns = [
	url(r'^', views.Api_invitation_view),

	]