#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from basket.models import Basket
from shop.models import Order
from basket.serializers import BasketSerializer
from django.http import JsonResponse
from rest_framework.response import Response
import json


class BasketViewSet(viewsets.ModelViewSet):
    
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        """
        If provided 'pk' is "me" then return the current user Basket.
        """
        if pk == 'me':
            return JsonResponse([], status=202)
        
basket_detail = BasketViewSet.as_view({'get': 'retrieve'})






