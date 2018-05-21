from django.shortcuts import render

from notification.models import Notification
from notification.serializers import NotificationSerializer

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response

from django.contrib.auth import get_user_model
import json
from django.utils import timezone
from profile.models import Profile
from django.http import JsonResponse
# Create your views here.

from django.core.paginator import Paginator

from django.utils import timezone


#from notification.announcer import Notification_Client

class NotificationViewSet(viewsets.ModelViewSet):

    User                   = get_user_model()
    queryset               = Notification.objects.all()
    serializer_class       = NotificationSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes     = (IsAuthenticated,)


    def retrieve(self, request):

        me = Profile.objects.get(username=request.user.username)
        data = []
        notification = Notification.objects.filter(notification_to=me)
        #print dir(notification)
        paginator = Paginator(notification, 10)

        serializer = NotificationSerializer(paginator.page(paginator.num_pages).object_list, many=True)
        data =  serializer.data
        print timezone.now()
        return JsonResponse( data  , safe=False ,status=200)


    def get_object(self, pk):
        from rest_framework import status
        from django.http import Http404

        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            raise Http404

    def delete(self, request,pk):
        print"dsafasd"
        from rest_framework import status
        notification = Notification.objects.get(pk=pk)
        notification.notification_to.id
        if request.user.id == notification.notification_to.id:
            print "yes"
            notification = self.get_object(pk)
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({ "errors": 'You have no authority to delete this notification' }, status=400,safe=False)

notification_detail = NotificationViewSet.as_view({'get': 'retrieve','put':'update'})









