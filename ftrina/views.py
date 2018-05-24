from django.http import HttpResponse
from django.shortcuts import render

from django.template.context_processors import csrf
from django.template import Context, RequestContext

from django.contrib.auth import authenticate,logout,login
from .auth import logout,login
from django.http import HttpResponseRedirect
from .forms import LoginForm , RegisterForm,CheckoutForm,PayForm,PasswordChangeForm,EditProfileForm,AddAddressForm,UserCheckoutForm,EditAddressForm,UpdateCartForm,DeliveryForm,addToCartForm

from newsletter.forms import SubscribersForm
#from product.models import Category,Product
from django.contrib.auth.models import User
from blog.models import Category, Article

from shop.models import Shop,Product,Collection,Order,Invoice,Inventory

from shipping.models import Model,Zone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.decorators.csrf import csrf_exempt
from basket.models import Basket,Checkout
from django.contrib.sessions.models import Session
from basket.models import Checkout


#from rest_framework.permissions import IsAuthenticated,AllowAny
#from rest_framework.decorators import api_view,authentication_classes,permission_classes
#from drf_haystack.viewsets import HaystackViewSet
#from haystack.generic_views import SearchView
#from shop.serializers import SearchSerializer
from drf_haystack.filters import HaystackAutocompleteFilter
import json

from forms import SearchForm
from haystack.query import SearchQuerySet,EmptySearchQuerySet
from django.shortcuts import redirect
from django.contrib.sessions.models import Session


import stripe
import requests


import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from profile.models import Profile,Address
from django.utils import timezone






from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import json
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basket.models import Buyer,Seller
from django.contrib.auth import get_user_model

from shop.models import Customer,Shop
from django.conf import settings

User = get_user_model()


@login_required
def change_password(request):
    profile = request.user
    searchForm = SearchForm()
    subscribersForm = SubscribersForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form,'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile
    })




@login_required
def history(request):
	page = request.GET.get('page', 1)
	template = 'history.html'
	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	order_list = request.user.order_set.all().reverse()
	paginator = Paginator(order_list, 10)

	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)

	profile = request.user
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile,'orders':orders }
	return render(request,template,context)	


@login_required
def address(request):
	page = request.GET.get('page', 1)
	template = 'address.html'
	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	address_list = request.user.address_set.all()
	paginator = Paginator(address_list, 10)

	try:
		address = paginator.page(page)
	except PageNotAnInteger:
		address = paginator.page(1)
	except EmptyPage:
		address = paginator.page(paginator.num_pages)

	profile = request.user
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile, 'address':address }

	return render(request,template,context)	



@login_required
def add_address(request):
	template = 'address_add.html'

	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	form = AddAddressForm()
	if request.method == 'POST':
		form = AddAddressForm(request.POST,user = request.user)
		if form.is_valid():
			address = Address.objects.create(
				profile  = request.user,
				name     = form.cleaned_data['name'],
				country  = form.cleaned_data['country'],
				province = form.cleaned_data['province'],
				city     = form.cleaned_data['city'],
				zip_code = form.cleaned_data['zip_code'],
				address  = form.cleaned_data['address'],
				geom     = None
				)
			address.save
			return redirect('/address/')

	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'form':form }
	return render(request,template,context)	


@login_required
def edit_address(request,id):
	template = 'address_edit.html'

	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	
	user_address = Address.objects.get(pk=id)
	data = {'name': user_address.name , 'country': user_address.country ,'province': user_address.province ,'city': user_address.city ,'zip_code': user_address.zip_code ,'address': user_address.address}
	form = EditAddressForm(data, user = request.user , address = user_address)

	if request.method == 'POST':
		form = EditAddressForm(request.POST, user = request.user , address = user_address)
		if form.is_valid():
			user_address.name     = form.cleaned_data['name']
			user_address.country  = form.cleaned_data['country']
			user_address.province = form.cleaned_data['province']
			user_address.city     = form.cleaned_data['city']
			user_address.zip_code = form.cleaned_data['zip_code']
			user_address.address  = form.cleaned_data['address']
			user_address.save()
			return redirect('/address/')
		#print form.errors

	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'form':form }
	return render(request,template,context)	


