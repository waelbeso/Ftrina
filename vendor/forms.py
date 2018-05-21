
from django import forms
from shop.models import Invoice,Shop,Branch,WareHouse,Product,Collection,Contact,Variant,Inventory
from django.utils.translation import ugettext_lazy as _
from ftrina.countries import COUNTRIES,COUNTRIES_CODE,CURRENCY,COURIER,COUNTRIES_2
from leaflet.forms.fields import PointField
from cloudinary.forms import CloudinaryJsFileField   
from album.models import Image
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
# Next two lines are only used for generating the upload preset sample name
from cloudinary.compat import to_bytes
import cloudinary, hashlib

from django.forms.widgets import ChoiceWidget
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe





class editInventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super(editInventoryForm, self).__init__(*args, **kwargs)
        if not self.product == None:
            self.fields['quantity']  = forms.IntegerField(required=True, initial= 1 , min_value=0 , widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'class':'form-control', 'id':'QuantityInput' }))
            self.fields['warehouse'] = forms.ModelChoiceField( queryset=self.product.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class addToInventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super(addToInventoryForm, self).__init__(*args, **kwargs)
        if not self.product == None:
            self.fields['quantity']  = forms.IntegerField(required=True, initial= 1 , min_value=0 , widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'class':'form-control', 'id':'QuantityInput' }))
            self.fields['warehouse'] = forms.ModelChoiceField( queryset=self.product.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
            for option in self.product.option:
                self.fields[ option["name"] ] = forms.ChoiceField(label=option["name"] + " * ",choices=option["value"], initial= option["value"][0] , required=True, widget=forms.Select(attrs={ 'class':'form-control'   }))

class inventoryForm(forms.Form):
	quantity = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'class':'form-control', 'id':'priceInput' }))
	#warehouse  = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Warehouse', 'class':'form-control' }))
	class Meta:
		model  = Inventory


class variantForm(forms.Form):
	price = forms.FloatField(required=True, min_value=1, widget=forms.NumberInput(attrs={'placeholder':'Price', 'class':'form-control', 'id':'priceInput' }))
	class Meta:
		model  = Variant

