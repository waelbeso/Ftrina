#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from report_bug.serializers import BugSerializer
from django.template.loader import render_to_string
import cloudinary
from cloudinary.utils import api_sign_request
import json
from django.core.mail import send_mail
from report_bug.models import Bug

from album.models import Image

@api_view(['GET'])
@permission_classes((AllowAny, ))
def Api_bug_signature_view(request):
    timestamp = request.GET.get('timestamp','')
    params = {"timestamp": timestamp }

    signature = api_sign_request( params , cloudinary._config.api_secret )
    data = {
    "timestamp":timestamp,
    "signature":signature,
    "api_key":cloudinary._config.api_key,
    #"tags":"bug",
    #"resource_type":"image",
    #"allowed_formats":['jpg', 'gif' , 'png'],
    #"allowed_formats":['image/gif', 'image/png' , 'image/jpg'],
    #"allowed_formats": 'image/jpeg,image/gif,image/png',
    #"acceptFileTypes": "/^image\/(gif|jpe?g|png)$/i",
    #"maxFileSize": 1000000,
    }
    return JsonResponse(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def Api_bug_view(request):
	json_data=json.loads(request.body)
	serializer = BugSerializer(data=json_data)
	if serializer.is_valid():
		user_message = json_data.get('message')
		user = request.user.username
		img = json_data.get('img')
		email = request.user.email
		
		path_to_txt = 'bug_report_body.txt'
		subjec = 'Bug report'
		context = {'user': user ,'message': user_message,'img':img,'user_email':email }
		message = render_to_string(path_to_txt, context)
		send_mail(subjec, message, 'admin@ftrina.com',
			["admin@ftrina.com"], fail_silently=False)

		image = Image.objects.filter(secure_url=img).update(confirmed = True,)

		new_bug = Bug.objects.create(
			user = user,
			email = email,
			message = user_message,
			img = img)
		new_bug.save()

		return JsonResponse({'status': 'Accepted' }, status=202)
	print serializer.errors
	return JsonResponse(serializer.errors, status=400 ,safe=False)