@login_required
def profile(request):
	template = 'profile.html'

	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	profile = request.user
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile }



	return render(request,template,context)	

@login_required
def edit_profile(request):
	template = 'profile_edit.html'

	data = { 'first_name': request.user.first_name, 'last_name':request.user.last_name,'email':request.user.email ,'mobile':request.user.mobile.as_national,'country_code':request.user.mobile.country_code  }

	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	profile = request.user
	form = EditProfileForm(data)
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile , 'form':form }

	if request.method == 'POST':
		form = EditProfileForm(request.POST)
		if form.is_valid():
			mobile = '+' + form.cleaned_data['country_code'] + form.cleaned_data['mobile']

			'''  if email Change Re verifi the user email '''
			if not str(profile.email) == str(form.cleaned_data['email']):
				from rest_framework.authtoken.models import Token
				from email_confirmation.tasks import confirm_user_email_task
				try:
					user = Profile.objects.get(email=form.cleaned_data['email'])
				except Profile.DoesNotExist:
					user = request.user
					user.email_verified = False
					user.save()
					new_email = form.cleaned_data['email']
					confirmation_key = user.add_email_if_not_exists(new_email)
					confirm_user_email_task.apply_async((new_email,),countdown=1)
				else:
					error = "That EMAIL is already registered, please select another."
					context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile , 'form':form ,'error': error}
					return render(request,template,context)

			'''  if mobile Change Re verifi the user mobile '''
			#print profile.mobile
			#print mobile
			if not str(profile.mobile) in str(mobile):
				from mobile_confirmation.tasks import confirm_user_mobile_task

				try:
					user = Profile.objects.get(mobile=mobile)
				except Profile.DoesNotExist:
					user = request.user
					user.mobile_verified = False
					user.save()
					new_mobile = mobile
					confirmation_key = user.add_mobile_if_not_exists(new_mobile)
					#confirm_user_mobile_task.apply_async((new_mobile,),countdown=1)
				else:
					error = "That MOBILE is already registered, please select another."
					context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm , 'profile':profile , 'form':form ,'error': error}
					return render(request,template,context)

			user_profile               = Profile.objects.get(pk=profile.id)
			user_profile.first_name    = form.cleaned_data['first_name']
			user_profile.last_name     = form.cleaned_data['last_name']
			user_profile.email         = form.cleaned_data['email']
			user_profile.mobile        = mobile
			user_profile.save()
			return redirect('/profile/')
	return render(request,template,context)	

def home(request):
	template = 'home.html'
	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	shops = Shop.objects.filter(featured = True )
	article      = Article.objects.filter(recommended='True')
	product_list = Product.objects.filter(language="English")
	new_arrivals = Product.objects.filter(language="English").order_by("created_date").reverse()
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm,'article': article , 'shops':shops, 'products': product_list , 'new_arrivals':new_arrivals}
	return render(request,template,context)

