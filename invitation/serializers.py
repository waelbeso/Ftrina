from rest_framework import serializers
from invitation.models import Invitation
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.utils.translation import ugettext_lazy as _

from profile.models import Profile

class InvitationSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(required=True, max_length=20)

    email = serializers.EmailField(required=True, allow_blank=False,max_length=50,
    	#validators=[UniqueValidator(queryset=User.objects.all(),
    	validators=[UniqueValidator(queryset=Profile.objects.all(),
    		message= "That EMAIL is already registered with Us." )],)

    language = serializers.CharField(required=True)

    class Meta:
        model = Invitation
        fields = ('firstname','email', 'language')