# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Basket , Checkout
# Register your models here.
admin.site.register(Basket)
admin.site.register(Checkout)
