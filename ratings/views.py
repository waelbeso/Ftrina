from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.contenttypes.models import ContentType

from shop.models import Shop,Product

from . import app_settings
from .models import Rating
import json


from django.test import override_settings, Client, TestCase
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from profile.models import Profile

User = get_user_model
# Create your views here.
@api_view(['get'])
@permission_classes((AllowAny, ))
def get_ratings_view(request):



	#object_id = Shop.objects.get(slug="test-ftrina").id
	object_id = Shop.objects.get(slug="ftrina-store").id

	content_type = ContentType.objects.get(model="shop")
	instance =  content_type.get_object_for_this_type(pk=object_id)
	rating_for = Rating.objects.for_instance(instance)
	print "-----------------", rating_for.average

	object_id = Product.objects.get(pk="f5cfa967-6a72-4ad6-ba07-5b7d4ccd2519").id
	content_type = ContentType.objects.get(model="product")
	instance =  content_type.get_object_for_this_type(pk=object_id)
	rating_for = Rating.objects.for_instance(instance)
	print "-----------------", rating_for

	object_id = Shop.objects.get(slug="ftrina-store").id
	content_type = ContentType.objects.get(model="shop")

	instance =  content_type.get_object_for_this_type(pk=object_id)
	rating_for = Rating.objects.for_instance(instance)
	print "-----------------", rating_for

	client = Client(REMOTE_ADDR='127.0.0.1')
	ip = request.META['REMOTE_ADDR']
	score = 5
	user = Profile.objects.get(username="wael")
	print ip
	print user


	print dir(rating_for.user_ratings)
	print "has_rated: ", rating_for.user_ratings.has_rated(instance,user=user)
	#rating = Rating.objects.rate(instance, score, user=user, ip=ip)
	#print "-----------------",rating


	#try:
	#	ratings = Rating.objects.get(content_type = content_type, object_id= object_id  )
	#except Rating.DoesNotExist, e:
	#	ratings = "Does Not Exist"

	#print ratings
	return JsonResponse({ "sdlhfa":"adsfjh" }, status=200,safe=False)


@api_view(['post'])
@permission_classes((AllowAny, ))
def get_ratings_view(request):
	try:
		json_data=json.loads(request.body)
	except ValueError:
		return JSONResponse({ "errors": "empty payload" }, status=400)

	json_data=json.loads(request.body)
	print json_data
	user = request.user

	if json_data.get('type') == "shop":
		object_id = Shop.objects.get(slug=json_data.get('actor') ).id
	if json_data.get('type') == "product":
		object_id = json_data.get('actor')
	if json_data.get('type') == "servise":
		object_id = json_data.get('actor')

	content_type = ContentType.objects.get(model=json_data.get('type') )
	instance =  content_type.get_object_for_this_type(pk=object_id)
	
	score = json_data.get('rat')
	rating = Rating.objects.rate(instance, score, user=user, ip= json_data.get('ip'))
	rating_for = int(Rating.objects.for_instance(instance).average)
	print rating_for
	#rating_for = 3
	from random import randint

	id = randint(0, 9999)
	return JsonResponse({ "id": id ,'rating':rating_for, 'rat':json_data.get('rat'),'user':json_data.get('user'),'ip':json_data.get('ip'),'actor':json_data.get('actor'),'type':json_data.get('type') }, status=202,safe=False)

	#return JsonResponse({ "id": rating.id,'rat':json_data.get('rat'),'user':json_data.get('user'),'ip':json_data.get('ip'),'actor':json_data.get('actor'),'type':json_data.get('type') }, status=202,safe=False)








