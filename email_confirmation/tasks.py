from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import Celery

from email_confirmation.models import EmailAddress

from django.template.loader import render_to_string # for mail gun
from django.core.mail import send_mail, EmailMultiAlternatives # for mail gun
from django.core.mail import get_connection # for mail gun

from django.utils.translation import ugettext_lazy as _
from ftrina.celery import app as celery_app

logger = get_task_logger(__name__)

#@shared_task
@celery_app.task(name="confirm_user_email_task",ignore_result=True)
def confirm_user_email_task(email):
	logger.info("Send user confirm email")
	return confirm_user_email(email)

def confirm_user_email(email):
	print 'confirm_user_email:' + str(email)
	user_confirm_email = EmailAddress.objects.get(email=email)
	#print user_confirm_email.key
	#print user_confirm_email.user
	member = user_confirm_email.user
	subjec =_('Confirmation')
	#path_to_txt = 'confirmation_email.txt'
	path_to_txt = 'confirmation_email.html'
	context = {'member': member, 'key': user_confirm_email.key}
	#message = render_to_string(path_to_txt, context)
	html_content  = render_to_string(path_to_txt, context).strip()
	msg = EmailMultiAlternatives(subjec, html_content, 'admin@ftrina.com',[email]) 
	msg.content_subtype = 'html'
	msg.mixed_subtype = 'related'
	msg.send() 
	return 'email send'