class upsForm(forms.Form):
	account_number  = forms.CharField(label=_('Account Number'),widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control' }))
	access_key      = forms.CharField(label=_('Access Key'),widget=forms.TextInput(attrs={'placeholder':'Access Key', 'class':'form-control' }))
	password        = forms.CharField(widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))
	user_identifier = forms.CharField(label=_('User Identifier'),widget=forms.TextInput(attrs={'placeholder':'User Identifier', 'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(upsForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))


class AramexAccountForm(forms.Form):
	account_number = forms.CharField(label=_('Account Number'),widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control' }))
	username       = forms.CharField(label=_('Username'),widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
	password       = forms.CharField(widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))
	account_pin    = forms.CharField(label=_('Account Pin'),widget=forms.TextInput(attrs={'placeholder':'Account Pin', 'class':'form-control'}))
	account_entity = forms.CharField(label=_('Account Entity'),widget=forms.TextInput(attrs={'placeholder':'Account Entity', 'class':'form-control'}))
	account_country = forms.ChoiceField(label=_('Account Country'),choices=COUNTRIES_2, required=True, widget=forms.Select(attrs={ 'class':'form-control', 'id':'countryInput'}))

	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(AramexAccountForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))


class dhlForm(forms.Form):
	account_number = forms.CharField(label=_('Account Number'),widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control' }))
	password       = forms.CharField(widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))
	site_id        = forms.CharField(label=_('Site ID'),widget=forms.TextInput(attrs={'placeholder':'Site ID', 'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(dhlForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))


class tntForm(forms.Form):
	company_id     = forms.CharField(label=_('Company Id'),widget=forms.TextInput(attrs={'placeholder':'Company ID', 'class':'form-control'}))
	password       = forms.CharField(widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control'}))
	account_number = forms.CharField(label=_('Account Number'),widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control'}))
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(tntForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class FedexAccountForm(forms.Form):
	account_number = forms.CharField(label=_('Account Number'),widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control' }))
	password       = forms.CharField( widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control' }))
	key            = forms.CharField(label=_('Key'),widget=forms.TextInput(attrs={'placeholder':'Key', 'class':'form-control' }))
	meter_number   = forms.CharField(label=_('Meter Number'),widget=forms.TextInput(attrs={'placeholder':'Meter Number', 'class':'form-control'}))
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(FedexAccountForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class CreateShipperAccountForm(forms.Form):
	account_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Account Number', 'class':'form-control', 'id':'userNameInputLogin' }))
	password       = forms.CharField( widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control', 'id':'passwordInputLogin' }))
	site_id        = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Site ID', 'class':'form-control', 'id':'userNameInputLogin' }))
	courier        = forms.ChoiceField(label=_('Courier:'),choices=COURIER, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'currencyInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
	#warehouse      = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control', 'id':'FirstNameInput' }))
	class Meta:
		model = Contact
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(CreateShipperAccountForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class DefaultContactForm(forms.Form):
	contact  = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control', 'id':'FirstNameInput' }))
	class Meta:
		model = Contact
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(DefaultContactForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['contact'] = forms.ModelChoiceField(queryset=self.shop.contact_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class DefaultWarehouseForm(forms.Form):
	warehouse  = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Warehouse', 'class':'form-control' }))
	class Meta:
		model  = Contact
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		super(DefaultWarehouseForm, self).__init__(*args, **kwargs)
		if not self.shop == None:
			self.fields['warehouse'] = forms.ModelChoiceField(queryset=self.shop.warehouse_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class DefaultCurrencyForm(forms.Form):
	currency  = forms.ChoiceField(label=_('Currency:'),choices=CURRENCY, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'currencyInput', 'data-live-search':'true','data-dropup-auto':'false'   }))


class ContactForm(forms.Form):
	first_name  = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control', 'id':'FirstNameInput' }))
	last_name   = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control', 'id':'LastNameInput' }))
	email       = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
	mobile          = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))
	country_code    = forms.ChoiceField(label=_('Country Code:'),choices=COUNTRIES_CODE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false',
		'type':'button', 'data-toggle':'dropdown', 'aria-haspopup':'true', 'aria-expanded':'false'
	   }))

	class Meta:
		model = Contact

class ProductForm(forms.Form):
	LANGUAGE =(
		('',   _('Please Select')),
		('Arabic',  _('Arabic')),
		('English', _('English')),
		('Chinese', _('Chinese')),
		('French',  _('French')),
		)
	

	name             = forms.CharField(label=_('Title'),required=True,widget=forms.TextInput(attrs={'placeholder':'Product Name', 'class':'form-control', 'id':'NameInput' }))
	keyword          = forms.CharField(label=_('Keyword'),widget=forms.TextInput(attrs={'placeholder':'Search Keyword', 'class':'form-control', 'id':'keywordInput', 'data-role':'tagsinput'}) , required=False )
	cart_description = forms.CharField(label=_('Cart Description'),required=True,widget=forms.TextInput(attrs={'placeholder':'Cart Description', 'class':'form-control' }))

	
	description      = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Description', 'class':'form-control email-body load-ckeditor ', 'id':'descriptionInput'}))

	price            = forms.FloatField(required=True, min_value=1, widget=forms.NumberInput(attrs={'placeholder':'Price', 'class':'form-control', 'id':'priceInput' }))
	weight           = forms.FloatField(required=True, max_value=20000, min_value=1, widget=forms.NumberInput(attrs={'placeholder':'Product Weight', 'class':'form-control', 'id':'weightInput' }))
	origin           = forms.ChoiceField(label=_('Origin:'),choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'originInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
	variant          = forms.CharField(required=False,widget=forms.HiddenInput(attrs={ 'class':'variant_container'}) )
	photos           = forms.CharField(required=False,widget=forms.HiddenInput(attrs={ 'class':'photo_container'}) )
	sku              = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Stock Keeping Unit', 'class':'form-control', 'id':'skuInput' }))

	class Meta:
		model = Product
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		self.product = kwargs.pop('product', None)
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields["price_currency"] = forms.ChoiceField(label=_('Currency:'),choices=CURRENCY, initial=self.shop.currency, required=False, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'currencyInput', 'data-live-search':'true','data-dropup-auto':'false', 'disabled':'disabled'   }))

	def clean_name(self, *args, **kwargs):
		name = self.cleaned_data['name']
		products = self.shop.product_set.all()
		if not self.product:
			for objects in products:
				if objects.name == name:
					raise forms.ValidationError( _("You have product with the same name") )
		else:
			if self.product.name == name:
				return name
			else:
				for objects in products:
					if objects.name == name:
						raise forms.ValidationError( _("You have product with the same name") )
		return name


class CollectionForm(forms.Form):
	LANGUAGE =(
		('',   _('Please Select')),
		('Arabic',  _('Arabic')),
		('English', _('English')),
		('Chinese', _('Chinese')),
		('French',  _('French')),
		)
	name         = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Collection Name', 'class':'form-control', 'id':'NameInput' }))
	keywords     = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Keywords', 'class':'form-control', 'id':'keywordsInput', 'data-role':'tagsinput' }))
	products     = forms.CharField(required=False,widget=forms.HiddenInput(attrs={ 'class':'token'}) )


	class Meta:
		model = Collection
	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		self.collection = kwargs.pop('collection', None)
		super(CollectionForm, self).__init__(*args, **kwargs)

	def clean_name(self, *args, **kwargs):
		name = self.cleaned_data['name']
		collection = self.shop.collection_set.all()
		if not self.collection:
			for objects in collection :
				if objects.name == name:
					raise forms.ValidationError( _("You have collection with the same name") )
		else:
			if self.collection.name == name:
				return name
			else:
				for objects in collection:
					if objects.name == name:
						raise forms.ValidationError( _("You have collection with the same name") )
		return name
class BranchForm(forms.Form):
	name     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Branch Name', 'class':'form-control', 'id':'NameInput' }))
	mobile          = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))
	country_code    = forms.ChoiceField(label=_('Country Code:'),choices=COUNTRIES_CODE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false',
		'type':'button', 'data-toggle':'dropdown', 'aria-haspopup':'true', 'aria-expanded':'false'
	   }))
	
	country  = forms.ChoiceField(label=_('Country:'),choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
	province = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))
	city     = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
	zip_code = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))
	address  = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))
	geom         = PointField(label=_('Branch Location:'),required=True )

	class Meta:
		model = Branch

	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		self.branch = kwargs.pop('branch', None)
		super(BranchForm, self).__init__(*args, **kwargs)

	def clean_name(self, *args, **kwargs):
		name = self.cleaned_data['name']
		branches = self.shop.branch_set.all()
		if not self.branch:
			for objects in branches :
				if objects.name == name:
					raise forms.ValidationError( _("You have branch with the same name") )
		else:
			if self.branch.name == name:
				return name
			else:
				for objects in branches:
					if objects.name == name:
						raise forms.ValidationError( _("You have branch with the same name") )
		return name
class WareHouseForm(forms.Form):
	name     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Name', 'class':'form-control', 'id':'NameInput' }))
	country  = forms.ChoiceField(label=_('Country:'),choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
	province = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))
	city     = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
	zip_code = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))
	address  = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))
	geom         = PointField(label=_('Branch Location:'),required=True )

	class Meta:
		model = WareHouse
		#fields = ['shop', 'country', 'province','city','zip_code','address','geom']

	def __init__(self, *args, **kwargs):
		self.shop = kwargs.pop('shop', None)
		self.warehouse = kwargs.pop('warehouse', None)
		super(WareHouseForm, self).__init__(*args, **kwargs)

	def clean_name(self, *args, **kwargs):
		name = self.cleaned_data['name']
		warehouse = self.shop.warehouse_set.all()
		if not self.warehouse:
			for objects in warehouse :
				if objects.name == name:
					raise forms.ValidationError( _("You have warehouse with the same name") )
		else:
			if self.warehouse.name == name:
				return name
			else:
				for objects in warehouse:
					if objects.name == name:
						raise forms.ValidationError( _("You have warehouse with the same name") )
		return name
		


