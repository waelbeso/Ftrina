from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class RatingsConfig(AppConfig):
    name = 'ratings'

    def ready(self):
    	from .models import UserRating
    	from .signals import calculate_ratings

    	post_save.connect(calculate_ratings, sender=UserRating)
    	post_delete.connect(calculate_ratings, sender=UserRating)
#https://github.com/wildfish/django-star-ratings