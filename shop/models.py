#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save
from django_countries.fields import CountryField

from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField

#from django_pgjson.fields import JsonField
from django.contrib.postgres.fields import JSONField as JsonField
from profile.models import Profile,Address
import uuid
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import smart_str, smart_unicode

from basket.models import Basket,Checkout
from django.contrib.sessions.models import Session
import json

from datetime import date, timedelta


class WareHouse (models.Model):
	id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop     = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True)
	name     = models.CharField(max_length=55,null=True,blank=True)
	country  = models.CharField(max_length=13,null=True,blank=True)
	province = models.CharField(max_length=55,null=True,blank=True)
	city     = models.CharField(max_length=55,null=True,blank=True)
	zip_code = models.CharField(max_length=20,null=True,blank=True)
	address  = models.CharField(max_length=250,null=True,blank=True)
	geom     = models.PointField(srid=4326,blank=True,default='POINT(0.0 0.0)',null=True)
	default  = models.BooleanField(default=False)

	class Meta:
		unique_together = ('shop', 'name')
	def __unicode__(self): 
		return self.name

	@property
	def ship_from(self):
		data = {
		"name": self.shop.name,
		"street1": self.address,
		"street2": None,
		"city": self.city,
		"state": self.province,
		"zip": self.zip_code,
		"country": self.country,
		"phone": self.shop.default_contact.mobile.as_international,
		"email": self.shop.default_contact.email,
		}
		return data
class Branch(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop         = models.ForeignKey("Shop",on_delete=models.CASCADE, null=True,blank=True)
	name         = models.CharField(max_length=55,null=True,blank=True)
	phone        = PhoneNumberField(null=False,default='+201005866658')
	country      = models.CharField(max_length=13,null=True,blank=True)
	province     = models.CharField(max_length=55,null=True,blank=True)
	city         = models.CharField(max_length=55,null=True,blank=True)
	zip_code     = models.CharField(max_length=20,null=True,blank=True)

	address      = models.CharField(max_length=250,null=True,blank=True)
	geom         = models.PointField(srid=4326,blank=True,default='POINT(0.0 0.0)',null=True)


	def __unicode__(self): 
		#print 'call Branch unicode'
		return '{} <{}>'.format(self.name, self.shop)

class Coverage (models.Model):
	id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop     = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True)
	name     = models.CharField(max_length=55,null=True,blank=True)
	country  = models.CharField(max_length=13,null=True,blank=True)
	province = models.CharField(max_length=55,null=True,blank=True)
	city     = models.CharField(max_length=55,null=True,blank=True)
	geom     = models.PolygonField(null=True,blank=True)

	def __unicode__(self): 
		#print 'call coverage unicode'
		return '{} <{}>'.format(self.name, self.shop)
class Variant(models.Model):
	id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product              = models.ForeignKey("Product", on_delete=models.CASCADE, null=True,blank=True)
	name                 = models.CharField(max_length=55,null=True,blank=True)
	price                = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	value                = models.CharField(max_length=100,null=True,blank=True)#
	def __unicode__(self): 
		return self.value