def add_to_cart(request,product):
	loginForm=LoginForm()
	searchForm = SearchForm()
	subscribersForm = SubscribersForm()
	session = Session.objects.get(pk=request.session.session_key)
	product = Product.objects.get(pk=product)
	shop = product.shop
	orders = request.basket.order_set.all()
	max_quantity = 0
	if request.method == 'POST':
		form = addToCartForm(request.POST,product=product)
		if form.is_valid():
			''' We confirm if all the basket orders is from the same Shop, as we will need to make invoice soon  '''
			if request.basket.order_set.all():
				product_shop = product.shop.id
				basket_shop  = request.basket.order_set.all().first().shop.id
				if not product_shop == basket_shop:
					error =  "We can not mix orders from different store at this time"
					template     = 'cart.html'
					context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'error':error}
					return render(request,template,context)

			if not request.user.is_authenticated:
				order = request.basket.order_set.create(session=session,shop=shop,product=product,quantity=form.cleaned_data["quantity"],with_option=product.with_variant,coupon=None)
			if request.user.is_authenticated:
				order = request.basket.order_set.create(owner=request.user, session=session,shop=shop,product=product,quantity=form.cleaned_data["quantity"],with_option=product.with_variant,coupon=None)
			if product.with_variant:
				variant = product.variant_set.all()
				target_variant = ()
				for o in variant:
					if str(o.id) == form.cleaned_data[o.name]:
						target_variant = target_variant + ( str(o.id), ) 
						new_option = order.option_set.create(
							name  = o.name,
							value = o.value,
							price = o.price,
							usd_price = o.usd_price
							)
						new_option.save()
				warehouse = shop.warehouse_set.all()
				for o in warehouse:
					try:
						shop.inventory_set.get( product=product, warehouse = o , variant = target_variant )
					except Inventory.DoesNotExist:
						max_quantity = max_quantity + 0
					else:
						item = shop.inventory_set.get( product=product, warehouse = o , variant = target_variant )
						max_quantity = max_quantity + item.quantity
						order.max_quantity = max_quantity
						if order.warehouse.all().count() == 0:
							order.warehouse.add(o)
						order.save()
						if order.quantity > item.quantity:
							order.quantity = item.quantity
							order.save()
			if not product.with_variant:
				warehouse = shop.warehouse_set.all()
				for o in warehouse:
					try:
						shop.inventory_set.get( product=product, warehouse = o )
					except Inventory.DoesNotExist:
						max_quantity = max_quantity + 0
					else:
						item = shop.inventory_set.get( product=product, warehouse = o )
						max_quantity = max_quantity + item.quantity
						order.max_quantity = max_quantity
						if order.warehouse.all().count() == 0:
							order.warehouse.add(o)
						order.save()
				if order.quantity > item.quantity:
					order.quantity = item.quantity
					order.save()
	return redirect('/cart/')


def remove_from_cart(request,order):
	order = Order.objects.get(pk=order)
	if order.with_option:
		option = order.option_set.all()
		for o in option:
			option.delete()
	order.delete()
	return redirect('/cart/')
def cart(request):

	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	form = UpdateCartForm()

	#print request.basket.order_set.all().first().shop
	template     = 'cart.html'
	context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'form':form }

	if request.method == 'POST':
		form = UpdateCartForm(request.POST)
		if form.is_valid():
			order = Order.objects.get(pk=form.cleaned_data['order'])
			order.quantity =form.cleaned_data['quantity']
			order.save()
	return render(request,template,context)


def product(request,shop,product):
    from shop.models import Shop,Product
    template = '404.html'
    loginForm=LoginForm()
    subscribersForm = SubscribersForm()
    searchForm = SearchForm()
    

    context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }

    #category_name = categorie.replace ("-", " ")
    product_name = product.replace ("-", " ")

    try:
        queryset = Shop.objects.get(slug=shop)
    except Shop.DoesNotExist:
        return render(request,template,context)

    shop = Shop.objects.get(slug = shop)
    ''' Did this category include this product ? '''
    try:
        queryset = Product.objects.filter(shop=shop ,name = product_name )
    except Product.DoesNotExist:
        return render(request,template,context)

    product = Product.objects.get(shop=shop , name = product_name )
    form = addToCartForm(product=product)
    related = shop.product_set.all()

    template = 'product.html'
    context  = { 'loginForm': loginForm, 'subscribersForm': subscribersForm ,'searchForm':searchForm, 'product':product,'related':related, 'form':form }

    return render(request,template,context)



