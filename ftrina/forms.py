from __future__ import unicode_literals

import unicodedata

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _


from django import forms
#from django.contrib.auth.models import User
from django.forms import ModelForm



from haystack.query import EmptySearchQuerySet, SearchQuerySet


from .countries import COUNTRIES,COUNTRIES_CODE

from basket.models import Checkout

from django.contrib.auth.forms import SetPasswordForm
from profile.models import Profile,Address
from shop.models import Order

from django.contrib.auth import get_user_model
User = get_user_model()
UserModel = get_user_model()

from phonenumber_field.validators import  validate_international_phonenumber



class addToCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super(addToCartForm, self).__init__(*args, **kwargs)
        if not self.product == None:
            self.fields['quantity'] = forms.IntegerField(required=True, initial= 1 , min_value=1, max_value = self.product.availability["quantity"] , widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'class':'form-control', 'id':'QuantityInput' }))
            for option in self.product.option:
                #print option["name"]
                self.fields[ option["name"] ] = forms.ChoiceField(label=option["name"] + " * ",choices=option["value"], initial= option["value"][0] , required=True, widget=forms.Select(attrs={ 'class':'form-control'   }))

class DeliveryForm(forms.Form):
    shipping   = forms.ChoiceField( required=True , widget=forms.RadioSelect() )
    #checkout   = forms.CharField(required=False,widget=forms.HiddenInput(attrs={ 'class':'token'}) )


class PayForm(forms.Form):

    name   = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Card Holder Name', 'class':'input', 'id':'name', 'type':'text' , 'data-tid':'name_placeholder'}))
    stripeToken = forms.CharField(required=False,widget=forms.HiddenInput(attrs={ 'class':'token'}) )

    #email  = forms.EmailField(required=False,widget=forms.TextInput(attrs={'placeholder':'email@domine.tld', 'class':'input', 'id':'email' , 'type':'text' , 'data-tid':'email_placeholder'}))
    #phone  = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'(941) 555-0123', 'class':'input', 'id':'phone', 'type':'tel' , 'data-tid':'phone_placeholder'}))
    #card   = forms.CharField(required=False,widget=forms.TextInput(attrs={ 'class':'input', 'id':'card-element'}))
    #card
    #expire_date      = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
    #cvv     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))



class AddAddressForm(forms.Form):

    name     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Address Name', 'class':'form-control', 'id':'NameInput' }))
    country  = forms.ChoiceField(label='Country:',choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
    province = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))
    city     = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
    zip_code = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))
    address  = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))


    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddAddressForm, self).__init__(*args, **kwargs)

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data['name']
        address = self.user.address_set.all()
        for objects in address :
            if objects.name == name:
                raise forms.ValidationError("You have address with the same name")

        return name

class EditAddressForm(forms.Form):

    name     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Address Name', 'class':'form-control', 'id':'NameInput' }))
    country  = forms.ChoiceField(label='Country:',choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
    province = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))
    city     = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
    zip_code = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))
    address  = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))


    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.address = kwargs.pop('address', None)
        super(EditAddressForm, self).__init__(*args, **kwargs)

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data['name']
        address = self.user.address_set.all()
        user_address = self.address
        if user_address.name == name:
            return name
        else:
            for objects in address :
                if objects.name == name:
                    raise forms.ValidationError("You have address with the same name")
                    
        return name