class Product(models.Model):
	id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#auto
	name                 = models.TextField(max_length=64,null=True,blank=True)#
	shop                 = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True) #auto
	description          = models.TextField(default='new',null=True,blank=False) #
	cart_description     = models.CharField(max_length=255,null=True,blank=True)#
	min_order            = models.IntegerField(default=1, blank=True, null=True) # auto
	price                = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	price_currency       = models.CharField(max_length=55,null=True,blank=True)
	weight               = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	list_as              = models.CharField(default='new', max_length=55,null=True,blank=True)# auto
	language             = models.CharField(max_length=55,null=True,blank=True)# auto
	origin               = models.CharField(max_length=55,null=True,blank=True,default='EG')
	sku                  = models.CharField(max_length=55,null=True,blank=True) # Stock Keeping Unit
	keywords             = models.CharField(max_length=100,null=True,blank=True)#
	with_variant         = models.BooleanField(default=False)
	characteristics      = JsonField(null=True,blank=True) # can pass attributes like null, blank, ecc.
	created_date         = models.DateTimeField(default=timezone.now,auto_now=False,blank=True) # at witch time

	def __unicode__(self): 
		return '{} <{}>'.format(self.name, self.shop) #http://www.saltycrane.com/blog/2008/11/python-unicodeencodeerror-ascii-codec-cant-encode-character/
	''' get product slug '''
	@property
	def slug(self):
		return self.name.replace (" ", "-")
	''' get main image for search result '''
	@property
	def image(self):
		return self.images.first().secure_url
	''' For Search Result '''
	@property
	def url(self):
		from django.conf import settings
		site = getattr(settings, "WEBSITE_URL", None)
		return str(site) + str(self.shop.slug) + "/" + self.slug
	''' For Search Result '''
	@property
	def followers(self):
		from django.contrib.contenttypes.models import ContentType
		from activity.models import is_following,followers 
		actor = ContentType.objects.get(app_label="shop", model="shop")
		total_followers = len( followers( actor=actor,actor_slug=self.shop.slug) )
		return total_followers
	''' For Search Result '''
	@property
	def rating(self):
		from django.contrib.contenttypes.models import ContentType
		from ratings.models import Rating
		object_id = self.id
		content_type = ContentType.objects.get(model="product")
		instance =  content_type.get_object_for_this_type(pk=object_id)
		rating_for = Rating.objects.for_instance(instance)
		return rating_for.to_dict()
	''' For Search Result '''
	@property
	def orders(self):
		orders = len(self.order_set.all())
		return orders
	''' Product Availability '''
	@property
	def availability(self):
		inventory = self.inventory_set.all()
		availability = False
		quantity = 0
		for o in inventory:
			if o.quantity > 0 :
				if o.warehouse.courier_set.all():
					quantity = quantity + o.quantity
					availability = True
		return { "available": availability, "quantity":quantity }

	''' Ready for shipping if we find courier from the  Product warehouse '''
	@property
	def ready(self):
		inventory = self.inventory_set.all()
		ready = False
		quantity = 0
		for o in inventory:
			if o.quantity > 0 :
				if o.warehouse.courier_set.all():
					ready = True
		return ready

	''' Ready for shipping if we find courier from the  Product warehouse '''
	@property
	def option(self):
		variant_list  = self.variant_set.all()
		variant = []
		variant_dict = {}
		for o in variant_list:
			variant_dict[o.name] = []
		for o in variant_list:
			variant_dict[o.name].append(  ( str(o.id) , str(o.value) + ' + ' + str(o.price) ) )
			#variant_dict[o.name].append( {  "id":o.id, "name":o.name, "value": o.value, "price":int(o.price)   } )
		for i in variant_dict:
			variant.append( { "name":i,"value":variant_dict[i]  } )
		return variant

class Collection(models.Model):
	id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop           = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True)
	name           = models.CharField(max_length=55,null=True,blank=True)
	keywords       = models.CharField(max_length=100,null=True,blank=True)
	language       = models.TextField(max_length=20, choices=(('Arabic', 'Arabic'), ('English', 'English'), ('Chinese', 'Chinese')), blank=True, null=True)
	products       = models.ManyToManyField(Product)
	created_date   = models.DateTimeField(default=timezone.now,auto_now=False,blank=True) # at witch time

	def __unicode__(self): 
		return self.name
	@property
	def slug(self):
		return self.name.replace (" ", "-")
	''' For Search Result '''
	@property
	def url(self):
		from django.conf import settings
		site = getattr(settings, "WEBSITE_URL", None)
		return str(site) + str(self.shop.slug) + "/" + self.slug + "/"
	''' For Search Result '''
	@property
	def image(self):
		from album.models import Image
		from django.conf import settings
		try:
			logo = Image.objects.get(shop=self.shop.id,is_logo=True)
		except Image.DoesNotExist:
			return getattr(settings, "DEFAULT_SHOP_LOGO", None)
		logo = Image.objects.get(shop=self.shop.id,is_logo=True)
		return logo.secure_url
	''' For Search Result '''
	@property
	def followers(self):
		from django.contrib.contenttypes.models import ContentType
		from activity.models import is_following,followers 
		actor = ContentType.objects.get(app_label="shop", model="shop")
		total_followers = len( followers( actor=actor,actor_slug=self.shop.slug) )
		return total_followers
	''' For Search Result '''
	@property
	def rating(self):
		from django.contrib.contenttypes.models import ContentType
		from ratings.models import Rating
		object_id = self.shop.id
		content_type = ContentType.objects.get(model="shop")
		instance =  content_type.get_object_for_this_type(pk=object_id)
		rating_for = Rating.objects.for_instance(instance)
		return rating_for.to_dict()
	''' For Search Result '''
	@property
	def orders(self):
		orders = len(self.shop.order_set.all())
		return orders
	''' For Search Result '''
	@property
	def collection(self):
		return True



