from __future__ import unicode_literals

from django.db import models
#from shop.models import Order
from django.utils.translation import ugettext_lazy as _
from profile.models import Profile
import uuid
import json
from django.contrib.sessions.models import Session


class Buyer(models.Model):
	id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name      = models.CharField(max_length=255, blank=True, null=True)
	last_name       = models.CharField(max_length=255, blank=True, null=True)
	email           = models.CharField(max_length=255, blank=True, null=True)
	mobile          = models.CharField(max_length=255, blank=True, null=True)
	address         = models.TextField(blank=True, null=True)
	city            = models.CharField(max_length=255, blank=True, null=True)
	zip_code        = models.CharField(max_length=255, blank=True, null=True)
	country         = models.CharField(max_length=3, blank=True, null=True)
	province        = models.CharField(max_length=255, blank=True, null=True)
	notes           = models.TextField(blank=True, null=True)

	def __unicode__(self): 
		return str(self.id)

class Seller(models.Model):
	id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name      = models.CharField(max_length=255, blank=True, null=True)
	last_name       = models.CharField(max_length=255, blank=True, null=True)
	email           = models.CharField(max_length=255, blank=True, null=True)
	mobile          = models.CharField(max_length=255, blank=True, null=True)
	address         = models.TextField(blank=True, null=True)
	city            = models.CharField(max_length=255, blank=True, null=True)
	zip_code        = models.CharField(max_length=255, blank=True, null=True)
	country         = models.CharField(max_length=3, blank=True, null=True)
	province        = models.CharField(max_length=255, blank=True, null=True)


	def __unicode__(self): 
		return str(self.id)

class Checkout(models.Model):
	id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name      = models.CharField(max_length=255, blank=True, null=True)
	last_name       = models.CharField(max_length=255, blank=True, null=True)

	email           = models.CharField(max_length=255, blank=True, null=True)
	mobile          = models.CharField(max_length=255, blank=True, null=True)

	address         = models.TextField(blank=True, null=True)
	city            = models.CharField(max_length=255, blank=True, null=True)

	zip_code        = models.CharField(max_length=255, blank=True, null=True)
	country         = models.CharField(max_length=3, blank=True, null=True)
	province        = models.CharField(max_length=255, blank=True, null=True)
	notes           = models.TextField(blank=True, null=True)
	session         = models.ForeignKey(Session,default='261bj1xhw9qxb0wpc3hkr1x9ozudc02a')

	customs_info    = models.CharField(max_length=255, blank=True, null=True)

	shipment_id        = models.CharField(max_length=255, blank=True, null=True)
	rate_id            = models.CharField(max_length=255, blank=True, null=True)
	currency           = models.CharField(max_length=255, blank=True, null=True)
	rate               = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2,default=0.00)
	carrier            = models.CharField(max_length=55,null=True,blank=True)

	status             = models.BooleanField(default=False)
	stripe_customer_id = models.CharField( max_length=256,blank=True, null=True)

	def __unicode__(self): 
		return str(self.id)
	@property
	def ship_to(self):
		data = {
		"name": str( self.first_name + ' ' + self.last_name )  ,
		"street1": self.address,
		"city": self.city,
		"state": self.province,
		"zip": self.zip_code,
		"country": self.country,
		"phone": self.mobile,
		"email": self.email,
		#"type": "residential"
		}
		return data

# Create your models here.
class BasketManager(models.Manager):
	pass

