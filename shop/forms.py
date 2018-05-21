#from django import forms as form
from django.contrib import admin
from django.contrib.gis import forms as gisforms
from django import forms
from django.forms import ModelForm    
from leaflet.forms.fields import PointField


from shop.models import Shop
from django.utils.translation import ugettext_lazy as _

from cloudinary.forms import CloudinaryFileField, CloudinaryJsFileField  
import cloudinary, hashlib

from django_countries.widgets import CountrySelectWidget
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries


from leaflet.forms.widgets import LeafletWidget

class ShopUpdateForm(forms.ModelForm):


	SPECIALTY = (
		('',                            _('Please Select')),
		('Chemical Products',           _('Chemical Products')),
		('Vegetables Products',         _('Vegetables Products')),
		('Food Products',               _('Food Products')),
		('Textile & Clothes',           _('Textile & Clothes')),
		('Leather Products',            _('Leather Products')),
		('Engineering Products',        _('Engineering Products')),
		('Wood Products',               _('Wood Products')),
		('Mining Products',             _('Mining Products')),
		('Handmade Products',           _('Handmade Products')),
		('Prototype Products',          _('Prototype Products')),
		)
	LANGUAGE =(
		('',   _('Please Select')),
		('Arabic',  _('Arabic')),
		('English', _('English')),
		('Chinese', _('Chinese')),
		('French',  _('French')),
		)
	LEGALFORM = (
		('',                      _('Please Select')),
		('Association',           _('Association')),
		('Liability.Ltd',         _('Liability.Ltd')),
		('Partnership.Ltd',       _('Partnership.Ltd')),
		('Partnership by Shares', _('Partnership by Shares')),
		('Office Rep.',           _('Office Rep.')),
		('Scientific Office',     _('Scientific Office')),
		('Branch',                _('Branch')),
		('Cooperative',           _('Cooperative')),
		('individual Ent',        _('individual Ent')),
		('Institution',           _('Institution')),
		('Joint Operating Co.',   _('Joint Operating Co.')),
		('Joint Stock',           _('Joint Stock')),
		('Work from home',        _('Work from home')),
		)


	EMPLOYEES = (
		('',     _('Please Select')),
		('From 0 to 9',    _('From 0 to 9')),
		('From 10 to 20',    _('From 10 to 20')),
		('From 20 to 49',    _('From 20 to 49')),
		('From 50 to 99',    _('From 50 to 99')),
		('From 100 to 249',    _('From 100 to 249')),
		('From 250 to 499',    _('From 250 to 499')),
		('From 500 to 999',    _('From 500 to 999')),
		('From 1000 to 4999',    _('From 1000 to 4999')),
		('More Than 5000',    _('More Than 5000')),
		)
	AREAS = (
		('',                           _('Please Select')),
		('Middle Asia',                _('Middle Asia')),
		('Africa',                     _('Africa')),
		('South america',              _('South america')),
		('Middle east',                _('Middle east')),
		('Central America',            _('Central America')),
		('all around the world',       _('all around the world')),
		('North America',              _('North America')),
		('Western Europe',             _('Western Europe')),
		('Central / Eastern Europe',   _('Central / Eastern Europe')),
		('Localhost only',             _('Localhost only')),
		)

	ACTIVITE = (
		('',                         _('Please Select')),
		('Import',                   _('Import')),
		('Export',                   _('Export')),
		('Manufacturing',            _('Manufacturing')),
		('Servisess',                _('Servisess')),
		('Shipping',                 _('Shipping')),
		)
	specialty= forms.ChoiceField(label='Specialty:',choices=SPECIALTY, required=False, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger'}),
		help_text="Choose the closest to your products")

	name = forms.CharField(label='Name:',max_length=55,required=False,widget=forms.TextInput(attrs={'class':'tags form-control col-md-7 col-xs-12 form-control-danger'}))
	slug = forms.SlugField(label='Slug:',max_length=50,required=False,widget=forms.TextInput(attrs={'class':'tags form-control col-md-7 col-xs-12 form-control-danger'}))

	keywords= forms.CharField(label='Keywords:',max_length=30,required=False,widget=forms.TextInput(attrs={'class':'tags form-control col-md-7 col-xs-12 form-control-danger'}))
	description= forms.CharField(label='Description:',max_length=1024,required=False,widget=forms.Textarea(attrs={'placeholder': 'Desccripe your specialty','class':'form-control col-md-7 col-xs-12 form-control-danger'}))


	legalform=forms.ChoiceField(label='Legal Form:',choices=LEGALFORM, required=False, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger'}))
	employees=forms.ChoiceField(label='Employees Number:',choices=EMPLOYEES, required=False, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger'}))

	activite=forms.ChoiceField(label='Activite:',choices=ACTIVITE, required=False, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger'}))
	areas=forms.ChoiceField(label='Export Areas:',choices=AREAS, required=False, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger'}))

	country = LazyTypedChoiceField(choices=countries,required=False,widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12 form-control-danger','required':'required'}))

	province     = forms.CharField(max_length=200,required=True)
	address      = forms.CharField(max_length=200,required=True)
	#geom         = PointField(label='Map Location:',required=True )

	class Meta:
		model = Shop
		exclude = ('shop',)
		fields = ('name','slug','specialty','keywords','description', 'legalform','employees','activite','areas','country','province','address','featured', 'geom')
		widgets = {'geom': LeafletWidget()}