class OrdersEditForm(forms.Form):
    CHOICES = (  ('', _('Please select') )  , ('Pending', _('Pending'),) , ('Picked', _('Picked'),) , ('Shipped', _('Shipped'),) , ('Reserved', _('Reserved'),) )
    stage   = forms.ChoiceField(label='Country:',choices=CHOICES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

    class Meta:
    	model = Invoice


class EditBasicInfoForm(forms.Form):
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
	specialty    =forms.ChoiceField(choices=SPECIALTY, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'specialtyInput'}))
	keywords     =forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Keywords', 'class':'form-control', 'id':'keywordsInput' , 'data-role':'tagsinput' }))
	language     =forms.ChoiceField(choices=LANGUAGE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'languageInput'}))
	description  = forms.CharField(required=False,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Notes', 'class':'form-control email-body load-ckeditor ', 'id':'descriptionInput'}))

	class Meta:
		model = Shop

class EditBusinessInfoForm(forms.Form):
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
		('From 0 to 9',        _('From 0 to 9')),
		('From 10 to 20',      _('From 10 to 20')),
		('From 20 to 49',      _('From 20 to 49')),
		('From 50 to 99',      _('From 50 to 99')),
		('From 100 to 249',    _('From 100 to 249')),
		('From 250 to 499',    _('From 250 to 499')),
		('From 500 to 999',    _('From 500 to 999')),
		('From 1000 to 4999',  _('From 1000 to 4999')),
		('More Than 5000',     _('More Than 5000')),
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
	legalform    =forms.ChoiceField(label=_('Legal Form:'), choices=LEGALFORM, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'specialtyInput'}))
	employees    =forms.ChoiceField(label=_('Employee Average:'), choices=EMPLOYEES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'specialtyInput'}))
	activite     =forms.ChoiceField(label=_('Activite:'), choices=AREAS, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'specialtyInput'}))
	areas        =forms.ChoiceField(label=_('Target market:'), choices=ACTIVITE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'specialtyInput'}))
	
	class Meta:
		model = Shop


class EditLocationInfoForm(forms.Form):

    country  = forms.ChoiceField(label=_('Country:'),choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
    province = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))
    city     = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
    zip_code = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))
    address  = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))
    geom         = PointField(label=_('Map Location:'),required=True )


    class Meta:
        model = Shop










class PhotoForm(forms.ModelForm):
	'''
	PRODUCT  = Product.objects.all()
	PRODUCTLIST = [ ('',  'please select') ]
	for product in PRODUCT:
		PRODUCTLIST.append( ( product.pk ,  product ) )
	'''

	#profile     = forms.CharField(max_length=55,widget=forms.TextInput(attrs={'placeholder': 'Product','class':'form-control', 'id':'iorder', 'type':'hidden' }),)

	class Meta:
		model = Image
		fields = ( 'image',)

class PhotoDirectForm(PhotoForm):
    image = CloudinaryJsFileField()
    
class PhotoUnsignedDirectForm(PhotoForm):
    upload_preset_name = "sample_" + hashlib.sha1(to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)




