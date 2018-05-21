from __future__ import unicode_literals

from django.db import models

# Create your models here.

from profile.models import Profile
from shop.models import Shop,Product
import uuid
from cloudinary.models import CloudinaryField
# confirmed status means the image have relation with one of our models
# validate  status means one of our team view the image and validate it's not publishing rules violation



class Image(models.Model):
	id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title          = models.CharField("Title (optional)", max_length=200, blank=True)
	shop           = models.ForeignKey(Shop,blank=True, null=True,)
	profile        = models.ForeignKey(Profile,blank=True, null=True)
	product        = models.ForeignKey(Product,blank=True,null=True,related_name='images')
	secure_url     = models.URLField(max_length=200,default = "https://res.cloudinary.com/ftrina/image/upload/v1469046333/default_user_avatar_ljpbex.png" )
	public_id      = models.CharField( max_length=256,blank=True, null=True)
	add_time       = models.DateTimeField(auto_now=True)

	is_logo        = models.BooleanField(default=False)
	is_banner      = models.BooleanField(default=False)
	is_product     = models.BooleanField(default=False)
	is_avatar      = models.BooleanField(default=False)
	is_bug         = models.BooleanField(default=False)
	confirmed      = models.BooleanField(default=False)
	
	## Points to a Cloudinary image
	image = CloudinaryField('image')

	""" Informative name for model """
	def __unicode__(self):
		return self.image.public_id

