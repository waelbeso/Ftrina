from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from profile.serializers import ProfileSerializer,ChangePasswordSerializer,AddressSerializer,LanguageSerializer
from rest_framework.response import Response
from django.http import JsonResponse

from profile.models import Profile,Address
#from django.contrib.auth.models import User
import json
from basket.serializers import BasketSerializer
from basket.models import Basket

from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
#User = get_user_model()

#@authentication_classes((TokenAuthentication,))
#@permission_classes((IsAuthenticated,))

class LanguageViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'me':
            serializer = LanguageSerializer(request.user)
            data=serializer.data
            data['id'] = "me"
            return Response(data)
        return super(LanguageViewSet, self).retrieve(request, pk)

    def update(self, request,pk):
        json_data = json.loads(request.body)
        print json_data

        profile = request.user
        serializer = LanguageSerializer(profile, data=json_data)

        if serializer.is_valid():
            serializer.update(profile,json_data)
            data=serializer.data
            data['id'] = "me"
            print JsonResponse(data)
            return JsonResponse(data, status=202)

        print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

language_detail = LanguageViewSet.as_view({'get': 'retrieve','put':'update'})



class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request):

        #profile = Profile.objects.get(id=request.user.id)
        #print profile.id
        address = Address.objects.filter(profile=request.user.id)
        serializer = AddressSerializer(address, many=True)
        data=serializer.data

        return Response(data)

    def create(self, request):
        #print request.body
        json_data = json.loads(request.body)
        #shop = Shop.objects.get(owner=request.user)
        #print json_data["geom"]

        # rebuild the json data to add the shop ID
        # shop id is required in AddressesValidator
        data = {}
        data['name']     = { "name": json_data["name"] , "profile": str(request.user.id) , "method":"new"}
        data['country']  = json_data["country"]
        data['province'] = json_data["province"]
        data['city']     = json_data["city"]
        data['zip_code'] = json_data["zip_code"]
        data['address']  = json_data["address"]
        data['geom']     = json_data["geom"]
        #print json_data["geom"].get('lat')
        #print json_data["geom"].get('lng')

        

        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            #shop = Shop.objects.get(owner=request.user)
            #print 'valid'
            #point = Point(json_data["geom"].get('lng'),json_data["geom"].get('lat'),srid=4326)
            point = Point(json_data["geom"][0]['lng'],json_data["geom"][0]['lat'],srid=4326)
            address = Address.objects.create(
                profile  = request.user,
                name     = json_data['name'],
                country  = json_data['country'],
                province = json_data['province'],
                city     = json_data['city'],
                zip_code = json_data['zip_code'],
                address  = json_data['address'],
                geom     = point
                )
            address.save
            #print address.id
            return JsonResponse({'id':address.id,'name': address.name}, status=202)
        
        #print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def update(self, request,pk):
        json_data = json.loads(request.body)
        #print json_data

        #shop = Shop.objects.get(owner=request.user)

        data = {}
        data['name']     = { "name": json_data["name"] , "profile": str(request.user.id) , "method":"update","pk":pk }
        data['country']  = json_data["country"]
        data['province'] = json_data["province"]
        data['city']     = json_data["city"]
        data['zip_code'] = json_data["zip_code"]
        data['address']  = json_data["address"]
        data['geom']     = json_data["geom"]


        serializer = AddressSerializer(data=data)

        if serializer.is_valid():
            #shop = Shop.objects.get(owner=request.user)
            address          = Address.objects.get(pk=pk)
            address.name     = json_data['name']
            address.country  = json_data['country']
            address.province = json_data['province']
            address.city     = json_data['city']
            address.zip_code = json_data['zip_code']
            address.address  = json_data['address']
            #address.geom    = Point(json_data["geom"].get('lng'),json_data["geom"].get('lat'),srid=4326)
            address.geom     = Point(json_data["geom"][0]['lng'],json_data["geom"][0]['lat'],srid=4326)
            address.save()
            data['name']     = json_data["name"]
            data['id']       = address.id

            print JsonResponse(data)
            return JsonResponse(data, status=202)

        #print serializer.errors
        return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

    def get_object(self, pk):
        from rest_framework import status
        from django.http import Http404
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def delete(self, request,pk):

        from rest_framework import status
        #shop = Shop.objects.get(owner=request.user)
        address = Address.objects.get(pk=pk)
        if request.user.id == address.profile.id:
            
            address = self.get_object(pk)
            address.delete()
            #return JsonResponse({ "errors": 'You have no authority' }, status=400,safe=False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({ "errors": 'You have no authority to delete this Address' }, status=400,safe=False)

profile_address = AddressViewSet.as_view({'get': 'retrieve','post':'create','put':'update','delete':'delete'})

