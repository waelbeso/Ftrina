from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import Celery

from django.template.loader import render_to_string 

from django.template.loader import render_to_string # for mail gun
from django.core.mail import send_mail, EmailMultiAlternatives # for mail gun
from django.core.mail import get_connection # for mail gun

from django.conf import settings

import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.utils.translation import ugettext_lazy as _
from ftrina.celery import app as celery_app
from album.models import Image

logger = get_task_logger(__name__)

#@shared_task
@celery_app.task(name="verification_confirmation_task",ignore_result=False)
def verification_confirmation_task(user,target,attachment):
	logger.info("Send verification confirmation")
	return send_verification_confirmation(user,target,attachment)

def send_verification_confirmation(user,target,attachment):

	user_email = user.email
	path_to_txt = 'verification_confirmation_email.txt'
	subjec = 'Verification confirmation'
	context = {'user_name': user.username}
	message = render_to_string(path_to_txt, context)
	send_mail(subjec, message, 'admin@ftrina.com',
		[str(user_email)], fail_silently=False)

	path_to_txt = 'verification_request_email.txt'
	subjec = 'Verification confirmation'
	context = {'user_name': user.username,'target':target,'img':attachment}
	message = render_to_string(path_to_txt, context)
	send_mail(subjec, message, 'admin@ftrina.com',
		[str(user_email)], fail_silently=False)
	
	image = Image.objects.filter(secure_url=attachment).update(confirmed = True,)
	return "email's send"



@celery_app.task(name="avatar_changing_task",ignore_result=False)
def avatar_changing_task(user,db_avatar,old_avatar):
	logger.info("Avatar Changing")
	return update_user_avatar(user,db_avatar,old_avatar)

def update_user_avatar(user,db_avatar,old_avatar):

	default_public_id = getattr(settings, "DEFAULT_USERS_AVATARE_PUBLIC_ID", None)
	if str(default_public_id) in str(db_avatar):
		print "remove old_avatar"
		print db_avatar,old_avatar
		cloudinary.api.delete_resources([old_avatar])

	if not str(default_public_id) in str(db_avatar):
		print "remove old_avatar and db_avatar "
		print db_avatar,old_avatar
		cloudinary.api.delete_resources([db_avatar,old_avatar])

	return "user avatar updated"





