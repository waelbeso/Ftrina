from django.shortcuts import render
from messenger.models import Message,Conversation
from messenger.serializers import MessageSerializer,ConversationSerializer

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



class MessageViewSet(viewsets.ModelViewSet):

    User = get_user_model()
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request,page=None):

        conversation = request.query_params["include"]
        messages = Message.objects.filter( conversation = conversation )
        paginator = Paginator(messages, 10)
        #print paginator.page_range
        #print paginator.count
        #print paginator.num_pages
        #print dir(paginator)
        serializer = MessageSerializer(paginator.page(paginator.num_pages).object_list, many=True)
        data =  serializer.data

        return JsonResponse( data  , safe=False ,status=200)

    def create(self, request):
        json_data = json.loads(request.body)
        #print json_data

        if json_data['type'] == "shop":
            sender = Profile.objects.get(username=request.user.username)
            receiver = Profile.objects.get(username=json_data["message_to"])
            
            try:
                message_object = Message.objects.filter(message_from=sender,message_to=receiver)
            except Message.DoesNotExist:
                conversation = Conversation.objects.create()
                conversation.save()
                conversation.audience.add(sender,receiver)
            else:
                message_object = Message.objects.filter(message_from=sender,message_to=receiver)
                #print dir(message_object.first)
                #print message_object
                try:
                    conversation = message_object[0].conversation
                except IndexError:
                    conversation = Conversation.objects.create()
                    conversation.save()
                    conversation.audience.add(sender,receiver)
                else:
                    conversation = message_object[0].conversation

            serializer = MessageSerializer(data=json_data)
            if serializer.is_valid():
                message = Message.objects.create( 
                    message_from = sender, 
                    message_to = receiver ,
                    text=json_data["text"],
                    status = False,
                    conversation = conversation,
                    )
                message.save()
                #print message.id
                data = serializer.data
                data["id"] = str(message.id)
                #print data
                return JsonResponse(data, status=202)
            #print serializer.errors
            return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)
        if json_data['type'] == "chat":
            sender = Profile.objects.get(username=request.user.username)
            receiver = Profile.objects.get(username=json_data["message_to"])
            conversation = Conversation.objects.get(id= json_data["conversation"])
            #json_data["send_at"] = timezone.now
            serializer = MessageSerializer(data=json_data)
            if serializer.is_valid():
                message = Message.objects.create( 
                    message_from = sender, 
                    message_to = receiver ,
                    text=json_data["text"],
                    status = False,
                    conversation = conversation,
                    )
                message.save()
                #print message.id
                data = serializer.data
                data["id"] = str(message.id)
                #print data
                return JsonResponse(data, status=202)
            #print serializer.errors
            return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

message_detail = MessageViewSet.as_view({'get': 'retrieve','post':'create'})


class ConversationViewSet(viewsets.ModelViewSet):

    User                   = get_user_model()
    queryset               = Conversation.objects.all()
    serializer_class       = ConversationSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes     = (IsAuthenticated,)


    def retrieve(self, request):
        
        me = Profile.objects.get(username=request.user.username)
        #print me.username
        data = []
        conversations = Conversation.objects.filter(audience=me)

        for conversation in conversations:

            messages = Message.objects.filter( conversation = conversation.id)
            latest = messages.latest("send_at")

            data.append({ "id": conversation.id,
                "action": "messenger",
                "message_from": latest._from ,
                "message_to"  : latest._to ,
                "text"        : latest.text ,
                "send_at"     : latest.send_at,
                "status"      : latest.status,
                "from_avatar" : latest.message_from.get_avatar(),
                "to_avatar"   : latest.message_to.get_avatar(),
                })  

        return Response(data)

conversation_detail = ConversationViewSet.as_view({'get': 'retrieve'})