class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    #queryset = User.objects.all()
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes =(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def retrieve(self, request, pk=None):
        #print dir(request)
        #print request.META['REMOTE_ADDR']

        """
        If provided 'pk' is "me" then return the current user.
        """
        if pk == 'me':
            #print request.user
            data = ProfileSerializer(request.user).data 
            data['photo'] = request.user.get_avatar()
            data['is_seller'] = request.user.is_seller


            
            #print data['basket']
            if request.user.is_seller:
                data['seller_for'] = request.user.seller_for
            #print "request.user.is_seller",request.user.is_seller
            #print "request.user.is_seller",request.user.seller_for
            data['id'] = "me"
            data['ip'] = request.META['REMOTE_ADDR']
            return Response(data)
        return super(UserViewSet, self).retrieve(request, pk)

    def update(self, request, pk=None):
        #print request.body
    	#print 'update'
        profile = Profile.objects.get(pk=request.user.id)
    	json_data=json.loads(request.body)


    	serializer = ProfileSerializer(profile, data=json_data)
    	if serializer.is_valid():

            '''  if email Change Re verifi the user email '''
            if not str(profile.email) == str(json_data.get('email')):
                
                from rest_framework.authtoken.models import Token
                from email_confirmation.tasks import confirm_user_email_task
                try:
                    user = Profile.objects.get(email=json_data.get('email'))
                except Profile.DoesNotExist:
                    user = request.user
                    user.email_verified = False
                    user.save()
                    new_email = json_data.get('email')
                    confirmation_key = user.add_email_if_not_exists(new_email)
                    confirm_user_email_task.apply_async((new_email,),countdown=1)
                    #print "email change"
                    serializer.save()
                    return JsonResponse({'id':request.user.id,'status': 'Accepted' }, status=202)
                return JsonResponse({ "errors": { "email":"That EMAIL is already registered, please select another."} }, status=400,safe=False)

            '''  if mobile Change Re verifi the user mobile '''
            if not str(profile.mobile) in str(json_data.get('mobile')):
                from mobile_confirmation.tasks import confirm_user_mobile_task
                try:
                    user = Profile.objects.get(mobile=json_data.get('mobile'))
                except Profile.DoesNotExist:
                    user = request.user
                    user.mobile_verified = False
                    user.save()
                    new_mobile = json_data.get('mobile')
                    confirmation_key = user.add_mobile_if_not_exists(new_mobile)
                    confirm_user_mobile_task.apply_async((new_mobile,),countdown=1)
                    #print "mobile change"
                    serializer.save()
                    return JsonResponse({'id':request.user.id,'status': 'Accepted' }, status=202)
                return JsonResponse({ "errors": { "mobile":"That MOBILE is already registered, please select another."} }, status=400,safe=False)

            serializer.save()
            return JsonResponse({'id':'me','status': 'Accepted' }, status=202)
    	print serializer.errors
    	return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)
user_detail = UserViewSet.as_view({'get': 'retrieve','put':'update'})


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_change_password(request):

	json_data=json.loads(request.body)
	user = request.user
	serializer = ChangePasswordSerializer(data=json_data)

	if serializer.is_valid():
		if request.user.check_password(json_data.get('old_password')):
			user.set_password(json_data.get('new_password'))
			user.save()
			return JsonResponse({'status': 'Accepted'}, status=202)
		else:
			return JsonResponse({"errors": {"old_password": ["password is not correct."]}}, status=401,safe=False)
	#print serializer.errors
	return JsonResponse({ "errors": serializer.errors }, status=400,safe=False)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def Confirmations_view(request):
    json_data=json.loads(request.body)
    #print json_data
    user = request.user
    if "email" in str(json_data.get('target')):

        from email_confirmation.tasks import confirm_user_email_task
        user  = request.user
        email = user.email
        confirm_user_email_task.apply_async((email,),countdown=1)

    if "mobile" in str(json_data.get('target')):

        from mobile_confirmation.tasks import confirm_user_mobile_task
        user = request.user
        mobile = str(user.mobile)
        confirm_user_mobile_task.apply_async((mobile,),countdown=1)

    return JsonResponse({ 'status': 'Accepted' }, status=202)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def Verifications_view(request):
    json_data=json.loads(request.body)
    #print json_data
    user = request.user
    attachment = json_data.get('attachment')
    
    if "email" in str(json_data.get('target')):
        #print "he need to verifi email"
        if str(user.email_confirmation_key) in str(json_data.get('code')):
            user.email_verified = True
            user.save()
            json_data["id"]="me"
            return JsonResponse(json_data, status=200)
        return JsonResponse({"errors": {"code": ["Invalid Code."]}}, status=404)

    if "mobile" in str(json_data.get('target')):
        #print "he need to verifi mobile"
        if str(user.mobile_confirmation_key) == str(json_data.get('code')):
            user.mobile_verified = True
            user.save()
            json_data["id"]="me"
            return JsonResponse(json_data, status=200)
        return JsonResponse({"errors": {"code": ["Invalid Code."]}}, status=404)

    if "person" in str(json_data.get('target')):
        #print "he need to verifi person"
        if "None" in str(json_data.get('attachment')):
            return JsonResponse({"errors": {"attachment": ["Your ID is required."]}}, status=404)

        from profile.tasks import verification_confirmation_task
        verification_confirmation_task(user=user,target="person",attachment=attachment)
        json_data["id"]="me"
        return JsonResponse(json_data, status=200)

    if "business" in str(json_data.get('target')):
        #print "he need to verifi business"
        if "None" in str(json_data.get('attachment')):
            return JsonResponse({"errors": {"attachment": ["Your BUSINESS LICENS is required."]}}, status=404)

        from profile.tasks import verification_confirmation_task
        verification_confirmation_task(user=user,target="business",attachment=attachment)
        json_data["id"]="me"
        return JsonResponse(json_data, status=200)