class ShopManager(models.Manager):

    def go_live(self, shop=None, save=False):
        "Change shop status to live"
        shop = shop or getattr(self, 'instance', None)
        if not user:
        	raise ValueError('Must specify shop or call from related manager')
        if save:
        	shop.live = True
        	shop.save(update_fields=['live'])
        return shop.is_live

class Shop(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	owner        = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
	name         = models.CharField(max_length=55,null=True,blank=True)
	slug         = models.SlugField(max_length=50,blank=True, unique=True, null=True)
	specialty    = models.CharField(max_length=200,null=True,blank=True)
	keywords     = models.CharField(max_length=200,null=True,blank=True)
	description  = models.TextField(null=True,blank=True)
	language     = models.TextField(max_length=1, choices=(('Arabic', 'Arabic'), ('English', 'English'), ('Chinese', 'Chinese'),('French','French')), blank=True, null=True)
	legalform    = models.CharField(max_length=100,null=True,blank=True)
	employees    = models.CharField(max_length=255,null=True,blank=True)
	activite     = models.TextField(max_length=50, choices=(('import', 'Import'), ('export', 'Export'), ('manufacturing', 'Manufacturing'), ('servisess', 'Servisess'), ('shipping', 'Shipping')), blank=True, null=True)
	areas        = models.CharField(max_length=200,null=True,blank=True)

	live         = models.BooleanField(default=False)
	featured     = models.BooleanField(default=False)
	status       = models.TextField(max_length=1, default='Test', choices=(('Active', 'Active'), ('Test', 'Test')))
	country      = models.CharField(max_length=3,null=True,blank=True)
	province     = models.CharField(max_length=200,null=True,blank=True)
	city         = models.CharField(max_length=55,null=True,blank=True)
	address      = models.CharField(max_length=200,null=True,blank=True)
	zip_code     = models.CharField(max_length=20,null=True,blank=True)
	geom         = models.PointField(srid=4326,blank=True,default='POINT(0.0 0.0)',null=True)
	created_date = models.DateTimeField(default=timezone.now,auto_now=False,blank=True) # at witch time
	currency     = models.CharField(max_length=55,null=True,blank=True)#Default Currency
	objects = ShopManager()

	def __unicode__(self): 
		return self.slug

	''' Shop Default Contact '''
	@property
	def default_contact(self):
		return self.contact_set.get(default=True)
	''' Shop Default Warehouse '''
	@property
	def default_warehouse(self):
		return self.warehouse_set.get(default=True)
	''' Shop Default Currency '''
	@property
	def default_currency(self):
		return self.currency
	''' Shop Default Language '''
	@property
	def default_language(self):
		return self.language
	''' Shop URL '''
	@property
	def url(self):
		from django.conf import settings
		site = getattr(settings, "WEBSITE_URL", None)
		return str(site) + self.slug
	''' Shop owner username '''
	def shop_username(self):
		return self.owner
	''' if the user is the shop owner '''
	def is_shop_owner(self,user):
		if self.owner == user:
			return True
		if not self.owner == user:
			return False
	''' if shop is Live '''
	@property
	def is_live(self):
		return self.live is not False
	''' Get shop logo '''
	@property
	def image(self):
		from album.models import Image
		from django.conf import settings
		try:
			logo = Image.objects.get(shop=self.id,is_logo=True)
		except Image.DoesNotExist:
			return getattr(settings, "DEFAULT_SHOP_LOGO", None)
		logo = Image.objects.get(shop=self.id,is_logo=True)
		return logo.secure_url
	''' Get shop banner '''
	@property
	def banner(self):
		from album.models import Image
		from django.conf import settings
		try:
			banner = Image.objects.get(shop=self.id,is_banner=True)
		except Image.DoesNotExist:
			return getattr(settings, "DEFAULT_SHOP_BANNER", None)
		banner = Image.objects.get(shop=self.id,is_banner=True)
		return banner.secure_url
	''' Get shop total follower for search results rendering and home page'''
	@property
	def followers(self):
		from django.contrib.contenttypes.models import ContentType
		from activity.models import is_following,followers 
		actor = ContentType.objects.get(app_label="shop", model="shop")
		total_followers = len( followers( actor=actor,actor_slug=self.slug) )
		return total_followers
	''' Get shop shop rating for search results rendering and home page '''
	@property
	def rating(self):
		from django.contrib.contenttypes.models import ContentType
		from ratings.models import Rating
		object_id = self.id
		content_type = ContentType.objects.get(model="shop")
		instance =  content_type.get_object_for_this_type(pk=object_id)
		rating_for = Rating.objects.for_instance(instance)
		return rating_for.to_dict()
	''' Get shop total orders for search results rendering and home page '''
	@property
	def orders(self):
		orders = len(self.order_set.all())
		return orders
	''' For Search Results Rendering '''
	@property
	def collection(self):
		return True
	''' For shop home page Rendering '''
	@property
	def have_offers(self):
		products = Product.objects.filter(shop=self,list_as='offer')
		if len(products) > 0 :
			return True
		return False
	''' shop orders this year For the chart '''
	@property
	def orders_this_year(self):
		today       = timezone.now().date()
		this_year = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
		orders_this_year = self.order_set.filter(timestamp__year=today.year)
		for o in orders_this_year:
			this_year[o.timestamp.month-1] = this_year[o.timestamp.month-1] + 1
		return this_year

	''' shop orders this month For the chart '''
	@property
	def orders_this_month(self):
		today       = timezone.now().date()
		this_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		orders_this_month = self.order_set.filter(timestamp__year=today.year,timestamp__month=today.month)
		for o in orders_this_month:
			this_month[o.timestamp.day-1] = this_month[o.timestamp.day-1] + 1
		return this_month
	''' shop orders today For the chart '''
	@property
	def orders_today(self):
		today       = timezone.now().date()
		this_day = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
		orders_this_day = self.order_set.filter(timestamp__year=today.year,timestamp__month=today.month,timestamp__day=today.day)
		for o in orders_this_day:
			print o.timestamp.time().hour
			this_day[o.timestamp.time().hour-1] = this_day[o.timestamp.time().hour-1] + 1
		return this_day
	''' For shop statistics in dashboard '''
	@property
	def statistics(self):
		new      = self.invoice_set.filter(finished=False).count()
		archived = self.invoice_set.filter(finished=True).count()
		expected = self.order_set.filter(finished=False,status=False).count()
		customer = self.customer_set.all().count()
		return {"new":new,"archived":archived,"expected":expected,"customer":customer}
	''' For shop home page Rendering '''
	@property
	def have_new(self):
		products = Product.objects.filter(shop=self,list_as='new')
		if len(products) > 0 :
			return True
		return False

	''' For shop home page Rendering '''
	def new(self):
		from album.models import Image
		products = Product.objects.filter(shop=self,list_as='new')
		data = []
		for product in products:
			data.append({
				'id': str(product.id),
				'main_image': product.image,
				'name':product.name,
				'slug':product.slug,
				'origin':product.origin,
				'min':str(product.min_order),
				'price':str(product.price),
				'price_currency':product.price_currency,
				'shop':product.shop.slug,
				'shop_id':product.shop.id,
				'language':product.language,
				'rating':product.rating,
				'orders':product.orders,
				'url':str(product.url),
				})
		return data
	''' For shop home page Rendering '''
	def offers(self):
		from album.models import Image
		products = Product.objects.filter(shop=self,list_as='offer')
		data = []
		for product in products:
			data.append({
				'id': str(product.id),
				'main_image': product.image,
				'name':product.name,
				'slug':product.name.slug,
				'origin':product.origin,
				'min':product.origin,
				'price':str(product.price),
				'price_currency':product.price_currency,
				'shop':product.shop.slug,
				'shop_id':product.shop.id,
				'language':product.language,
				'classification':'product',
				'rating':product.rating,
				'orders':product.orders,
				'url':str(product.url) 
				})
		return data

class Customer(models.Model):
	id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=255, blank=True, null=True)
	last_name  = models.CharField(max_length=255, blank=True, null=True)
	email      = models.CharField(max_length=255, blank=True, null=True)
	mobile     = models.CharField(max_length=255, blank=True, null=True)
	country    = models.CharField(max_length=3, blank=True, null=True)
	shop       = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True) #auto
	orders     = models.IntegerField(blank=True, null=True)
	
	def __unicode__(self): 
		return str(self.id)

	''' if shop is Live '''
	@property
	def name(self):
		return self.first_name + " " + self.last_name

