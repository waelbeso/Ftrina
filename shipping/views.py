


from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import authentication_classes,permission_classes

from django.http import JsonResponse
from shipping.models import Model,Zone
from shipping.serializers import ModelSerializer,ZoneSerializer
from shop.models import Shop,WareHouse
from rest_framework.response import Response
import json

class ShippingViewSet(viewsets.ModelViewSet):

    queryset               = Model.objects.all()
    serializer_class       = ModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes     = (IsAuthenticated,)


    def retrieve(self, request):
    	try:
    		Shop.objects.get(owner=request.user)
    	except Shop.DoesNotExist:
    		return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        shop                = Shop.objects.get(owner=request.user)
        shop_shipping_model = Model.objects.filter(shop=shop)
        serializer          = ModelSerializer(shop_shipping_model, many=True)

        data       = serializer.data
        return Response(data, status=200)

    def create(self, request):

    	json_data = json.loads(request.body)
        try:
            Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        # rebuild the json data to add the shop ID
        # shop id is required in ShippingValidator
        shop                = Shop.objects.get(owner=request.user)

        data = {}
        data['name']       = { "name": json_data["name"] , "shop": str(shop.id) , "method":"new" }
        data['ware_house'] = json_data['ware_house']
        data['shop']       = str(shop.id)

        serializer = ModelSerializer(data=data)
        if serializer.is_valid():
        	shop      = Shop.objects.get(owner=request.user)
        	warehouse = WareHouse.objects.get(pk=json_data['ware_house'])

        	shop_shipping_model = Model.objects.create(
        		shop = shop,
        		name =  json_data['name'],
        		ware_house = warehouse,
        		)
        	shop_shipping_model.save
        	json_data["id"] = str(shop_shipping_model.id)
        	return JsonResponse(json_data, status=202)
        print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def update(self, request,pk):

        json_data = json.loads(request.body)
        try:
            Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        # rebuild the json data to add the shop ID
        # shop id is required in ShippingValidator
        shop                = Shop.objects.get(owner=request.user)

        data = {}
        data['name']       = { "name": json_data["name"] , "shop": str(shop.id) , "method":"update","pk":pk }
        data['ware_house'] = json_data['ware_house']
        data['shop']       = str(shop.id)

        serializer = ModelSerializer(data=data)        
        if serializer.is_valid():
        	print "yes"
        	serializer.validated_data["name"] = json_data['name']
        	shop_shipping_model = Model.objects.get(pk=pk)

        	serializer.update(shop_shipping_model,serializer.data)
        	data = serializer.data
        	data["id"] = pk
        	return JsonResponse(data, status=202)
        print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def get_object(self, pk):
        from rest_framework import status
        from django.http import Http404
        try:
            return Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            raise Http404

    def delete(self, request,pk):
        from rest_framework import status
        shop = Shop.objects.get(owner=request.user)
        shop_shipping_model = Model.objects.get(pk=pk)
        if shop == shop_shipping_model.shop:
        	shop_shipping_model = self.get_object(pk)
        	shop_shipping_model.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({ "errors": 'You have no authority' }, status=400,safe=False)

shop_shipping = ShippingViewSet.as_view({'get': 'retrieve','post':'create','put':'update'})



class ShippingZoneViewSet(viewsets.ModelViewSet):

    queryset               = Zone.objects.all()
    serializer_class       = ZoneSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes     = (IsAuthenticated,)


    def retrieve(self, request):
    	try:
    		Shop.objects.get(owner=request.user)
    	except Shop.DoesNotExist:
    		return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        shop       = Shop.objects.get(owner=request.user)
        zone       = Zone.objects.filter(shop=shop)
        serializer = ZoneSerializer(zone, many=True)
        data       = serializer.data
        return Response(data, status=200)

    def create(self, request):

    	json_data = json.loads(request.body)
        try:
            Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        
        serializer = ZoneSerializer(data=json_data)
        print json_data

        if serializer.is_valid():
        	model      = Model.objects.get(pk=json_data['model'])
        	shop       = Shop.objects.get(owner=request.user)

        	shop_shipping_zone = Zone.objects.create(
        		shop  = shop,
        		model =  model,
        		country = json_data['country'],
        		province = json_data['province'],
        		price = json_data['price'],
        		price_currency =json_data['price_currency'],
        		)
        	shop_shipping_zone.save
        	json_data["id"] = str(shop_shipping_zone.id)
        	return JsonResponse(json_data, status=202)
        print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def update(self, request,pk):

        json_data = json.loads(request.body)
        try:
            Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return JsonResponse({ "errors": "Bad Request" }, status=404,safe=False)

        if json_data['price']:
        	try:
        		int( json_data['price'])
        	except Exception, e:
        		return JsonResponse({ "errors": {"price":"A valid number is required."} }, status=400,safe=False) 

        	shop_shipping_zone = Zone.objects.filter(pk=pk).update(price = json_data['price'] )
        	json_data["id"] = pk
        	return JsonResponse(json_data, status=202)
        return JsonResponse({ "errors": {"price":"This field may not be null."} }, status=400,safe=False)

    def get_object(self, pk):
        from rest_framework import status
        from django.http import Http404
        try:
            return Zone.objects.get(pk=pk)
        except Zone.DoesNotExist:
            raise Http404

    def delete(self, request,pk):
        from rest_framework import status
        shop = Shop.objects.get(owner=request.user)
        shop_shipping_model = Zone.objects.get(pk=pk)
        if shop == shop_shipping_model.shop:
        	shop_shipping_model = self.get_object(pk)
        	shop_shipping_model.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({ "errors": 'You have no authority' }, status=400,safe=False)

shop_shipping_zone = ShippingZoneViewSet.as_view({'get': 'retrieve','post':'create','put':'update'})