class Basket(models.Model):
	id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	owner                   = models.ForeignKey(Profile, null=True, blank=True) # The Profile Who own this Basket
	session                 = models.ForeignKey(Session,default='261bj1xhw9qxb0wpc3hkr1x9ozudc02a')  
	usd                     = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2,default=0.00)
	shipment_price          = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2,default=0.00)
	shipment_price_currency = models.CharField(max_length=55,null=True,blank=True)
	objects = BasketManager()


	''' Customs item for easypost api '''
	@property
	def customs_item(self):
		data = []
		orders = self.order_set.all().filter(status=False)
		for order in orders:
			data.append({
				"description": order.product.cart_description,
				"quantity": order.quantity,
				"value":  float( self.sub_total_price(order) ), # total price (unit price * quantity)
				"currency": order.product.price_currency,
				"weight": self.customs_weight(float(order.product.weight)), # in oz
				"hs_tariff_number":None,
				"code":order.product.sku,
				"origin_country":order.product.origin,
				},)
		return data

	''' Convert Grams to Ounces'''
	def customs_weight(self,weight):
		oz = weight * 1/28.34952313
		return oz
	''' calculate unit price and add the variant price '''
	def unit_price(self,order):
		if order.product:
			price = order.product.usd_price
			if order.with_option:
				options = order.option_set.all()
				for option in options:
					price = price + option.usd_price
		return price
	''' calculate total order price price and add the quantity '''
	def sub_total_price(self,order):
		if order.product:
			price = order.product.usd_price * order.quantity
			if order.with_option:
				options = order.option_set.all()
				for option in options:
					price = price + option.usd_price
		return price

	''' Basket Total weight in Grams '''
	@property
	def weight(self):
		data = []
		orders = self.order_set.all().filter(status=False)
		weight = 0
		for order in orders:
			order_weight = order.product.weight * order.quantity
			weight = weight + order_weight
		return weight

	''' parcels for easypost api, we can Choose the parcels Box here '''
	@property
	def parcels(self):
		data = []
		if self.weight < 600:
			parcel= { "weight": self.customs_weight( float(self.weight) ),"length": 27 * 0.39,"width": 35 * 0.39 ,"height": 2 * 0.39  }      #Up to 0.5kg
			return parcel

		if self.weight < 1000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 33 * 0.39 ,"width": 16 * 0.39 , "height": 10 * 0.39 }     #Up to 1kg Conferm

			return parcel
		if self.weight < 1500:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 34 * 0.39,  "width": 31 * 0.39, "height": 10 * 0.39 }     #Up to 1.5kg Conferm
			return parcel

		if self.weight < 2000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 33 * 0.39 ,  "width": 33 * 0.39 , "height": 9.5 * 0.39  }  #Up to 2kg Conferm
			return parcel

		if self.weight < 3000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 33 * 0.39  ,  "width": 33 * 0.39  , "height": 14 * 0.39 }   #Up to 3kg Conferm
			return parcel

		if self.weight < 4000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 33 * 0.39   ,  "width": 33 * 0.39  , "height": 18.5 * 0.39 } #Up to 4kg Conferm
			return parcel

		if self.weight < 5000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 35 * 0.39   ,  "width": 33 * 0.39  , "height": 22 * 0.39 } #Up to 5kg Conferm
			return parcel

		if self.weight < 7000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 34 * 0.39 ,  "width": 32 * 0.39, "height": 32.5 * 0.39 } #Up to 7kg Conferm
			return parcel

		if self.weight < 12000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 42 * 0.39 ,  "width": 36 * 0.39 , "height": 37 * 0.39 } #Up to 12kg Conferm
			return parcel

		if self.weight < 18000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 45 * 0.39 ,  "width": 36 * 0.39 , "height": 37 * 0.39 } #Up to 18kg
			return parcel

		if self.weight < 25000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 54.8 * 0.39 ,  "width": 42.1 * 0.39 , "height": 33.5 * 0.39  } #Up to 25kg
			return parcel

		if self.weight < 150000:
			parcel= { "weight": self.customs_weight( float(self.weight) ), "length": 120 * 0.39 ,  "width": 80 * 0.39 , "height": 80 * 0.39  } #Up to 25kg
			return parcel

	''' Change the Basket price to zero before start calculation '''
	def zero_fill_currency(self):
		self.usd   = 0
		self.save()
		return
	''' Get orders List and calculate the total price '''
	@property
	def get_orders(self):
		orders = self.order_set.all().filter(status=False)
		data = []
		self.zero_fill_currency()
		for order in orders:
			if order.coupon:
				descent   = order.coupon.rate
			else:
				descent   = None

			if order.product:
				options = []
				if order.with_option:
					options_list = order.option_set.all()
					for o in options_list:
						options.append({
							'name': str(o.name),
							'value': str(o.value),
							'price': str(o.usd_price),
							})

				data.append({
					'order_id': str(order.id),
					'product': {
					'id': str(order.product.id),
					'shop_id':str(order.product.shop.id),
					'main_image': order.product.image,
					'name':order.product.name,
					'quantity':order.quantity,
					'total_price':self.sub_total_price(order),# total price (unit price * quantity)
					'price': self.unit_price(order),
					'price_currency': 'USD',
					#'price_currency': order.product.price_currency,
					'classification':'product',
					'descent':descent,
					'max_value': order.max_quantity,
					'url':order.product.url,
					'with_option':order.with_option,
					},
					'options':options,
					})
				self.total_price(currency = "USD" , price = order.product.usd_price , order = order )
		return data

	''' Basket Total Price '''
	def total_price(self,currency,price, order):
		quantity = order.quantity
		coupon   = order.coupon
		total    = price * quantity
		if coupon:
			after_discount = total - (total/100 * coupon.rate )
		else:
			after_discount = total
		final = after_discount
		if currency == "USD":
			total = price * quantity
			self.usd = self.usd + final
		if order.with_option:
			options = order.option_set.all()
			for option in options:
				self.usd = self.usd + option.usd_price
		self.save()
		return 

'''
	def get_currency(self):
		currency = self.order.product.price_currency
		return currency
'''




