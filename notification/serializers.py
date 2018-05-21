from django.forms import widgets
from rest_framework import serializers

from profile.models import Profile
from django.contrib.auth.models import User


from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

	notification_to = serializers.CharField(required=True)
	status          = serializers.BooleanField(default=False)
	send_at         = serializers.DateTimeField(allow_null=True,required=False)
	message         = serializers.CharField(required=True)
	title           = serializers.CharField(required=True)

	class Meta:
		model = Notification
		fields = ('id', 'notification_to','status','send_at',"message","title","timesince")
		order_by = ( ('timesince',) )