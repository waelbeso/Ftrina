from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings

import uuid
from profile.models import Profile

from django.contrib.auth import get_user_model


# Create your models here.

class Message(models.Model):
	id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	message_from  = models.ForeignKey(Profile,null=True,blank=True,related_name = "from+" )
	message_to    = models.ForeignKey(Profile,null=True,blank=True,related_name = "to+"   )
	status        = models.BooleanField(default=False)
	send_at       = models.DateTimeField(default=timezone.now,auto_now=False,blank=True)
	text          = models.CharField(max_length=255, blank=True, null=True)
	conversation  = models.ForeignKey('Conversation',blank=True, null=True,related_name = "Conversation+"   )

	def __unicode__(self): 
		print 'call message unicode'
		return '{} <{}>'.format(self.message_from, self.message_to)

	@property
	def _from(self):
		return self.message_from.username

	@property
	def _to(self):
		return self.message_to.username

class Conversation(models.Model):

	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	audience     = models.ManyToManyField(Profile)

	def __unicode__(self): 
		print 'call conversation unicode'
		return str(self.id)








