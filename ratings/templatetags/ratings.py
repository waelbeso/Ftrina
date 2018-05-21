from __future__ import unicode_literals

from decimal import Decimal
import uuid
from django import template
from django.template import loader

from ..models import UserRating
from .. import app_settings, get_star_ratings_rating_model
from ..compat import is_authenticated

register = template.Library()


@register.filter(name='full') 
def full(number):
	return range(number)
@register.filter(name='empty') 
def empty(number):
	return range(5 - number)