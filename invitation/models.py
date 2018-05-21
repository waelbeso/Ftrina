from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Invitation(models.Model):
	firstname = models.CharField(max_length=55,default='Name')
	email = models.EmailField(max_length=55,default='email')
	language = models.CharField(max_length=10,default='english')
	inviter = models.BooleanField(max_length=55,default='wael')
	status = models.BooleanField(default=False)


	def __unicode__(self): 
		return self.name


