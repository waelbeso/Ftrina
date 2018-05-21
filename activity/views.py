from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

from .models import Follow
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse


class UserActionsSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = Follow.objects.all()
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def follow(self,request,data):
    	print 'it is follow'
    	actor = ContentType.objects.get(app_label=data.get('type'), model=data.get('type'))
    	#print dir(actor.model_class())
    	if 'shop' == data.get('type'):
    		actor_type = actor.model_class().objects.get(slug=data.get('actor'))
    		instance = Follow.objects.create(
    			profile     = request.user,
    			actor       = actor,
    			actor_uuid  = actor_type.id,
    			actor_slug  = data.get('actor')
    			)
    	return instance.id

    def unfollow(self,request,data):
    	print "it is unfollow"
    	actor = ContentType.objects.get(app_label=data.get('type'), model=data.get('type'))
    	if 'shop' == data.get('type'):
    		actor_type = actor.model_class().objects.get(slug=data.get('actor'))
    		instance = Follow.objects.get(
    			profile     = request.user,
    			actor       = actor,
    			actor_uuid  = actor_type.id,
    			actor_slug  = data.get('actor')
    			)
    		instance_id = instance.id
    		instance.delete()
    	return instance_id

    def post(self,request):
    	try:
    		json_data=json.loads(request.body)
    	except ValueError:
    		return JSONResponse({ "errors": "empty payload" }, status=400)

    	json_data=json.loads(request.body)
    	user = request.user

    	if 'follow' == json_data.get('verb'):
    		instance = self.follow(request,json_data)
    		return JsonResponse({ "id": instance,'user':json_data.get('user'),'verb':'follow','actor':json_data.get('actor'),'type':json_data.get('type') }, status=202,safe=False)

    	if 'unfollow' == json_data.get('verb'):
    		instance = self.unfollow(request,json_data)
    		return JsonResponse({ "id": instance,'user':json_data.get('user'),'verb':'unfollow','actor':json_data.get('actor'),'type':json_data.get('type') }, status=202,safe=False)

    	return JsonResponse({ "errors": "Verb is not supported" }, status=400,safe=False)


user_actions_api_view = UserActionsSet.as_view({'post': 'post'})