def collection(request,shop,collection):
	store = Shop.objects.get(slug = shop)
	collection_name = collection.replace ("-", " ")
	target_collection = Collection.objects.get(shop=store  , name= collection_name )
	product = target_collection.products.all()
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	template = 'collection.html'
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'shop': store ,'searchForm':searchForm, 'collection':target_collection , 'product': product}
	return render(request,template,context)


def shop(request,shop):
	store = Shop.objects.get(slug = shop)
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	template = 'shop.html'
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'shop': store,'searchForm':searchForm }
	return render(request,template,context)

def shipping(request,shop):
	store = Shop.objects.get(slug = shop)
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()

	model = store.model_set.all()
	template = 'shipping.html'
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'shop': store,'searchForm':searchForm,'model':model }
	return render(request,template,context)

def location(request,shop):
	store = Shop.objects.get(slug = shop)
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()

	model = store.model_set.all()
	template = 'location.html'
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'shop': store,'searchForm':searchForm,'model':model }
	return render(request,template,context)



@csrf_exempt
def finish(request):
	data = { "errors": { "state":"state did not exist", "token":"token did not exist" } }
	return HttpResponse( status=200 )

def pay(request,checkout):

	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	key = stripe.publishable_key
	form = PayForm()
	template     = 'pay.html'
	
	user_checkout = Checkout.objects.get(pk= checkout)

	total_price  = user_checkout.rate + request.basket.usd
	context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'key':key , 'form' :form, 'checkout': user_checkout, 'total_price': total_price } 

	if user_checkout.status == True :
		template     = 'charge.html'
		context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
		return render(request,template,context)

	if request.method == 'POST':
		form = PayForm(request.POST)

		if form.is_valid():
			if request.user.is_authenticated:
				user = request.user
				if user.stripe_customer_id:
					customer = stripe.Customer.retrieve(user.stripe_customer_id)
					user_checkout.stripe_customer_id = user.stripe_customer_id
					user_checkout.save()
				else:
					customer = stripe.Customer.create(
						email=user_checkout.email,
						source=form.cleaned_data['stripeToken']
						)
					user.stripe_customer_id = customer["id"]
					user.save()
					user_checkout.stripe_customer_id = user.stripe_customer_id
					user_checkout.save()
			else:
				all_user_checkout = Checkout.objects.filter(email=user_checkout.email)
				stripe_customer_id = None
				for o in all_user_checkout:
					if o.stripe_customer_id :
						stripe_customer_id = o.stripe_customer_id
				if stripe_customer_id:
					customer_id = stripe_customer_id
					customer = stripe.Customer.retrieve(customer_id)
					user_checkout.stripe_customer_id = customer["id"]
					user_checkout.save()
				else:
					customer = stripe.Customer.create(
						email=user_checkout.email,
						source=form.cleaned_data['stripeToken']
						)
					user_checkout.stripe_customer_id = customer["id"]
					user_checkout.save()


			if request.basket.usd > 0.50:
				charge = stripe.Charge.create(
					customer=customer.id,
					amount=str(int(total_price)*100),
					currency='usd',
					description='Ftrina Charge'
					)

			user_checkout.status = True
			user_checkout.save()

			shop    = Shop.objects.get(pk=request.basket.order_set.all().first().shop.id)
			basket  = request.basket
			orders  = basket.order_set.all()

			invoice = Invoice.objects.create(paid = True)
			invoice.save()
			#print dir(invoice)

			seller = Seller.objects.create(
				first_name = shop.default_contact.first_name,last_name = shop.default_contact.last_name ,email = shop.default_contact.email,
				mobile = shop.default_contact.mobile,address= shop.address,city=shop.city,zip_code=shop.zip_code,
				country=shop.country,province = shop.province)
			seller.save()
			buyer = Buyer.objects.create(
				first_name = user_checkout.first_name ,last_name = user_checkout.last_name ,
				email = user_checkout.email ,mobile = user_checkout.mobile ,address = user_checkout.address,
				city = user_checkout.city,zip_code = user_checkout.zip_code ,
				country = user_checkout.country ,province = user_checkout.province, notes = user_checkout.notes  )
			buyer.save()
			invoice.buyer  = buyer
			invoice.seller = seller
			invoice.shop   = shop
			invoice.save()
			if request.user.is_authenticated:
				invoice.owner = request.user
				invoice.save()

			for order in orders:
				order.status = True
				order.basket = None
				order.invoice      = invoice
				order.stage  = "pending"
				order.checkout = user_checkout
				order.timestamp = timezone.now()

				if request.user.is_authenticated :
					order.owner = request.user
					#order.address = 
				if not request.user.is_authenticated:
					order.guest  = True

				order.save()
			
			try:
				Customer.objects.get(shop=shop, mobile=buyer.mobile, email=buyer.email)
			except Customer.DoesNotExist:
				new_customer = Customer.objects.create(
				first_name = user_checkout.first_name ,last_name = user_checkout.last_name ,
				email = user_checkout.email , mobile = user_checkout.mobile, orders=1, country = user_checkout.country, shop = shop)
				new_customer.save()
			else:
				new_customer = Customer.objects.get(shop=shop, mobile=buyer.mobile, email=buyer.email)
				new_customer.orders = new_customer.orders + 1
				new_customer.save()
			#print dir(request.basket.order_set.all())
			''' send Notification to shop owner '''
			#send_notification(to=str(order.shop.owner.username),title="New Order",message="You Have New Order")

			#print request.basket.order_set.all()
			request.basket_size = 0
			template     = 'charge.html'
			context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
			return render(request,template,context)
		else:
			print form.errors
	return render(request,template,context)


