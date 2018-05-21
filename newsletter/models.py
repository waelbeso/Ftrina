# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import uuid


# Create your models here.

class Subscribers(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	date         = models.DateTimeField(default=timezone.now,auto_now=False,blank=True)
	email        = models.CharField(max_length=55,default='wael@rojx.com' , blank=True, null=True)
	def __unicode__(self): 
		return self.email
