

from django.conf.urls import url
from report_bug import views


urlpatterns = [
	url(r'^report$', views.Api_bug_view),
	url(r'^signature$', views.Api_bug_signature_view ),
	]