class EditProfileForm(forms.Form):
    first_name      = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control', 'id':'firstNameInput' }))
    last_name       = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'User Name', 'class':'form-control', 'id':'lastNameInput' }))
    email           = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
    mobile          = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))
    country_code    = forms.ChoiceField(label='Country:',choices=COUNTRIES_CODE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
    

    class Meta:
        model = Profile


class UpdateCartForm(forms.Form):
    quantity     = forms.IntegerField(required=True, initial= 1 , min_value=1 , widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'class':'form-control', 'id':'QuantityInput' }))
    order        = forms.CharField(required=True,widget=forms.HiddenInput() )
    class Meta:
        model = Order
    def __init__(self, *args, **kwargs):
        print args
        print kwargs
        super(UpdateCartForm, self).__init__(*args, **kwargs)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control', 'id':'firstNameInput' }))
    last_name  = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control', 'id':'lastNameInput' }))
    email      = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
    mobile     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))

    address    = forms.CharField(required=True,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Address', 'class':'form-control', 'id':'addressInput'}))
    city       = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'City', 'class':'form-control', 'id':'cityInput'}))
    zip_code   = forms.CharField(required=True,widget=forms.NumberInput(attrs={'type':'text', 'placeholder': 'Post Code', 'class':'form-control', 'id':'postInput'}))

    country    = forms.ChoiceField(label='Country:',choices=COUNTRIES, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))
    province   = forms.CharField(required=True,widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Province', 'class':'form-control', 'id':'regionInput'}))

    notes      = forms.CharField(required=False,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Notes', 'class':'form-control', 'id':'addressInput'}))

    class Meta:
        model = Checkout

class UserCheckoutForm(forms.Form):
    address    = forms.ModelChoiceField(queryset = Address.objects.all() )
    notes      = forms.CharField(required=False,widget=forms.Textarea(attrs={'type':'textarea','rows':'3' ,'placeholder': 'Notes', 'class':'form-control', 'id':'addressInput'}))
    class Meta:
        model = Address

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserCheckoutForm, self).__init__(*args, **kwargs)
        if not self.user == None:
            self.fields['address'] = forms.ModelChoiceField(queryset=self.user.address_set.all(), empty_label="--- Please Select ---", required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class LoginForm(forms.Form):
	username        = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'User Name', 'class':'form-control', 'id':'userNameInputLogin' }))
	password        = forms.CharField( widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control', 'id':'passwordInputLogin' }))

class RegisterForm(ModelForm):
        username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User Name', 'class':'form-control', 'id':'userNameInput' }))
        email    = forms.EmailField(widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
        password = forms.CharField( widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Password', 'type':'password', 'class':'form-control', 'id':'passwordInput' }))

        password_confirm = forms.CharField( widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'password Confirm', 'type':'password', 'class':'form-control', 'id':'passwordConfirmInput' }))

        phone           = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control', 'id':'phoneInput' }))
        country_code    = forms.ChoiceField(label='Country code',choices=COUNTRIES_CODE, required=True, widget=forms.Select(attrs={ 'class':'form-control selectpicker', 'id':'countryInput', 'data-live-search':'true','data-dropup-auto':'false'   }))

        class Meta:
                model = User
                #exclude = ('user',)
                fields = ['username','email','password','password_confirm','country_code','phone']

        def clean_username(self):
        	username = self.cleaned_data['username']
        	try:
        		User.objects.get(username=username)
        	except User.DoesNotExist:
        		return username
        	raise forms.ValidationError("That username is already taken, please select another.")
                
        def clean_email(self):
        	email = self.cleaned_data['email']
        	try:
        		User.objects.get(email=email)
        	except User.DoesNotExist:
        		return email
        	raise forms.ValidationError("That email is already register with us , please select another or login" )

        def clean_phone(self):
            mobile = '+' + self.data['country_code'] + self.cleaned_data['phone']
            validate_international_phonenumber(mobile)
            try:
                User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                return mobile
            raise forms.ValidationError("That mobile is already register with us , please select another or login" )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Email', 'class':'form-control', 'id':'emailInput'}))
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'New Password', 'type':'password', 'class':'form-control', 'id':'new_password1' }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(render_value=False , attrs={'placeholder':'Confirm New Password', 'type':'password', 'class':'form-control', 'id':'new_password2' }),
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True , 'class':'form-control', 'placeholder':'Old Password'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache



class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'text','aria-label':'Search here...', 'placeholder':'Search here...', 'class':'form-control search-input', 'autocomplete':"off" }))

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(SearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data['q'])
