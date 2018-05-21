




from shipping.models import Model,Zone
from rest_framework import serializers
from shop.models import WareHouse,Shop

from rest_framework.validators import UniqueTogetherValidator

class ModelSerializer(serializers.ModelSerializer):

	def ShippingValidator(value):
		import json
		if "update" in value['method']:
			if value['name']:
				try:
					Model.objects.get(name=value['name'],shop=value['shop'])
				except Model.DoesNotExist:
					return
				shop_shipping_model = Model.objects.get(name=value['name'],shop=value['shop'])
				if str(shop_shipping_model.id) in value['pk']:
					return
				raise serializers.ValidationError('You have Shipping Model with this name.')
			raise serializers.ValidationError('Name is required.')

		if "new" in value['method']:
			if value['name']:
				try:
					Model.objects.get(name=value['name'],shop=value['shop'])
				except Model.DoesNotExist:
					return
				raise serializers.ValidationError('You have Shipping Model with this name.')
			raise serializers.ValidationError('Name is required.')

	name       = serializers.JSONField(required=True, validators=[ShippingValidator])
	shop       = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.filter(),read_only=False)
	ware_house = serializers.PrimaryKeyRelatedField(required=True,queryset=WareHouse.objects.filter(),read_only=False)

	class Meta:
		model  = Model
		fields = ('id', 'name','shop','ware_house','zone')

	def update(self, instance, validated_data):
		''' We did not update the shop record '''
		ware_house          = WareHouse.objects.get(pk=validated_data.pop('ware_house'))
		instance.name       = validated_data.get('name', instance.name)
		instance.ware_house = ware_house
		instance.save()
		return instance



class ZoneSerializer(serializers.ModelSerializer):

	model          = serializers.PrimaryKeyRelatedField(queryset=Model.objects.filter(),read_only=False)
	country        = serializers.CharField(required=True)
	province       = serializers.CharField(required=True)
	price          = serializers.DecimalField(max_digits=19, decimal_places=2, coerce_to_string=None, max_value=None, min_value=None)
	price_currency = serializers.CharField(max_length=None, min_length=None, allow_blank=False)

	class Meta:
		model  = Zone
		fields = ('id', 'model','country','province','price','price_currency')

		validators = [
		UniqueTogetherValidator(
			queryset=Zone.objects.all(),
			fields=('model', 'country','province')
			)
		]







