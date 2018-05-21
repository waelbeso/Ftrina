from django.forms import widgets
from rest_framework import serializers
from future_customer.models import Future_Customer



class FutureCustomerSerializer(serializers.Serializer):

    def InternationalPhonenumberValidate(value):
        from phonenumber_field.phonenumber import to_python

        phone_number = to_python(value)
        if phone_number and not phone_number.is_valid():
            raise serializers.ValidationError('The MOBILE Number you entered is not valid.')


    name = serializers.CharField(required=True, min_length=6, max_length=25,)

    mobile = serializers.CharField(required=True, allow_blank=False, max_length=15,
        validators=[InternationalPhonenumberValidate],)

    email = serializers.EmailField(required=True, allow_blank=False,max_length=50,)


    class Meta:
        model = Future_Customer
        fields = ('name', 'mobile', 'email')

