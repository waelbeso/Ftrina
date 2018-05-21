from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from future_customer.serializers import FutureCustomerSerializer
from future_customer.models import Future_Customer
from django.http import JsonResponse
import json


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def future_customer_view(request):
	try:
		json_data=json.loads(request.body)
	except ValueError:
		return JSONResponse({ "errors": "empty payload" }, status=400)

	json_data = json.loads(request.body)
	print json_data
	serializer = FutureCustomerSerializer(data=json_data)
	if serializer.is_valid():
		print "is_valid"
		customer = Future_Customer.objects.create(
			name=serializer.validated_data.get('name'),
			email =serializer.validated_data.get('email'),
			mobile = serializer.validated_data.get('mobile'),
			)
		customer.save()
		data = serializer.data
		data['id'] = customer.id
		return JsonResponse(data, status=202)

	print serializer.errors
	return JsonResponse({'errors': serializer.errors }, status=400)