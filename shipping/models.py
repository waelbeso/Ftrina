from __future__ import unicode_literals

from django.db import models

from shop.models import Shop,WareHouse
import uuid
# Create your models here.



class Model(models.Model):
	''' Shipping Model '''
	id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name          = models.CharField(max_length=55,null=True,blank=True)
	shop          = models.ForeignKey(Shop,on_delete=models.CASCADE, null=True,blank=True)
	ware_house    = models.ForeignKey(WareHouse,on_delete=models.CASCADE, null=True,blank=True)

	class Meta:
		unique_together = ['name', 'shop']

	def __unicode__(self): 
		return '{} <{}>'.format(self.name, self.shop)

	def zone(self):
		zones = self.zone_set.filter(model=self)
		data = []
		for zone in zones:
			data.append({
				'id':zone.id,
				'country': zone.country,
				'province': zone.province,
				'price': zone.price,
				'price_currency': zone.price_currency,
				})
		return data


class Zone(models.Model):
	''' Shipping Zone '''
	id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	shop                 = models.ForeignKey(Shop,on_delete=models.CASCADE, null=True,blank=True)
	model                = models.ForeignKey("Model", null=True,blank=True, on_delete=models.CASCADE)
	country              = models.CharField(max_length=13,null=True,blank=True)
	province             = models.CharField(max_length=55,null=True,blank=True)
	price                = models.DecimalField(null=True,blank=True, max_digits=19, decimal_places=3)
	price_currency       = models.CharField(max_length=55,null=True,blank=True)


	class Meta:
		unique_together = ['model', 'country','province']

	def __unicode__(self): 
		return '<{}> {} <{}>'.format(self.model,self.country, self.province)

	def model_id(self):
		return str(self.model.id)

	def to_dict(self):

		return {
		'model': self.model,
		'country': self.country,
		'province': self.province,
		'price': self.price,
		'price_currency': self.price_currency,
        }
