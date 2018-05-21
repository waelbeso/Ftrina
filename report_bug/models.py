from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bug(models.Model):
	user = models.CharField(max_length=55,default='Name')
	message = models.TextField(max_length=1000,default='message')
	img = models.URLField(max_length=100,null=True)
	email = models.EmailField(max_length=55,default='email')



	def __unicode__(self): 
		return self.user