def checkout(request):

	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()

	checkoutForm = CheckoutForm()
	template     = 'checkout.html'


	if request.user.is_authenticated:
		address= request.user.address_set.all()
		form = UserCheckoutForm( user = request.user )
	else:
		address = ''
		form = UserCheckoutForm()


	context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm,'checkoutForm':checkoutForm , 'address':address , 'form':form }
	if request.method == 'POST':
		if not request.user.is_authenticated:
			form = CheckoutForm(request.POST)
			if form.is_valid():
				session       = Session.objects.get(pk=request.session.session_key)

				new_checkout      = Checkout.objects.create(
					first_name    = form.cleaned_data['first_name'],
					last_name     = form.cleaned_data['last_name'],
					email         = form.cleaned_data['email'],
					mobile        = form.cleaned_data['mobile'],
					address       = form.cleaned_data['address'],
					city          = form.cleaned_data['city'],
					zip_code      = form.cleaned_data['zip_code'],
					country       = form.cleaned_data['country'],
					province      = form.cleaned_data['province'],
					notes         = form.cleaned_data['notes'],
					session       = session
					)
				new_checkout.save()
				return redirect('/checkout/delivery/' + str(new_checkout.id) + '/' )
			else:
				#print form.errors
				return render(request,template,context)

		if request.user.is_authenticated:
			form = UserCheckoutForm(request.POST)
			if form.is_valid():
				if request.user.first_name == '' or request.user.last_name == '' or request.user.mobile == '':
					error = "Please update your profile information before before ordering"
					context= { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm,'checkoutForm':checkoutForm , 'address':address , 'form':form,  'error':error }
					return render(request,template,context)

				session       = Session.objects.get(pk=request.session.session_key)
				user_address  = Address.objects.get(name=form.cleaned_data['address'], profile = request.user )
				#print "-----",user_address

				new_checkout      = Checkout.objects.create(
					first_name    = request.user.first_name,
					last_name     = request.user.last_name,
					email         = request.user.email,
					mobile        = request.user.mobile,
					address       = user_address.address,
					city          = user_address.city,
					zip_code      = user_address.zip_code,
					country       = user_address.country,
					province      = user_address.province,
					notes         = form.cleaned_data['notes'],
					session       = session
					)
				new_checkout.save()
				#request.checkout = new_checkout
				return redirect('/checkout/delivery/' + str(new_checkout.id) + '/' )
			else:
				#print form.errors
				#print form.data
				return render(request,template,context)
	return render(request,template,context)