class Courier(models.Model):
	id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name           = models.CharField(max_length=255, blank=True, null=True)
	shop           = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True) #auto
	warehouse      = models.ForeignKey(WareHouse,on_delete=models.CASCADE,null=True,blank=True)
	slug           = models.CharField(max_length=255, blank=True, null=True)
	credentials    = JsonField(blank=True, null=True)
	postmen_id     = models.CharField(max_length=255, blank=True, null=True)
	easypost_id    = models.CharField(max_length=255, blank=True, null=True)

	
	def __unicode__(self): 
		return self.name

class Contact(models.Model):
	id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=255, blank=True, null=True)
	last_name  = models.CharField(max_length=255, blank=True, null=True)
	email      = models.CharField(max_length=255, blank=True, null=True)
	mobile     = PhoneNumberField(null=False,default='+201005866658')
	shop       = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True) #auto
	default    = models.BooleanField(default=False)

	def __unicode__(self): 
		return self.name

	''' if shop is Live '''
	@property
	def name(self):
		return self.first_name + " " + self.last_name


class Coupon(models.Model):
	id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name              = models.CharField(max_length=55,null=True,blank=True)
	code              = models.CharField(max_length=55,null=True,blank=True)
	user_limit        = models.PositiveIntegerField(default=1)
	valid_until       = models.DateField(blank=True, null=True)
	rate              = models.PositiveIntegerField(default=1)
	created_by        = models.ForeignKey(Profile,on_delete=models.CASCADE,)
	shop              = models.ForeignKey(Shop,on_delete=models.CASCADE,)
	created_at        = models.DateTimeField(auto_now_add=True)

	def __unicode__(self): 
		#print 'call coupon unicode'
		return '{} <{}>'.format(self.shop,self.code)

	@property
	def is_expired(self):
		import datetime
		now = datetime.datetime.now()
		foo = str(self.valid_until)
		foo = foo.split('-')

		return datetime.date(now.year,now.month,now.day) >= datetime.date(int(foo[0]),int(foo[1]),int(foo[2])) 

