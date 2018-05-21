from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Future_Customer(models.Model):
	name = models.CharField(max_length=55,null=True,blank=True,default='Name')
	email = models.EmailField(max_length=55,null=True,blank=True,default='email')
	mobile = PhoneNumberField(null=True,blank=True,default='+201005866658')

	def __unicode__(self):
		return self.name