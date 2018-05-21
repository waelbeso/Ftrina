from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import Celery

from celery import shared_task
import cloudinary
from album.models import Image
from ftrina.celery import app as celery_app
from django.conf import settings


logger = get_task_logger(__name__)

#@shared_task
@celery_app.task(name="delete_image_by_public_id",ignore_result=False)
def delete_image_by_public_id(public_id):
	logger.info("delete image by public_id ")
	return delete_image_by_public_id_task(public_id)

def delete_image_by_public_id_task(public_id):
	deleted_image = cloudinary.api.delete_resources([public_id])
	image = Image.objects.filter(public_id=public_id).delete()
	return deleted_image

