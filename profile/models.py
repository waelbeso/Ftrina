
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
#from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
#from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
#from shop.models import Shop

from django.contrib.auth import get_user_model
from email_confirmation.models import UserEmailConfirmation
from mobile_confirmation.models import UserMobileConfirmation
#User = get_user_model()
from django.contrib.gis.db.models import PointField


from django.contrib.sessions.models import Session


class ProfileManager(UserManager):
	"verifi an Profile. Returns the Profile that was verified."
	def create_verifi(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.verified=True
			user.save(update_fields=['verified'])
		return user.is_verified

	"premium an Profile. Returns the Profile that was premium."
	def create_premium(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.premium=True
			user.save(update_fields=['premium'])
		return user.is_premium

	"unpremium an Profile. Returns the Profile that was unpremium."
	def create_unpremium(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.premium=False
			user.save(update_fields=['premium'])
		return user.is_premium

	"unverifi an Profile. Returns the Profile that was unverifi."
	def create_unverifi(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.verified=False
			user.save(update_fields=['verified'])
		return user.is_verified

	"verified_business for an Profile. Returns the Profile that was verified_business."
	def create_verified_business(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.verified_business=True
			user.save(update_fields=['verified_business'])
		return user.is_verified_business


	"verified_person for  an Profile. Returns the Profile that was verified_business."
	def create_verified_person(self, user=None, save=False):
		user = user or getattr(self, 'instance', None)
		if not user:
			raise ValueError('Must specify user or call from related manager')
		if save:
			user.verified_person=True
			user.save(update_fields=['verified_person'])
		return user.is_verified_person

class Profile(AbstractUser,UserEmailConfirmation,UserMobileConfirmation):
	#user = get_user_model()
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	#email = models.CharField(max_length=255, blank=True, null=True)
	mobile = PhoneNumberField(null=False,default='+201005866658')
	shopname = models.SlugField(max_length=50, default='ftrina-store' )
	#photo = models.ImageField(upload_to= 'pic_folder/',default = '/static/img/default_picture.png',blank=True,null=True)
	#photo = models.URLField(max_length=200,default = "https://res.cloudinary.com/ftrina/image/upload/v1469046333/default_user_avatar_ljpbex.png" )
	photo_public_id = models.CharField( max_length=256,blank=True, null=True, default = "default_user_avatar_ljpbex")
	shop_created = models.BooleanField(default=False)
	stripe_customer_id = models.CharField( max_length=256,blank=True, null=True)

	about_me = models.TextField(blank=True, null=True)
	website_url = models.TextField(blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=1, choices=(('m', 'Male'), ('f', 'Female')), blank=True, null=True)
	profile_language = models.CharField(max_length=10, choices=(('arabic', 'Arabic'), ('english', 'English'), ('chinese', 'Chinese'),('french','French')), blank=True, null=True)

	verified = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	mobile_verified = models.BooleanField(default=False)
	premium = models.BooleanField(default=False)
	verified_business= models.BooleanField(default=False)
	verified_person = models.BooleanField(default=False)
	vendor = models.BooleanField(default=False)
	shipper = models.BooleanField(default=False)
	expires_at = models.DateTimeField(blank=True, null=True)
	preferred_language = models.CharField(max_length=7,choices=(('ar', 'Arabic'), ('en', 'English'), ('zh-hans', 'Chinese'),('fr','French')),blank=False, null=False,default='en')

	citi = models.BooleanField(default=False)
	
	# facebook Profile information 
	blog_url = models.TextField(blank=True, null=True)
	access_token = models.TextField(blank=True, help_text='Facebook token for offline access', null=True)	
	raw_data = models.TextField(blank=True, null=True)
	facebook_profile_url = models.TextField(blank=True, null=True)
	facebook_name = models.CharField(max_length=255, blank=True, null=True)
	facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
	# the field which controls if we are sharing to facebook
	facebook_open_graph = models.NullBooleanField(help_text='Determines if this user want to share via open graph')
	# set to true if we require a new access token
	new_token_required = models.BooleanField(default=False,help_text='Set to true if the access token is outdated or lacks permissions')


	objects = ProfileManager()

	def __unicode__(self):
		return self.username
		#return str(self.username)

	@property
	def is_verified(self):
		return self.verified is not False

	@property
	def is_premium(self):
		return self.premium is not False

	@property
	def is_verified_business(self):
		return self.verified_business is not False

	@property
	def is_verified_person(self):
		return self.verified_person is not False

	@property
	def profile_expires_in(self):
		expires_in = timezone.now() - self.expires_at
		foo = str(expires_in)
		foo = foo.split(',')[0]
		foo = foo.split(' ')[0]
		foo = int(foo)
		foo = abs(foo)

		return foo

	@property
	def is_expired(self):
		return timezone.now() >= self.expires_at

	@property
	def is_preferred_language(self):
		return self.preferred_language is not False

	@property
	def is_vendor(self):
		return self.vendor is not False	

	@property
	def is_shipper(self):
		return self.shipper is not False

	@property
	def xmpp(self):
		return self.username + "@ftrina.com"

	def get_avatar(self):
		from album.models import Image
		from django.conf import settings

		try:
			image = Image.objects.get(profile=self.id,profile_avatar=True)
		except Image.DoesNotExist:
			return getattr(settings, "DEFAULT_USERS_AVATARE", None)

		image = Image.objects.get(profile=self.id,profile_avatar=True)
		return image.secure_url
	@property
	def is_seller(self):
		from shop.models import Seller
		try:
			seller = Seller.objects.filter(profile=self)
		except Seller.DoesNotExist:
			return False
		return True
	@property
	def seller_for(self):
		from shop.models import Seller
		shops = Seller.objects.filter(profile=self)
		data = []
		for seller in shops:
			data.append({ "name":seller.shop.name, "slug": seller.shop.slug })
		return data

	@property
	def shop_url(self):
		return self.shop_set.get().url()


class Address (models.Model):
	id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	profile  = models.ForeignKey("Profile")
	name     = models.CharField(max_length=55,null=True,blank=True)

	country  = models.CharField(max_length=13,null=True,blank=True)
	province = models.CharField(max_length=55,null=True,blank=True)
	city     = models.CharField(max_length=55,null=True,blank=True)
	zip_code = models.CharField(max_length=20,null=True,blank=True)

	address  = models.CharField(max_length=250,null=True,blank=True)
	geom     = PointField(srid=4326,blank=True,default='POINT(0.0 0.0)',null=True)

	def __unicode__(self): 
		#print 'call user Address unicode'
		return str(self.name)

	@property
	def ship_to(self):
		data = []
		data.append({
			"contact_name": self.profile.get_full_name(),
			"phone": self.profile.mobile.as_national,
			"email": self.profile.email,
			"street1": self.address,
			"city": self.city,
			"postal_code": self.zip_code,
			"state": self.province,
			"country": self.country,
			"type": "residential"
			},)
		return data



'''  useless '''
class Session(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)    




#Create  our user object to attache to our profile object
#def create_profile_user_callback(sender, instance, **kwargs):
#	profile,  new = Profile.objects.get_or_create(user=instance)
#post_save.connect(create_profile_user_callback, User)




# Create your models here.