def checkout_shipping(request,checkout):
	user_checkout = Checkout.objects.get(pk=checkout)

	template = 'checkout_shipping.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	form = DeliveryForm()
	if request.method == 'POST':
		if request.POST.get('shipping'):
			user_choices   = request.POST.get('shipping').split("@")
			#user_checkout.carrier_account_id = user_choices[0]
			user_checkout.shipment_id        = user_choices[0]
			user_checkout.rate_id            = user_choices[1]
			user_checkout.rate               = user_choices[2]
			user_checkout.currency           = user_choices[3]
			user_checkout.carrier            = user_choices[4]
			user_checkout.save()
			return redirect('/cart/pay/' + str(user_checkout.id) + '/' )
	order_list       =  request.basket.order_set.all()
	shipper_accounts =  []
	first_warehouse  = request.basket.order_set.all().first().warehouse.all().first()
	''' We confirm if all the basket orders is from the same warehouse '''
	for order in order_list:
		warehouse_list = order.warehouse.all()
		for warehouse in warehouse_list:
			if not warehouse.id == first_warehouse.id:
				order.delete()
	couriers = first_warehouse.courier_set.all()
	for courier in couriers:
		shipper_accounts.append( courier.easypost_id  )

	import easypost
	from django.conf import settings
	easypost.api_key = getattr(settings, "EASYPOST_API_KEY", None)
	#print easypost.api_key

	customs_info = easypost.CustomsInfo.create(
		eel_pfc='NOEEI 30.37(a)', # If the value of the goods is less than $2,500, then you pass the following EEL code: "NOEEI 30.37(a)"
		contents_type='merchandise',
		contents_explanation='',
		customs_certify=True,
		customs_signer='Ftrina Limited',
		non_delivery_option='abandon',
		restriction_type='none',
		restriction_comments='',
		customs_items=request.basket.customs_item
		)
	user_checkout.customs_info = customs_info.id
	user_checkout.save()

	shipment = easypost.Shipment.create(
		to_address=user_checkout.ship_to,
		from_address=first_warehouse.ship_from,
		parcel=request.basket.parcels,
		customs_info = customs_info,
		carrier_accounts = shipper_accounts
		)

	response = shipment.get_rates()
	#print response.rates
	print shipment.id
	rates = response.rates
	choices = []
	fixer_api_key = getattr(settings, "FIXER_API_KEY", None)
	for rate in rates:
		amount = float(rate['rate']) / 100 * 0.5 + float(rate['rate'])
		url = 'http://data.fixer.io/api/convert?access_key=' + fixer_api_key + '&from=' + str(rate['currency']) + '&to=USD&amount=' + str(amount)
		fixer_response = requests.request('GET', url)
		json_response = json.loads(fixer_response.text)
		name  = str(rate['carrier']) + ' ' +  str( int(json_response['result']) ) + ' ' + 'USD' 
		value = str(shipment.id)  + '@' + str(rate['id'])  + '@' +   str( int(json_response['result']) ) + '@' +  'USD'  + '@' + str(rate['carrier'])  
		choices.append( ( value  , name  ) )
	form.fields["shipping"].choices = choices
	context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'data':user_checkout, 'rates':rates, 'form': form }
	return render(request,template,context)

from datetime import date
from haystack.generic_views import SearchView

class search(SearchView):
    """My custom search view."""

    form_class=SearchForm
    template='search.html',
    queryset = SearchQuerySet()
    loginForm=LoginForm()
    searchForm = SearchForm()
    subscribersForm = SubscribersForm()

    filter_backends = [HaystackAutocompleteFilter]
    index_models = [Shop,Product,Category]


    def get_queryset(self):
        queryset = super(search, self).get_queryset()
        return queryset.filter( name = self.request.GET.get('q') )

    def get_context_data(self, *args, **kwargs):
        context = super(search, self).get_context_data(*args, **kwargs)
        context['loginForm'] = self.loginForm
        context['subscribersForm'] = self.subscribersForm
        context['searchForm'] = self.searchForm
        context['total'] = len(self.queryset)
        return context

