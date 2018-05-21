from rest_framework import serializers
from basket.models import Basket
from shop.models import Order

class OrderSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = ('id','product','quantity')

class BasketSerializer(serializers.ModelSerializer):
	order = OrderSerializer(many=True, read_only=True)
	
	class Meta:
		model = Basket
		fields = ('id','order','usd','eur','aed','sar','kwd','egp','rmb','hkd')