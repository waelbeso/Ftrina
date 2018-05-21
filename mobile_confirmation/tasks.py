from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import Celery

from django.template.loader import render_to_string 
from mobile_confirmation.models import MobileNumbers


from django.utils.translation import ugettext_lazy as _
from ftrina.celery import app as celery_app
       
from twilio.rest import TwilioRestClient
from django.conf import settings


logger = get_task_logger(__name__)

#@shared_task
@celery_app.task(name="confirm_user_mobile_task",ignore_result=False)
def confirm_user_mobile_task(mobile):
	logger.info("Send user confirm mobile")
	return confirm_user_mobile(mobile)

def confirm_user_mobile(mobile):
	print 'confirm_user_mobile:' + str(mobile)
	user_confirm_mobile = MobileNumbers.objects.get(mobile=mobile)
	member = user_confirm_mobile.user
	path_to_txt = 'confirmation_sms.txt'
	context = {'member': member, 'key': user_confirm_mobile.key}
	sms = render_to_string(path_to_txt, context)
	print sms
	account_sid           = getattr(settings, "TWILIO_ACCOUNT_SID", None)
	auth_token            = getattr(settings, "TWILIO_AUTH_TOKEN", None)
	from_number           = getattr(settings, "TWILIO_FROM_NUMBER", None)
	messaging_service_sid = getattr(settings, "MESSAGING_SERVICES_SID", None)
	twilio = TwilioRestClient(account_sid, auth_token)
	#message = twilio.messages.create( to=str(mobile), messaging_service_sid=messaging_service_sid, body=str(sms),)
	message = twilio.sms.messages.create(to=str(mobile), from_=str(from_number), body=str(sms))
	user_confirm_mobile.sid = message.sid
	user_confirm_mobile.save()
	return message.sid

