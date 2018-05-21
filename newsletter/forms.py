from django import forms
from django.forms import ModelForm    
from .models import Subscribers


#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class SubscribersForm(forms.ModelForm):

	email        = forms.EmailField(max_length=55,widget=forms.TextInput(attrs={'placeholder': 'Email Address', 'class':'form-control',}),)

	class Meta:
		model = Subscribers
		fields = ( 'email',)

	def clean_email(self):
		email = self.cleaned_data['email']

		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError("That email is already register with us" )