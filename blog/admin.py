# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from models import Category,Article,Photo

class ArticleAdmin(admin.ModelAdmin):
	#form = ProductAdminForm
	def category(self, obj):
		return obj.category
	def published(self, obj):
		return obj.published
	def name(self, obj):
		return obj.title
	list_display = ('title', 'category', 'published')

admin.site.register(Photo,)
admin.site.register(Category,)
admin.site.register(Article,ArticleAdmin)


