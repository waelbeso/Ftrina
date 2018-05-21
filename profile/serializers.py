from django.forms import widgets
from rest_framework import serializers

from profile.models import Profile,Address
from django.contrib.auth.models import User

from django.contrib.gis.geos import Point


class LanguageSerializer(serializers.ModelSerializer):
	preferred_language = serializers.ChoiceField(required=True,choices=(('ar', 'Arabic'), ('en', 'English'), ('zh-hans', 'Chinese'),('fr','French')))

	def update(self, instance, validated_data):
		instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
		instance.save()
		return instance

	class Meta:
		model = Profile
		fields = ('id','preferred_language')


class ProfileSerializer(serializers.ModelSerializer):

	username         = serializers.CharField(required=False, allow_blank=False)
	#photo            = serializers.URLField(required=False, max_length=200, min_length=None, allow_blank=False)

	first_name       = serializers.CharField(required=True, allow_blank=False)
	last_name        = serializers.CharField(required=True, allow_blank=False)
	gender           = serializers.ChoiceField(required=True, allow_blank=False, choices=(('m', 'Male'), ('f', 'Female')))
	date_of_birth    = serializers.DateField(required=True)

	#website_url      = serializers.URLField(max_length=200,  allow_empty=True)
	about_me         = serializers.CharField(required=False, allow_blank=True,max_length=None, min_length=None)
	profile_language = serializers.ChoiceField(required=True,choices=(('arabic', 'Arabic'), ('english', 'English'), ('chinese', 'Chinese')))


	def create(self, validated_data):
		return Profile.objects.create(**validated_data)

	def update(self, instance, validated_data):

		instance.first_name         = validated_data.get('first_name',instance.first_name )
		instance.last_name          = validated_data.get('last_name', instance.last_name)
		instance.gender             = validated_data.get('gender', instance.gender)
		instance.date_of_birth      = validated_data.get('date_of_birth', instance.date_of_birth)
		#instance.website_url        = validated_data.get('website_url', instance.website_url)
		instance.about_me           = validated_data.get('about_me', instance.about_me)
		instance.profile_language   = validated_data.get('profile_language', instance.profile_language)
		instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
		instance.email              = validated_data.get('email',  instance.email)
		instance.mobile             = validated_data.get('mobile', instance.mobile)

		instance.save()
		return instance
	class Meta:
		model = Profile
		fields = (
			'id','first_name','last_name','email','username','is_active','last_login','date_joined',
			'mobile', 'shopname','shop_created',
			'about_me','website_url','date_of_birth','gender','profile_language',
			'verified','premium','verified_business','verified_person',
			'vendor','shipper','expires_at','preferred_language',
			'blog_url','access_token','raw_data','facebook_profile_url','facebook_name',
			'facebook_id','facebook_open_graph','new_token_required',
			'email_verified','mobile_verified','is_vendor','shop_url',
			)


class ChangePasswordSerializer(serializers.Serializer):


    def PasswordValidator(value):
        from  django.contrib.auth.password_validation import validate_password
        validate_password(value)

    old_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False,
        validators=[PasswordValidator],)

class GeomField(serializers.Field):
	from django.contrib.gis.geos import Point
	def to_representation(self, obj):
		#return "geom(%d, %d)" % (obj.get_y(), obj.get_x())
		#return '{"lat":%f,"lng":%f}' % (obj.get_y(), obj.get_x())
		return [{"lat":obj.get_y(),"lng":obj.get_x()}]

	def to_internal_value(self, data):
		#return Point(data.get('lng'),data.get('lat'),srid=4326)
		return Point(data[0]['lng'],data[0]['lat'],srid=4326)

class AddressSerializer(serializers.ModelSerializer):

	def AddressValidator(value):
		import json
		if "update" in value['method']:
			print "update"
			print value['pk']
			if value['name']:
				try:
					Address.objects.get(name=value['name'],profile=value['profile'])
				except Address.DoesNotExist:
					return
				address = Address.objects.get(name=value['name'],profile=value['profile'])
				if str(address.id) in value['pk']:
					return
				raise serializers.ValidationError('You have Address with this name.')
			raise serializers.ValidationError('Address name is required.')

		if "new" in value['method']:
			if value['name']:
				try:
					Address.objects.get(name=value['name'],profile=value['profile'])
				except Address.DoesNotExist:
					return
				raise serializers.ValidationError('You have Address with this name.')
			raise serializers.ValidationError('Address name is required.')

	name = serializers.JSONField(required=True,
		validators=[AddressValidator ],)

	country = serializers.CharField(required=True)
	province = serializers.CharField(required=True)
	city = serializers.CharField(required=True)
	zip_code = serializers.IntegerField(required=True)
	address = serializers.CharField(required=True)
	geom = GeomField()

	class Meta:
		model = Address
		fields = ('id', 'name','country','province','city','zip_code','address','geom')

#class UserSerializer(serializers.ModelSerializer):
#
#	first_name = serializers.CharField(required=True, allow_blank=False)
#	last_name = serializers.CharField(required=True, allow_blank=False)
#	username = serializers.CharField(required=False, allow_blank=False)
#
#	#profile = ProfileSerializer(many=False)
#	
#	#   Methods for nested representations
#	#   http://www.django-rest-framework.org/api-guide/serializers/
#	def update(self, instance, validated_data):
#		profile_data = validated_data.pop('profile')
#		profile = instance.profile
#
#		instance.first_name = validated_data.get('first_name', instance.first_name)
#		instance.last_name = validated_data.get('last_name', instance.last_name)
#		instance.save()
#
#		profile.email = profile_data.get('email', profile.email)
#		profile.mobile = profile_data.get('mobile', profile.mobile)
#		profile.shopname = profile_data.get('shopname', profile.shopname)
#		profile.about_me = profile_data.get('about_me', profile.about_me)
#		profile.website_url = profile_data.get('website_url', profile.mobile)
#		profile.date_of_birth = profile_data.get('date_of_birth', profile.mobile)
#		profile.gender = profile_data.get('gender', profile.gender)
#		profile.profile_language = profile_data.get('profile_language', profile.mobile)
#		profile.preferred_language = profile_data.get('preferred_language', profile.mobile)
#
#		profile.save()
#		return instance
#
#	class Meta:
#		model = User
#		fields = ('id','username', 'first_name','last_name','is_active','last_login','date_joined','profile')