def about(request):
	template = 'about.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def privacy(request):
	template = 'privacy.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def terms(request):
	template = 'terms.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def cookie(request):
	template = 'cookie.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def faq(request):
	template = 'faq.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def refund(request):
	template = 'refund.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def prohibited(request):
	template = 'prohibited.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)



def directory(request):
	template = 'directory.html'
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm }
	return render(request,template,context)

def loginView(request):
	template = 'login.html'
	certificate = {}
	certificate.update(csrf(request))
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'searchForm':searchForm }

	if request.method == 'POST':
		form = LoginForm(request.POST)
		#print request.POST
		if form.is_valid():
			username    = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				#print request.session.session_key
				#print dir(user.session_set)

				session = Session.objects.get(pk=request.session.session_key)
				basket  =  Basket.objects.get(session=session)
				orders = user.order_set.all()
				for order in orders:
					order.basket = basket
					order.save()
				#print basket.session

				Basket.objects.update(owner=user)
				#basket.owner=user
				basket.save()
				#print dir(basket)
				#print user.session_set.update_or_create(session=session,user=user)

				login(request, user)
				# Redirect to a success page.
				return HttpResponseRedirect('/')
			else:
				# Return an 'invalid login' error message.
				#print form.errors
				return render(request,template,context)
		else:
			return render(request,template,context)
	else:
		form = LoginForm()
		return render(request,template,context)

def logoutView(request):
	
	logout(request)
	return HttpResponseRedirect('/')


def registerView(request):

	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
		
	template = 'register.html'
	certificate = {}
	certificate.update(csrf(request))
	registerForm=RegisterForm()
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	context = { 'registerForm': registerForm, 'loginForm': loginForm , 'subscribersForm': subscribersForm,'searchForm':searchForm }

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			
			#print form.cleaned_data['phone']
			user = User.objects.create_user(username=form.cleaned_data['username'],  email = form.cleaned_data['email'],  password = form.cleaned_data['password'], mobile = form.cleaned_data['phone'] )
			user.save()
			from email_confirmation.tasks  import  confirm_user_email_task
			confirm_user_email_task.apply_async((form.cleaned_data['email'],),countdown=1)
			template = 'register_done.html'
			return render(request,template,context)
		else:
			#print form.errors
			registerForm=RegisterForm(request.POST)
			context = { 'registerForm': registerForm, 'loginForm': loginForm , 'subscribersForm': subscribersForm,'searchForm':searchForm }
			return render(request,template,context)
	else:
		'''  User Is Not Ubmitting the form, Show them a blank registration form  '''
		return render(request,template,context)

def register_confirms_view(request,code):

	from django.core.exceptions import ObjectDoesNotExist
	from email_confirmation.models import UserEmailConfirmation, EmailAddress
	from email_confirmation.signals import (
		email_confirmed, unconfirmed_email_created, primary_email_changed,)

	template = 'confirm.html'
	certificate = {}
	certificate.update(csrf(request))
	registerForm=RegisterForm()
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()
	#print code
	context = { 'registerForm': registerForm, 'loginForm': loginForm , 'subscribersForm': subscribersForm,'searchForm':searchForm }

	try:
		key = EmailAddress.objects.get(key=code)
	except ObjectDoesNotExist:
		template = 'invalid_confirm.html' 
		return render(request,template,context)
	else:
		key = EmailAddress.objects.get(key=code)
		user = Profile.objects.get(email=key.email)
		user.confirm_email(user.email_confirmation_key)
		user.email_verified = True
		user.save()
	
	return render(request,template,context)

