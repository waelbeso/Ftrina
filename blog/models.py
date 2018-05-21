# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import uuid

from cloudinary.models import CloudinaryField

# Create your models here.


class Category(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name         = models.CharField(max_length=38, blank=True, null=True)
	lang         = models.CharField(max_length=20)
	def __unicode__(self): 
		return self.name

class Article(models.Model):
	id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	date         = models.DateTimeField(default=timezone.now,auto_now=False,blank=True)
	title        = models.CharField(max_length=38, blank=True, null=True)
	body         = models.TextField()
	description  = models.CharField(max_length=110, blank=True, null=True)
	lang         = models.CharField(max_length=20)
	recommended  = models.BooleanField(default=False)
	published    = models.BooleanField(default=False)
	category     = models.ForeignKey(Category, on_delete=models.CASCADE)
	notification = models.BooleanField(default=False)
	def __unicode__(self): 
		return self.title

	@property
	def image(self):
		try:
			thumb = self.photo_set.first().image.url
		except AttributeError :
			return ''
		else:
			return self.photo_set.first().image.url

class Photo(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    article     = models.ForeignKey(Article, on_delete=models.CASCADE,null=True,blank=True)
    image       = CloudinaryField('image')

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return self.article.title




