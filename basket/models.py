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

	shipper_account = models.CharField(max_length=255, blank=True, null=True)
	service_type    = models.CharField(max_length=255, blank=True, null=True)
	service_name    = models.CharField(max_length=255, blank=True, null=True)
	shipment_price  = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=2,default=0.00)
	shipment_price_currency = models.CharField(max_length=55,null=True,blank=True)


	status        = models.BooleanField(default=False)

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

	@property
	def items(self):
		data = []
		orders = self.order_set.all().filter(status=False)
		for order in orders:
			data.append({
				"description": order.product.cart_description,
				"origin_country": order.product.origin,
				"quantity": order.quantity,
				"price": {
				"amount": float( self.get_price(order) ),
				"currency": order.product.price_currency
				},
				"weight": {
				"value":  float(order.product.weight),
				"unit": "g"
				},
				"sku": order.product.sku
				},)
		return data
	@property
	def weight(self):
		data = []
		orders = self.order_set.all().filter(status=False)
		weight = 0
		for order in orders:
			order_weight = order.product.weight * order.quantity
			weight = weight + order_weight
		return weight

	@property
	def parcels(self):
		data = []
		if self.weight < 600:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 0.5,
					"unit": "kg"
					},
				"dimension": {
				"width": 35,
				"height": 27.5,
				"depth": 1,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 1000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 1 ,
					"unit": "kg"
					},
				"dimension": {
				"width": 18.2,
				"height": 33.7,
				"depth": 10,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 2000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 2,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 10,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 5000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 5,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 18,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data
		if self.weight < 10000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 10,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 34.5,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data
		if self.weight < 20000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 20,
					"unit": "kg"
					},
				"dimension": {
				"width": 40.4,
				"height": 48.1,
				"depth": 38.9,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data
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
							'price': str(o.price),
							})

				data.append({
					'order_id': str(order.id),
					'product': {
					'id': str(order.product.id),
					'shop_id':str(order.product.shop.id),
					'main_image': order.product.image,
					'name':order.product.name,
					'quantity':order.quantity,
					'total_price':self.get_price(order),
					'price': self.unit_price(order),
					'price_currency': order.product.price_currency,
					'classification':'product',
					'descent':descent,
					'max_value': order.max_quantity,
					'url':order.product.url,
					'with_option':order.with_option,
					},
					'options':options,
					})
				self.calculat(currency = order.product.price_currency , price = order.product.price ,order = order )
		return data


	def unit_price(self,order):
		if order.product:
			price = order.product.price
			if order.with_option:
				options = order.option_set.all()
				for option in options:
					price = price + option.price
		return price

	def get_price(self,order):
		if order.product:
			price = order.product.price * order.quantity
			if order.with_option:
				options = order.option_set.all()
				for option in options:
					price = price + option.price
		return price

	def calculat(self,currency,price, order):

		quantity = order.quantity
		coupon   = order.coupon
		total = price * quantity

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
				self.usd = self.usd + option.price
		self.save()
		return 

	def get_currency(self):
		currency = self.order.product.price_currency
		return currency

	def zero_fill_currency(self):
		self.usd   = 0
		self.save()
		return