''' the seller is different from the shop seller model '''
from basket.models import Buyer,Seller
class Invoice(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	paid         = models.BooleanField(default=False) 
	timestamp    = models.DateTimeField(default=timezone.now,auto_now=False,blank=True) # at witch time
	buyer        = models.ForeignKey(Buyer,null=True,blank=True) # 
	seller       = models.ForeignKey(Seller,null=True,blank=True) # 
	shop         = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True)
	owner        = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
	finished     = models.BooleanField(default=False) # 
	reference    = models.UUIDField(default=uuid.uuid4, editable=False) # reference to look for the Order and to print in the invoice
	stage        = models.CharField(max_length=55,null=True,blank=True, default='pending') # pending - picked or reserved  - shipped - reserved

	def __unicode__(self): 
		return str(self.id)
	class Meta:
		ordering = ('timestamp',)
		unique_together = ("id", "reference")


# this order model is the basket items Option
class Option(models.Model):
	id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	order                = models.ForeignKey("Order", on_delete=models.CASCADE, null=True,blank=True)
	name                 = models.CharField(max_length=55,null=True,blank=True)
	price                = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	value                = models.CharField(max_length=100,null=True,blank=True)#
	def __unicode__(self): 
		return self.value

# this order model is the basket items
class Order(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	owner        = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)# whao make the Order
	invoice      = models.ForeignKey(Invoice,null=True,blank=True) # Invoice
	session      = models.ForeignKey(Session,default='261bj1xhw9qxb0wpc3hkr1x9ozudc02a')  
	shop         = models.ForeignKey(Shop,on_delete=models.CASCADE,) # From which shop
	product      = models.ForeignKey(Product,null=True,blank=True) # for witch with product
	basket       = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True,blank=True )
	quantity     = models.IntegerField(blank=True, null=True) # how many pieces of this product
	timestamp    = models.DateTimeField(auto_now=True,blank=True) # at witch time
	status       = models.BooleanField(default=False) # if the order is Ordered will change to True
	finished     = models.BooleanField(default=False) # if the order is closed will change to True
	coupon       = models.ForeignKey(Coupon,null=True,blank=True) # The coupon used in this order
	guest        = models.BooleanField(default=False) # if the order made by guest, so we did not have address relation.
	checkout     = models.ForeignKey(Checkout,null=True,blank=True) # Checkout relation.
	with_option  = models.BooleanField(default=False)# is the order incude Option
	max_quantity = models.IntegerField(blank=True, null=True) # how many is the order maximom
	warehouse    = models.ManyToManyField(WareHouse,null=True,blank=True)# From which warehouse
	def __unicode__(self): 
		#print 'call Order unicode'
		return '{} <{}>'.format(self.owner,self.product.id)
	class Meta:
		ordering = ('timestamp',)

	def registered(self):
		if self.owner is None:
			return False
		else:
			return True
	def item_info(self):
		if self.product:
			data = {
			"url":self.product.url(),
			"name":self.product.name,
			}
		return data

	@property
	def total_price(self):
		return self.product.price * self.quantity

