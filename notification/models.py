from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now

from django.conf import settings

import uuid
from profile.models import Profile

from django.contrib.auth import get_user_model
from django.utils.timesince import timesince as djtimesince

# Create your models here.

class Notification(models.Model):
	id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	notification_to    = models.ForeignKey(Profile,related_name = "to+"   )
	status             = models.BooleanField(default=False)
	send_at            = models.DateTimeField(default=now,auto_now=False,blank=True)
	title              = models.CharField(max_length=255, blank=True, null=True)
	message            = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self): 
		print 'call notification unicode'
		return '{} <{}>'.format(self.notification_to, self.title)

	def timesince(self, now=None):
		"""
		Shortcut for the ``django.utils.timesince.timesince`` function of the
		current timestamp.
		"""
		now = timezone.now()
		return djtimesince(self.send_at, now).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')






