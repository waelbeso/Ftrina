from django.forms import widgets
from rest_framework import serializers

from profile.models import Profile
from django.contrib.auth.models import User


from messenger.models import Message,Conversation


class MessageSerializer(serializers.ModelSerializer):

	message_from = serializers.CharField(required=True)
	message_to   = serializers.CharField(required=True)
	status       = serializers.BooleanField(default=False)
	send_at      = serializers.DateTimeField(allow_null=True,required=False)
	text         = serializers.CharField(required=True)

	class Meta:
		model = Message
		fields = ('id', 'message_from','message_to','status','send_at',"text","conversation")

class ConversationSerializer(serializers.ModelSerializer):


	class Meta:
		model = Conversation
		fields = ('id')