'''
class Item(models.Model):
	id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#auto
	name                 = models.TextField(max_length=64,null=True,blank=True)#
	product              = models.ForeignKey(Product,null=True,blank=True) # for witch with product
	shop                 = models.ForeignKey("Shop", on_delete=models.CASCADE, null=True,blank=True) #auto
	description          = models.TextField(default='new',null=True,blank=False) #
	cart_description     = models.CharField(default='Product',max_length=255,null=True,blank=True)#
	min_order            = models.IntegerField(default=1, blank=True, null=True) # auto
	price                = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	price_currency       = models.CharField(max_length=55,null=True,blank=True)
	weight               = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2)
	list_as              = models.CharField(default='new', max_length=55,null=True,blank=True)# auto
	language             = models.CharField(max_length=55,null=True,blank=True)# auto
	origin               = models.CharField(max_length=55,null=True,blank=True,default='EG')
	sku                  = models.CharField(max_length=55,null=True,blank=True) # Stock Keeping Unit
	keywords             = models.CharField(max_length=100,null=True,blank=True)#
	with_variant         = models.BooleanField(default=False)
	characteristics      = JsonField(null=True,blank=True) # can pass attributes like null, blank, ecc.
	created_date         = models.DateTimeField(default=timezone.now,auto_now=False,blank=True) # at witch time

	def __unicode__(self): 
		return name 
'''
class Inventory(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop         = models.ForeignKey(Shop,on_delete=models.CASCADE,) # From which shop
	product      = models.ForeignKey(Product,null=True,blank=True) # for witch with product
	quantity     = models.IntegerField(blank=True, null=True) # how many pieces of this product
	timestamp    = models.DateTimeField(auto_now=True,blank=True) # at witch time
	variant      = models.ManyToManyField(Variant,null=True,blank=True) # for witch with product. Variant
	warehouse    = models.ForeignKey(WareHouse,null=True,blank=True) # in witch warehouse

	def __unicode__(self): 
		return self.product.name









