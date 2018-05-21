#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from shop.search_indexes import ShopIndex,ProductIndex,CollectionIndex
from drf_haystack.serializers import HaystackSerializer




class ShopSearchSerializer(HaystackSerializer):

	def get_instance(self, obj):
		return obj.model_name
	def get_url(self, obj):
		return obj.object.url
	def get_followers(self, obj):
		return obj.object.followers
	def get_rating(self, obj):
		return obj.object.rating
	def get_orders(self, obj):
		return obj.object.orders

	instance    = serializers.SerializerMethodField()
	url         = serializers.SerializerMethodField()
	followers   = serializers.SerializerMethodField()
	rating      = serializers.SerializerMethodField()
	orders      = serializers.SerializerMethodField()

	class Meta:
		index_classes = [ShopIndex]
		fields = ["name", "language"]
		ignore_fields = ["autocomplete"]
		field_aliases = { "q": "name" }

class CollectionSearchSerializer(HaystackSerializer):

	def get_instance(self, obj):
		return obj.model_name
	def get_url(self, obj):
		return obj.object.url
	def get_followers(self, obj):
		return obj.object.followers
	def get_rating(self, obj):
		return obj.object.rating
	def get_orders(self, obj):
		return obj.object.orders

	instance    = serializers.SerializerMethodField()
	url         = serializers.SerializerMethodField()
	followers   = serializers.SerializerMethodField()
	rating      = serializers.SerializerMethodField()
	orders      = serializers.SerializerMethodField()

	class Meta:
		index_classes = [CollectionIndex]
		fields = ["name", "language"]
		ignore_fields = ["autocomplete"]
		field_aliases = { "q": "name" }

class ProductSearchSerializer(HaystackSerializer):

	def get_instance(self, obj):
		return obj.model_name
	def get_url(self, obj):
		return obj.object.url
	def get_followers(self, obj):
		return obj.object.followers
	def get_rating(self, obj):
		return obj.object.rating
	def get_orders(self, obj):
		return obj.object.orders

	instance    = serializers.SerializerMethodField()
	url         = serializers.SerializerMethodField()
	followers   = serializers.SerializerMethodField()
	rating      = serializers.SerializerMethodField()
	orders      = serializers.SerializerMethodField()
	
	class Meta:
		index_classes = [ProductIndex]
		fields = ["name", "language"]
		ignore_fields = ["autocomplete"]
		field_aliases = { "q": "name" }


class SearchSerializer(HaystackSerializer):

	class Meta:
		serializers = {
			ShopIndex     : ShopSearchSerializer,
			CollectionIndex : CollectionSearchSerializer,
			ProductIndex  : ProductSearchSerializer,
			}

	def multi_serializer_representation(self, instance):
		#print dir(self)
		serializers = self.Meta.serializers
		index = instance.searchindex
		serializer_class = serializers.get(type(index), None)
		if not serializer_class:
			raise ImproperlyConfigured("Could not find serializer for %s in mapping" % index)
		return serializer_class(context=self._context).to_representation(instance)


