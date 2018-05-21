#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invitation.serializers import InvitationSerializer
from invitation.models import Invitation
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
import json
from rest_framework.response import Response
import string,random
from django.utils.translation import get_language_info
from django.utils.translation import activate


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def Api_invitation_view(request, format=None):

	print request.body
	json_data=json.loads(request.body)
	serializer = InvitationSerializer(data=json_data)

	if serializer.is_valid():
		firstname = serializer.validated_data.get('firstname')
		email = serializer.validated_data.get('email')
		language = serializer.validated_data.get('language')
		inviter = request.user.username
		#invitation_number = ''.join(random.choice(string.lowercase) for i in range(24))


		path_to_txt = 'invitation_email_body.txt'
		activate(language)
		subjec = _('Invitation')
		context = {'name': firstname ,'inviter': request.user}
		message = render_to_string(path_to_txt, context)
		send_mail(subjec, message, 'admin@ftrina.com',
			[email], fail_silently=False)

		new_invitation = Invitation.objects.create(
			firstname = firstname,
			email = email,
			language = language,
			inviter = inviter)
		new_invitation.save()

		return JsonResponse({'status': 'Accepted' }, status=202)
	print str(serializer.errors)
	return JsonResponse(serializer.errors, status=400 ,safe=False)

