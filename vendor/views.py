# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import vendor_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.models import Order,Invoice,Branch,WareHouse,Collection,Product,Variant,Shop,Inventory
from vendor.forms import OrdersEditForm,EditBasicInfoForm,EditBusinessInfoForm,EditLocationInfoForm,BranchForm,WareHouseForm,CollectionForm,ProductForm,ContactForm,DefaultContactForm,DefaultWarehouseForm,DefaultCurrencyForm,CreateShipperAccountForm,upsForm,AramexAccountForm,dhlForm,tntForm,FedexAccountForm,variantForm,inventoryForm,addToInventoryForm,editInventoryForm


from .forms import PhotoForm, PhotoDirectForm, PhotoUnsignedDirectForm
from django.views.decorators.csrf import csrf_exempt
from cloudinary.forms import cl_init_js_callbacks
from cloudinary import api # Only required for creating upload presets on the fly
from django.http import JsonResponse,HttpResponse
import json
from album.models import  Image
from django.forms.utils  import ErrorList
import cloudinary
import requests
from ftrina.countries import COURIER_LIST
from django.conf import settings


@vendor_required
def dashboard(request):
	template = 'vendor/dashboard.html'
	d_link = 'active'
	shop = request.user.shop_set.get()
	orders = shop.invoice_set.filter(finished=False)
	context   = { 'd_link': d_link, 'shop':shop,'orders':orders }
	return render(request,template,context)


def visuals(request):
	template = 'vendor/visuals.html'
	v_link = 'active'
	shop = request.user.shop_set.get()
	logo = '<img src="'+ shop.image +'" alt="Your Avatar"><h6 class="text-muted">Click to select</h6>',
	context   = { 'v_link': v_link, 'shop':shop }
	return render(request,template,context)


@vendor_required
def customers(request):
	page = request.GET.get('page', 1)
	shop      = request.user.shop_set.get()
	customers_list = customers = shop.customer_set.all()
	paginator = Paginator(customers_list, 10)

	template  = 'vendor/customers.html'
	c_link    = 'active'
	try:
		customers = paginator.page(page)
	except PageNotAnInteger:
		customers = paginator.page(1)
	except EmptyPage:
		customers = paginator.page(paginator.num_pages)
	context   = { 'c_link': c_link, 'shop':shop, 'customers':customers }
	return render(request,template,context)







''''''



@vendor_required
def products(request):
	page = request.GET.get('page', 1)
	products_list = request.user.shop_set.get().product_set.all()
	paginator = Paginator(products_list, 10)
	template = 'vendor/products.html'
	p_link = 'active'

	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	context   = { 'p_link': p_link , 'products': products }
	return render(request,template,context)



@vendor_required
def products_edit(request,product):
	target_product = Product.objects.get(pk=product)
	shop = request.user.shop_set.get()
	p_link = 'active'
	template = 'vendor/products_edit.html'
	if not target_product.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'p_link': p_link }
		return render(request,template,context)

	data = { 'name': target_product.name, 'keyword':target_product.keywords,'description':target_product.description, 
	'price':target_product.price, 'price_currency':shop.currency,'weight':target_product.weight,
	'origin':target_product.origin,'sku':target_product.sku,
	'cart_description':target_product.cart_description }

	form = ProductForm(data,product= target_product, shop= shop )

	photo_container = []
	variant_data = target_product.characteristics
	photos_data = target_product.images.all()

	for o in photos_data:
		target_image = Image.objects.get(pk=o.id)
		photo_container.append({"id": target_image.id , "url" : target_image.image.build_url(), "caption": target_image.image.public_id + target_image.image.type , "width" : "120px", "delete":"/dashboard/products/upload/delete/"+ str(target_image.id) + "/"  })

	if request.method == 'POST':
		form = ProductForm(request.POST,product= target_product, shop=shop)

		variant_data = json.loads(form.data['variant'])
		if form.data['photos'] and not form.data['photos'] == "[]":
			photos_data = form.data['photos'].split('"')[1::2]
			for o in photos_data:
				target_image = Image.objects.get(pk=o)
				photo_container.append({"id": target_image.id , "url" : target_image.image.build_url(), "caption": target_image.image.public_id + target_image.image.type , "width" : "120px", "delete":"/dashboard/products/upload/delete/"+ str(target_image.id) + "/"  })
		else:
			form.errors['product'] = ErrorList([u"At least one picture is required."] )
			photo_container = ''
			context   = { 'p_link': p_link, 'form':form , 'variant':variant_data , 'photo_container':photo_container}
			return render(request,template,context)

		if form.is_valid():
			target_product.cart_description = form.cleaned_data['cart_description']

			if not form.cleaned_data['keyword']:
				keywords = form.cleaned_data['name']
			else:
				keywords = form.cleaned_data['keyword']

			with_variant = False
			variant_selection = []
			if variant_data:
				for o in variant_data:
					if ',' in o['value']:
						with_variant = True
						variant_selection.append({'name':o['name'], 'value': o['value'] })

			target_product.name = form.cleaned_data['name']
			target_product.keywords = keywords
			target_product.description = form.cleaned_data['description']
			target_product.price = form.cleaned_data['price']
			target_product.weight = form.cleaned_data['weight']
			target_product.origin = form.cleaned_data['origin']
			target_product.sku = form.cleaned_data['sku']
			target_product.with_variant = with_variant
			target_product.characteristics = variant_data
			target_product.save()

			if not shop.currency == "USD":
				fixer_api_key = getattr(settings, "FIXER_API_KEY", None)
				amount = float(target_product.price) / 100 * 0.5 + float(target_product.price)
				url = 'http://data.fixer.io/api/convert?access_key=' + fixer_api_key + '&from=' + str(shop.currency) + '&to=USD&amount=' + str(amount)
				fixer_response = requests.request('GET', url)
				json_response = json.loads(fixer_response.text)
				target_product.usd_price = json_response['result']
				target_product.save()
			else:
				target_product.usd_price = target_product.price
				target_product.save()


			clear_variant =  target_product.variant_set.all()
			for o in clear_variant:
				o.delete()
			old_inventory = target_product.inventory_set.all()
			for o in old_inventory:
				o.delete()
			if variant_selection:
				for o in variant_selection:
					if ',' in o['value']:
						values = o['value'].split(',')
						for obj in values:
							new_variant = target_product.variant_set.create(
								name = o['name'],
								value = obj,
								price = 0,
								usd_price = 0,
								)
							new_variant.save()
			if photo_container:
				for o in photo_container:
					target_image = Image.objects.get(pk=o["id"])
					target_image.shop = shop
					target_image.product = target_product
					target_image.is_product = True
					target_image.confirmed = True
					target_image.save()
			return redirect('/dashboard/products/')
		#else:
			#print form.errors
	context   = { 'p_link': p_link, 'form':form,'photo_container':photo_container,'variant':variant_data }
	return render(request,template,context)


@vendor_required
def products_add(request):
	shop = request.user.shop_set.get()
	p_link = 'active'
	variant = []
	photo_container = []
	variant_data = []
	data =  {'variant':variant,'price_currency':shop.currency}
	template = 'vendor/products_add.html'
	form = ProductForm(shop=shop)
	if request.method == 'POST':
		form = ProductForm(request.POST,shop= shop)
		variant_data = json.loads(form.data['variant'])
		if form.data['photos'] and not form.data['photos'] == "[]":
			photos_data = form.data['photos'].split('"')[1::2]
			for o in photos_data:
				target_image = Image.objects.get(pk=o)
				photo_container.append({"id": target_image.id , "url" : target_image.image.build_url(), "caption": target_image.image.public_id + target_image.image.type , "width" : "120px", "delete":"/dashboard/products/upload/delete/"+ str(target_image.id) + "/"  })
		else:
			form.errors['product'] = ErrorList([u"At least one picture is required."] )
			photo_container = ''
			context   = { 'p_link': p_link, 'form':form , 'variant':variant_data , 'photo_container':photo_container}
			return render(request,template,context)

		if form.is_valid():
			if not form.cleaned_data['keyword']:
				keywords = form.cleaned_data['name']
			else:
				keywords = form.cleaned_data['keyword']

			with_variant = False
			variant_selection = []
			if variant_data:
				for o in variant_data:
					if ',' in o['value']:
						with_variant = True
						variant_selection.append({'name':o['name'], 'value': o['value'] })


			new_product = shop.product_set.create(
				name = form.cleaned_data['name'],
				keywords = keywords,
				description = form.cleaned_data['description'],
				cart_description = form.cleaned_data['cart_description'],
				price = form.cleaned_data['price'],
				price_currency = shop.currency,
				weight = form.cleaned_data['weight'],
				origin = form.cleaned_data['origin'],
				sku = form.cleaned_data['sku'],
				min_order = 1,
				list_as = 'new',
				language = 'English',
				with_variant = with_variant,
				characteristics = variant_data,
				)
			new_product.save()
			if not shop.currency == "USD":
				fixer_api_key = getattr(settings, "FIXER_API_KEY", None)
				amount = float(new_product.price) / 100 * 0.5 + float(new_product.price)
				url = 'http://data.fixer.io/api/convert?access_key=' + fixer_api_key + '&from=' + str(shop.currency) + '&to=USD&amount=' + str(amount)
				fixer_response = requests.request('GET', url)
				json_response = json.loads(fixer_response.text)
				new_product.usd_price = int(json_response['result'])
				new_product.save()
			else:
				new_product.usd_price = new_product.price
				new_product.save()

			if variant_selection:
				for o in variant_selection:
					if ',' in o['value']:
						values = o['value'].split(',')
						for obj in values:
							new_variant = new_product.variant_set.create(
								name = o['name'],
								value = obj,
								price = 0,
								usd_price = 0,
								)
							new_variant.save()
			if photo_container:
				for o in photo_container:
					target_image = Image.objects.get(pk=o["id"])
					target_image.shop = shop
					target_image.product = new_product
					target_image.is_product = True
					target_image.confirmed = True
					target_image.save()
			return redirect('/dashboard/products/')
		#else:
			#print form.errors
	context   = { 'p_link': p_link, 'form':form , 'variant':variant_data , 'photo_container':photo_container}
	return render(request,template,context)



@vendor_required
def products_duplicate(request,product):
	target_product = Product.objects.get(pk=product)
	shop = request.user.shop_set.get()
	p_link = 'active'
	if not target_product.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'p_link': p_link }
		return render(request,template,context)
	try:
		shop.product_set.get( name = "Copy " + target_product.name )
	except Product.DoesNotExist:
		name = "Copy " + target_product.name
	else:
		import string
		import random
		name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
	new_product = shop.product_set.create(
		name = name ,
		keywords = target_product.keywords,
		description = target_product.description,
		cart_description = target_product.cart_description,
		price = target_product.price,
		price_currency = shop.currency,
		weight = target_product.weight,
		origin = target_product.origin,
		sku = target_product.sku,
		min_order = 1,
		list_as = 'new',
		language = 'English',
		with_variant = target_product.with_variant,
		characteristics = target_product.characteristics,
		usd_price = target_product.usd_price,
		)
	new_product.save()

	if target_product.with_variant:
		variant_selection = target_product.variant_set.all()
		for o in variant_selection:
			new_variant = new_product.variant_set.create(
				name = o.name,
				value = o.value,
				price = o.price,
				usd_price = o.usd_price,
				)
			new_variant.save()
	return redirect('/dashboard/products/edit/' + str(new_product.id) + '/' )

@vendor_required
def products_delete(request,product):
	target_product = Product.objects.get(pk=product)
	shop = request.user.shop_set.get()
	p_link = 'active'
	if not target_product.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'p_link': p_link }
		return render(request,template,context)
	else:
		from album.tasks import delete_image_by_public_id
		from album.models import Image
		images = target_product.images.all()
		variant = target_product.variant_set.all()
		inventory = target_product.inventory_set.all()
		for image in images:
			delete_image_by_public_id.apply_async((  str( image.public_id)  ,),countdown=1)
		for o in variant:
			o.delete()
		for o in inventory:
			o.delete()
		target_product.delete()

		return redirect('/dashboard/products/')


def inventory(request):
	page = request.GET.get('page', 1)
	template = 'vendor/inventory.html'
	in_link = 'active'
	shop = request.user.shop_set.get()
	target_inventory = shop.inventory_set.all()
	paginator = Paginator(target_inventory, 100)
	try:
		inventory = paginator.page(page)
	except PageNotAnInteger:
		inventory = paginator.page(1)
	except EmptyPage:
		inventory = paginator.page(paginator.num_pages)
	context   = { 'in_link': in_link, 'shop':shop,'inventory':inventory }
	return render(request,template,context)



@vendor_required
def inventory_add(request,product):
	shop = request.user.shop_set.get()
	target_product = shop.product_set.get(id=product)
	form = addToInventoryForm(product=target_product)
	if request.method == 'POST':
		form = addToInventoryForm(request.POST,product=target_product)
		if form.is_valid():
			''' We need to know if the product available in the inventory '''
			if not target_product.with_variant:
				try:
					shop.inventory_set.get(product=target_product, warehouse = form.cleaned_data['warehouse'] )
				except Inventory.DoesNotExist:
					new_item = shop.inventory_set.create(
						product      = target_product,
						quantity     = form.cleaned_data['quantity'],
						warehouse    = form.cleaned_data['warehouse']
						)
					new_item.save()
				else:
					item = shop.inventory_set.get(product=target_product, warehouse = form.cleaned_data['warehouse'] )
					item.product   = target_product
					item.quantity  = form.cleaned_data['quantity']
					item.warehouse = form.cleaned_data['warehouse']
					item.save()
			if target_product.with_variant:
				variant = target_product.variant_set.all()
				target_variant = ()
				for o in variant:
					if str(o.id) == form.cleaned_data[o.name]:
						#new_item.variant.add(o)
						target_variant = target_variant + ( str(o.id), ) 
				try:
					shop.inventory_set.get( product=target_product, warehouse = form.cleaned_data['warehouse'], variant = target_variant  )
				except Inventory.DoesNotExist:
					new_item = shop.inventory_set.create(
						product      = target_product,
						quantity     = form.cleaned_data['quantity'],
						warehouse    = form.cleaned_data['warehouse']
						)
					new_item.save()
					for o in variant:
						if str(o.id) == form.cleaned_data[o.name]:
							new_item.variant.add(o)
				else:
					item = shop.inventory_set.get( product=target_product, warehouse = form.cleaned_data['warehouse'], variant = target_variant  )
					item.quantity  = form.cleaned_data['quantity']
					item.warehouse = form.cleaned_data['warehouse']
					item.save()
			return redirect('/dashboard/inventory/' )
	in_link = 'active'
	template = 'vendor/inventory_add.html'
	context   = { 'in_link': in_link,'form':form}
	return render(request,template,context)

@vendor_required
def inventory_delete(request,inventory):
	shop = request.user.shop_set.get()
	target_item = shop.inventory_set.get(id=inventory)
	target_product = target_item.product
	in_link = 'active'
	if not target_product.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'in_link': in_link }
		return render(request,template,context)
	else:
		target_item.delete()
		return redirect('/dashboard/inventory/')


@vendor_required
def inventory_edit(request,inventory):
	shop = request.user.shop_set.get()
	target_item = shop.inventory_set.get(id=inventory)
	target_product = target_item.product
	data = { 'quantity': target_item.quantity, 'warehouse':target_item.warehouse.id }
	form = editInventoryForm(data,product=target_product)
	if request.method == 'POST':
		form = editInventoryForm(request.POST,product=target_product )
		if form.is_valid():
			target_item.quantity  = form.cleaned_data['quantity']
			target_item.warehouse = form.cleaned_data['warehouse']
			target_item.save()
			return redirect('/dashboard/inventory/' )
	in_link = 'active'
	template = 'vendor/inventory_edit.html'
	context   = { 'in_link': in_link,'form':form}
	return render(request,template,context)



@vendor_required
def products_variant(request,product):
	page = request.GET.get('page', 1)
	target_product = Product.objects.get(pk=product)
	shop = request.user.shop_set.get()
	variants_list = target_product.variant_set.all()
	paginator = Paginator(variants_list, 30)
	p_link = 'active'
	template = 'vendor/products_variant.html'
	try:
		variants = paginator.page(page)
	except PageNotAnInteger:
		variants = paginator.page(1)
	except EmptyPage:
		variants = paginator.page(paginator.num_pages)
	context   = { 'p_link': p_link,'variants':variants }
	return render(request,template,context)


@vendor_required
def variant_edit(request,variant):
	target_variant = Variant.objects.get(id=variant)
	target_product = target_variant.product
	shop = request.user.shop_set.get()
	form = variantForm()
	if request.method == 'POST':
		form = variantForm(request.POST)
		if form.is_valid():
			target_variant.price = form.cleaned_data['price']
			if not shop.currency == "USD":
				fixer_api_key = getattr(settings, "FIXER_API_KEY", None)
				amount = float(form.cleaned_data['price']) / 100 * 0.5 + float(form.cleaned_data['price'])
				url = 'http://data.fixer.io/api/convert?access_key=' + fixer_api_key + '&from=' + str(shop.currency) + '&to=USD&amount=' + str(amount)
				fixer_response = requests.request('GET', url)
				json_response = json.loads(fixer_response.text)
				target_variant.usd_price = json_response['result']
			else:
				target_variant.usd_price = form.cleaned_data['price']
			target_variant.save()
			return redirect('/dashboard/products/variant/' + str(target_variant.product.id) )
	p_link = 'active'
	template = 'vendor/variant_edit.html'
	context   = { 'p_link': p_link,'form':form,'product':target_product}
	return render(request,template,context)

@vendor_required
def warehouse(request):
	page = request.GET.get('page', 1)
	warehouse_list = request.user.shop_set.get().warehouse_set.all()
	paginator = Paginator(warehouse_list, 10)
	template = 'vendor/warehouse.html'
	w_link = 'active'

	try:
		warehouse = paginator.page(page)
	except PageNotAnInteger:
		warehouse = paginator.page(1)
	except EmptyPage:
		warehouse = paginator.page(paginator.num_pages)

	context   = { 'w_link': w_link , 'warehouse':warehouse }
	return render(request,template,context)

@vendor_required
def warehouse_edit(request,warehouse):
	target_warehouse = WareHouse.objects.get(pk=warehouse)
	shop = request.user.shop_set.get()
	w_link = 'active'
	data = { 'name': target_warehouse.name, 'country':target_warehouse.country,'province':target_warehouse.province, 'city':target_warehouse.city, 'zip_code':target_warehouse.zip_code,'address':target_warehouse.address,'geom':target_warehouse.geom}
	form = WareHouseForm(data, shop = shop)

	if not target_warehouse.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'w_link': w_link }
		return render(request,template,context)

	if request.method == 'POST':
		form = WareHouseForm(request.POST, shop = shop, warehouse = target_warehouse )
		if form.is_valid():
			target_warehouse.name     = form.cleaned_data['name']
			target_warehouse.country  = form.cleaned_data['country']
			target_warehouse.province = form.cleaned_data['province']
			target_warehouse.city     = form.cleaned_data['city']
			target_warehouse.zip_code = form.cleaned_data['zip_code']
			target_warehouse.address  = form.cleaned_data['address']
			target_warehouse.geom     = form.cleaned_data['geom']
			target_warehouse.save()
			return redirect('/dashboard/warehouse/')
	template = 'vendor/warehouse_edit.html'
	context   = { 'w_link': w_link, 'form':form }
	return render(request,template,context)


@vendor_required
def warehouse_add(request):
	shop = request.user.shop_set.get()
	data = { 'shop': shop }
	w_link = 'active'
	form = WareHouseForm()
	if request.method == 'POST':
		form = WareHouseForm(request.POST,shop = shop)
		if form.is_valid():
			new_branch = WareHouse.objects.create(
				shop     = shop,
				name     = form.cleaned_data['name'],
				country  = form.cleaned_data['country'],
				province = form.cleaned_data['province'],
				city     = form.cleaned_data['city'],
				zip_code = form.cleaned_data['zip_code'],
				address  = form.cleaned_data['address'],
				geom     = form.cleaned_data['geom'],
				)
			new_branch.save()
			return redirect('/dashboard/warehouse/')

	template = 'vendor/warehouse_add.html'
	context   = { 'w_link': w_link, 'form':form }
	return render(request,template,context)

@vendor_required
def warehouse_delete(request,warehouse):
	target_warehouse = WareHouse.objects.get(pk=warehouse)
	shop = request.user.shop_set.get()
	w_link = 'active'

	if not target_warehouse.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'w_link': w_link }
		return render(request,template,context)
	else:
		target_warehouse.delete()
		return redirect('/dashboard/warehouse/')

''''''

@vendor_required
def collection(request):
	page = request.GET.get('page', 1)
	collection_list = request.user.shop_set.get().collection_set.all()
	paginator = Paginator(collection_list, 10)
	template = 'vendor/collection.html'
	c_link = 'active'

	try:
		collections = paginator.page(page)
	except PageNotAnInteger:
		collections = paginator.page(1)
	except EmptyPage:
		collections = paginator.page(paginator.num_pages)

	context   = { 'c_link': c_link, 'collections':collections }
	return render(request,template,context)


@vendor_required
def collection_edit(request,collection):
	target_collection = Collection.objects.get(pk=collection)
	shop = request.user.shop_set.get()
	products = shop.product_set.all()
	listed_product = target_collection.products.all()
	c_link = 'active'
	data = { 'name': target_collection.name, 'keywords':target_collection.keywords}
	form = CollectionForm(data, shop=shop)

	if not target_collection.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'c_link': c_link }
		return render(request,template,context)

	if request.method == 'POST':
		form = CollectionForm(request.POST, shop = shop, collection = target_collection )
		if form.is_valid():
			target_collection.name     = form.cleaned_data['name']
			target_collection.keywords = form.cleaned_data['keywords']
			target_collection.save()
			target_collection.products.clear()
			if form.data['products']:
				products_data = json.loads(form.data['products'])
				for o in products_data:
					if o:
						target_product = shop.product_set.get(pk=o)
						target_collection.products.add(target_product)
			return redirect('/dashboard/collection/')
	template = 'vendor/collection_edit.html'
	context   = { 'c_link': c_link, 'form':form,'products':products, "listed_product":listed_product }
	return render(request,template,context)


@vendor_required
def collection_add(request):
	shop = request.user.shop_set.get()
	products = shop.product_set.all()
	c_link = 'active'
	form = CollectionForm( shop=shop )
	if request.method == 'POST':
		form = CollectionForm(request.POST, shop = shop)
		if form.is_valid():
			if not form.cleaned_data['keywords']:
				keywords = form.cleaned_data['name']
			else:
				keywords = form.cleaned_data['keywords']

			new_collection = Collection.objects.create(
				shop       = shop,
				name       = form.cleaned_data['name'],
				keywords   = keywords ,
				language   = "English",
				)
			new_collection.save()
			if form.data['products']:
				products_data = json.loads(form.data['products'])
				for o in products_data:
					if o:
						target_product = shop.product_set.get(pk=o)
						new_collection.products.add(target_product)
			return redirect('/dashboard/collection/')
	template = 'vendor/collection_add.html'
	context   = { 'c_link': c_link, 'form':form, 'products':products }
	return render(request,template,context)

@vendor_required
def collection_delete(request,collection):
	target_collection = Collection.objects.get(pk=collection)
	shop = request.user.shop_set.get()
	c_link = 'active'

	if not target_collection.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'c_link': c_link }
		return render(request,template,context)
	else:
		target_collection.products.clear()
		target_collection.delete()
		return redirect('/dashboard/collection/')

''''''
@vendor_required
def branches(request):
	page = request.GET.get('page', 1)
	branches_list = request.user.shop_set.get().branch_set.all()
	paginator = Paginator(branches_list, 10)
	template = 'vendor/branches.html'
	b_link = 'active'

	try:
		branches = paginator.page(page)
	except PageNotAnInteger:
		branches = paginator.page(1)
	except EmptyPage:
		branches = paginator.page(paginator.num_pages)

	context   = { 'b_link': b_link, 'branches':branches }
	return render(request,template,context)


@vendor_required
def branches_edit(request,branch):
	target_branch = Branch.objects.get(pk=branch)
	shop = request.user.shop_set.get()
	b_link = 'active'
	data = { 'mobile':target_branch.phone.as_national,'country_code':target_branch.phone.country_code ,'name': target_branch.name, 'country':target_branch.country,'province':target_branch.province, 'city':target_branch.city, 'zip_code':target_branch.zip_code,'address':target_branch.address,'geom':target_branch.geom}
	form = BranchForm(data,shop = shop)

	if not target_branch.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'b_link': b_link }
		return render(request,template,context)

	if request.method == 'POST':
		form = BranchForm(request.POST,shop = shop, branch = target_branch )
		if form.is_valid():
			#print form.cleaned_data['country_code'] , form.cleaned_data['mobile']
			phone = '+' + str(form.cleaned_data['country_code']) + str(form.cleaned_data['mobile'])
			target_branch.name     = form.cleaned_data['name']
			target_branch.country  = form.cleaned_data['country']
			target_branch.province = form.cleaned_data['province']
			target_branch.city     = form.cleaned_data['city']
			target_branch.zip_code = form.cleaned_data['zip_code']
			target_branch.address  = form.cleaned_data['address']
			target_branch.geom     = form.cleaned_data['geom']
			target_branch.phone    = phone
			target_branch.save()
			return redirect('/dashboard/branches/')
	template = 'vendor/branches_edit.html'
	context   = { 'b_link': b_link, 'form':form }
	return render(request,template,context)


@vendor_required
def branches_add(request):
	shop = request.user.shop_set.get()
	b_link = 'active'
	form = BranchForm()
	if request.method == 'POST':
		form = BranchForm(request.POST,shop = shop)
		if form.is_valid():
			#print form.cleaned_data['country_code'] , form.cleaned_data['mobile']
			phone = '+' + str(form.cleaned_data['country_code']) + str(form.cleaned_data['mobile'])
			new_branch = Branch.objects.create(
				shop     = shop,
				name     = form.cleaned_data['name'],
				country  = form.cleaned_data['country'],
				province = form.cleaned_data['province'],
				city     = form.cleaned_data['city'],
				zip_code = form.cleaned_data['zip_code'],
				address  = form.cleaned_data['address'],
				geom     = form.cleaned_data['geom'],
				phone    = phone,
				)
			new_branch.save()
			return redirect('/dashboard/branches/')

	template = 'vendor/branches_add.html'
	context   = { 'b_link': b_link, 'form':form }
	return render(request,template,context)

@vendor_required
def branches_delete(request,branch):
	target_branch = Branch.objects.get(pk=branch)
	shop = request.user.shop_set.get()
	b_link = 'active'

	if not target_branch.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'b_link': b_link }
		return render(request,template,context)
	else:
		target_branch.delete()
		return redirect('/dashboard/branches/')




''''''

@vendor_required
def contacts(request):
	page = request.GET.get('page', 1)
	contacts_list = request.user.shop_set.get().contact_set.all()
	paginator = Paginator(contacts_list, 10)
	template = 'vendor/contacts.html'
	co_link = 'active'

	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	context   = { 'co_link': co_link, 'contacts':contacts }
	return render(request,template,context)

@vendor_required
def contacts_edit(request,contact):
	shop = request.user.shop_set.get()
	target_contact = shop.contact_set.get(pk=contact)
	co_link = 'active'
	data = { 'first_name':target_contact.first_name,'last_name': target_contact.last_name,'email':target_contact.email ,'country_code': target_contact.mobile.country_code, 'mobile':target_contact.mobile.as_national}
	form = ContactForm(data)

	if not target_contact.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'co_link': co_link }
		return render(request,template,context)

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			phone = '+' + str(form.cleaned_data['country_code']) + str(form.cleaned_data['mobile'])
			target_contact.first_name = form.cleaned_data['first_name']
			target_contact.last_name  = form.cleaned_data['last_name']
			target_contact.email      = form.cleaned_data['email']
			target_contact.mobile     = phone
			target_contact.save()
			return redirect('/dashboard/contacts/')
	template = 'vendor/contacts_edit.html'
	context   = { 'co_link': co_link, 'form':form }
	return render(request,template,context)


@vendor_required
def contacts_add(request):
	shop = request.user.shop_set.get()
	co_link = 'active'
	form = ContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			phone = '+' + str(form.cleaned_data['country_code']) + str(form.cleaned_data['mobile'])
			new_contact = shop.contact_set.create(
				shop       = shop,
				first_name = form.cleaned_data['first_name'],
				last_name  = form.cleaned_data['last_name'],
				email      = form.cleaned_data['email'],
				mobile      = phone,
				)
			new_contact.save()
			return redirect('/dashboard/contacts/')

	template = 'vendor/contacts_add.html'
	context   = { 'co_link': co_link, 'form':form }
	return render(request,template,context)

@vendor_required
def contacts_delete(request,contact):
	shop = request.user.shop_set.get()
	target_contact = shop.contact_set.get(pk=contact)
	co_link = 'active'

	if not target_contact.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'co_link': co_link }
		return render(request,template,context)
	else:
		target_contact.delete()
		return redirect('/dashboard/contacts/')




''''''

@vendor_required
def setting(request):
	shop = request.user.shop_set.get()
	template = 'vendor/setting.html'
	s_link = 'active'
	context   = { 's_link': s_link, 'shop':shop }
	return render(request,template,context)


@vendor_required
def edit_default_contact(request):
	shop = request.user.shop_set.get()
	template = 'vendor/edit_default_contact.html'
	s_link = 'active'
	data = { 'contact': shop.contact_set.get(default=True).id  }
	form = DefaultContactForm(data,shop=shop)
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	if request.method == 'POST':
		form = DefaultContactForm(request.POST)
		if form.is_valid():
			#print form.cleaned_data['contact']
			old_contact            = shop.contact_set.get(default=True)
			old_contact.default    = False
			old_contact.save()
			target_contact         = shop.contact_set.get(pk=form.cleaned_data['contact'])
			target_contact.default = True
			target_contact.save()
			return redirect('/dashboard/setting/')
		#print form.errors
	return render(request,template,context)

def edit_default_warehouse(request):
	shop = request.user.shop_set.get()
	template = 'vendor/edit_default_warehouse.html'
	s_link = 'active'
	context   = { 's_link': s_link, 'shop':shop }
	data = { 'warehouse': shop.warehouse_set.get(default=True).id  }
	form = DefaultWarehouseForm(data,shop=shop)
	#form = DefaultWarehouseForm(shop=shop)
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	if request.method == 'POST':
		form = DefaultWarehouseForm(request.POST)
		if form.is_valid():
			old_warehouse            = shop.warehouse_set.get(default=True)
			old_warehouse.default    = False
			old_warehouse.save()
			target_warehouse         = shop.warehouse_set.get(pk=form.cleaned_data['warehouse'])
			target_warehouse.default = True
			target_warehouse.save()
			return redirect('/dashboard/setting/')
	return render(request,template,context)


@vendor_required
def edit_default_currency(request):
	shop = request.user.shop_set.get()
	template = 'vendor/edit_default_currency.html'
	s_link = 'active'
	context   = { 's_link': s_link, 'shop':shop }
	data = { 'currency': shop.currency  }
	form = DefaultCurrencyForm(data)
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	if request.method == 'POST':
		form = DefaultCurrencyForm(request.POST)
		if form.is_valid():
			shop.currency = form.cleaned_data['currency']
			shop.save()
			products = shop.product_set.all()
			for o in products:
				o.price_currency = form.cleaned_data['currency']
				o.save()
			return redirect('/dashboard/setting/')
	return render(request,template,context)
@vendor_required
def edit_default_status(request):
	shop = request.user.shop_set.get()
	template = 'vendor/edit_default_status.html'
	s_link = 'active'

	context   = { 's_link': s_link, 'shop':shop }
	return render(request,template,context)












''''''

@vendor_required
def information(request):
	shop = request.user.shop_set.get()
	template = 'vendor/information.html'
	f_link = 'active'

	context   = { 'f_link': f_link, 'shop':shop }
	return render(request,template,context)


@vendor_required
def orders_new_edit(request,order):
	target_invoice = Invoice.objects.get(pk=order)
	shop = request.user.shop_set.get()
	o_n_link = 'active'
	data = { 'stage': target_invoice.stage }
	form = OrdersEditForm(data)

	if not target_invoice.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'o_n_link': o_n_link }
		return render(request,template,context)

	if request.method == 'POST':
		form = OrdersEditForm(request.POST)
		if form.is_valid():
			target_invoice.stage = form.cleaned_data['stage']
			target_invoice.save()
			return redirect('/dashboard/orders/new/')

	template = 'vendor/orders_new_edit.html'
	context   = { 'o_n_link': o_n_link, 'form':form }
	return render(request,template,context)



@vendor_required
def orders_new_view(request,order):
	target_invoice = Invoice.objects.get(pk=order)
	shop = request.user.shop_set.get()
	o_n_link = 'active'

	if not target_invoice.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'o_n_link': o_n_link, 'shop':shop }
		return render(request,template,context)
	orders = target_invoice.order_set.all()

	template = 'vendor/orders_new_view.html'
	context   = { 'o_n_link': o_n_link, 'invoice':target_invoice , 'orders':orders }
	return render(request,template,context)

@vendor_required
def orders_new(request):
	page = request.GET.get('page', 1)

	orders_list = request.user.shop_set.get().invoice_set.filter(finished=False).reverse()
	paginator = Paginator(orders_list, 10)
	template = 'vendor/orders_new.html'
	o_n_link = 'active'

	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	context   = { 'o_n_link': o_n_link, 'orders':orders }

	return render(request,template,context)


@vendor_required
def orders_archivd_view(request,order):
	target_invoice = Invoice.objects.get(pk=order)
	shop = request.user.shop_set.get()
	o_a_link = 'active'

	if not target_invoice.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'o_a_link': o_a_link, 'shop':shop }
		return render(request,template,context)
	orders = target_invoice.order_set.all()

	template = 'vendor/orders_archivd_view.html'
	context   = { 'o_a_link': o_a_link, 'invoice':target_invoice , 'orders':orders }
	return render(request,template,context)

@vendor_required
def orders_archivd(request):
	page = request.GET.get('page', 1)
	orders_list = request.user.shop_set.get().invoice_set.filter(finished=True).reverse()
	paginator = Paginator(orders_list, 10)
	template = 'vendor/orders_archivd.html'
	o_a_link = 'active'

	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	context   = { 'o_a_link': o_a_link, 'orders':orders }

	return render(request,template,context)

@vendor_required
def orders_expected(request):
	page = request.GET.get('page', 1)
	orders_list = request.user.shop_set.get().order_set.filter(finished=False,status=False).reverse()
	paginator = Paginator(orders_list, 10)
	template = 'vendor/orders_expected.html'
	o_e_link = 'active'

	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	context   = { 'o_e_link': o_e_link, 'orders':orders }

	return render(request,template,context)

''''''

@vendor_required
def edit_basic_info(request):
	shop = request.user.shop_set.get()
	data = { 'specialty': shop.specialty, 'keywords':shop.keywords, 'language':shop.language, 'description':shop.description }
	form = EditBasicInfoForm(data)
	template = 'vendor/edit_basic_info.html'
	s_link = 'active'
	if request.method == 'POST':
		form = EditBasicInfoForm(request.POST)
		if form.is_valid():
			shop.specialty = form.cleaned_data['specialty']
			shop.keywords = form.cleaned_data['keywords']
			shop.language = form.cleaned_data['language']
			shop.description = form.cleaned_data['description']
			shop.save()
			return redirect('/dashboard/information/')
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	return render(request,template,context)



@vendor_required
def edit_business_info(request):
	shop = request.user.shop_set.get()
	data = { 'legalform': shop.legalform, 'employees':shop.employees, 'activite':shop.activite, 'areas':shop.areas }
	form = EditBusinessInfoForm(data)
	template = 'vendor/edit_business_info.html'
	s_link = 'active'
	if request.method == 'POST':
		form = EditBusinessInfoForm(request.POST)
		if form.is_valid():
			shop.legalform = form.cleaned_data['legalform']
			shop.employees = form.cleaned_data['employees']
			shop.activite = form.cleaned_data['activite']
			shop.areas = form.cleaned_data['areas']
			shop.save()
			return redirect('/dashboard/information/')
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	return render(request,template,context)

@vendor_required
def edit_location_info(request):
	shop = request.user.shop_set.get()
	data = { 'country': shop.country, 'province':shop.province, 'city':shop.city, 'address':shop.address, 'zip_code':shop.zip_code, 'geom':shop.geom }
	form = EditLocationInfoForm(data)
	template = 'vendor/edit_location_info.html'
	s_link = 'active'
	if request.method == 'POST':
		form = EditLocationInfoForm(request.POST)
		if form.is_valid():
			shop.country  = form.cleaned_data['country']
			shop.province = form.cleaned_data['province']
			shop.city     = form.cleaned_data['city']
			shop.address  = form.cleaned_data['address']
			shop.zip_code = form.cleaned_data['zip_code']
			shop.geom = form.cleaned_data['geom']
			shop.save()
			return redirect('/dashboard/information/')
	context   = { 's_link': s_link, 'shop':shop,'form':form }
	return render(request,template,context)





@csrf_exempt
def add_product_Photo(request):
    unsigned = request.GET.get("unsigned") == "true"
    
    if (unsigned):
        # For the sake of simplicity of the sample site, we generate the preset on the fly. It only needs to be created once, in advance.
        try:
            api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        except api.NotFound:
            api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True, folder="preset_folder")
            
    direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    context = dict(
        # Form demonstrating backend upload
        backend_form = PhotoForm(),
        # Form demonstrating direct upload
        direct_form = direct_form,
        # Should the upload form be unsigned
        unsigned = unsigned,
    )
    # When using direct upload - the following call is necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    if request.method == 'POST':
        # Only backend upload should be posting here
        form = PhotoForm(request.POST, request.FILES)
        shop    = request.user.shop_set.get()
        profile = request.user
        context['posted'] = form.instance
        if form.is_valid():
        	photo = form.save()
        	photo.shop       = shop
        	photo.profile    = profile
        	photo.public_id  = photo.image.public_id
        	photo.secure_url = photo.image.url.replace("http://", "https://")
        	photo.is_product = True
        	photo.save()
        	errorkeys = []
        	initialPreviewConfig = [{ "caption": photo.image.public_id, "width": '120px', "url": "/dashboard/products/upload/delete/" + str(photo.id) + "/","size": 329892 }]
        	src = str( photo.image.build_url() )
        	initialPreview = []
        	initialPreview.append(src)
        	return  JsonResponse( {  'id': str(photo.id),'initialPreviewConfig': initialPreviewConfig,'initialPreview':initialPreview, 'error': '','errorkeys': errorkeys } , status=200,safe=False)
        else:
        	return  JsonResponse( {  'error': form.errors ,'errorkeys': errorkeys } , status=200,safe=False)
    return  HttpResponse( "Something wrong with the server", status=400 )

@csrf_exempt
def delete_product_Photo(request,photo):
	if request.method == 'POST':
		from album.models import Image
		from album.tasks import delete_image_by_public_id

		target_image  = Image.objects.get(pk=photo)
		shop = request.user.shop_set.get()
		if not target_image.shop.id == shop.id:
			return HttpResponse( "Something wrong with the server", status=400 )
		else:
			delete_image_by_public_id.apply_async((  str( target_image.public_id)  ,),countdown=1)
			return  JsonResponse( {  'id': photo } , status=200,safe=False)
	return HttpResponse( "Something wrong with the server", status=400 )







@csrf_exempt
def add_store_logo(request):
    unsigned = request.GET.get("unsigned") == "true"
    
    if (unsigned):
        # For the sake of simplicity of the sample site, we generate the preset on the fly. It only needs to be created once, in advance.
        try:
            api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        except api.NotFound:
            api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True, folder="preset_folder")
            
    direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    context = dict(
        # Form demonstrating backend upload
        backend_form = PhotoForm(),
        # Form demonstrating direct upload
        direct_form = direct_form,
        # Should the upload form be unsigned
        unsigned = unsigned,
    )
    # When using direct upload - the following call is necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    if request.method == 'POST':
        # Only backend upload should be posting here
        form = PhotoForm(request.POST, request.FILES)
        shop    = request.user.shop_set.get()
        profile = request.user
        context['posted'] = form.instance
        if form.is_valid():
        	try:
        		shop.image_set.get(is_logo=True)
        	except Image.DoesNotExist:
        		have_logo = False
        	else:
        		have_logo = True
        	if have_logo:
        		from album.tasks import delete_image_by_public_id
        		old_logo = shop.image_set.get(is_logo=True)
        		delete_image_by_public_id.apply_async((  str( old_logo.public_id)  ,),countdown=1)
        	photo = form.save()
        	photo.shop       = shop
        	photo.profile    = profile
        	photo.public_id  = photo.image.public_id
        	photo.secure_url = photo.image.url.replace("http://", "https://")
        	photo.is_logo    = True
        	photo.save()
        	errorkeys = []
        	initialPreviewConfig = [{ "caption": photo.image.public_id, "width": '120px', "url": "/dashboard/products/upload/delete/" + str(photo.id) + "/","size": 329892 }]
        	src = '<img src="'+ str( photo.image.build_url() ) +'" alt="Your Avatar" style="width: 200px;" ><h6 class="text-muted">Click to select</h6>' 
        	initialPreview = []
        	initialPreview.append(src)
        	return  JsonResponse( {  'id': str(photo.id),'initialPreviewConfig': initialPreviewConfig,'initialPreview':initialPreview, 'error': '','errorkeys': errorkeys } , status=200,safe=False)
        else:
        	return  JsonResponse( {  'error': form.errors ,'errorkeys': errorkeys } , status=200,safe=False)
    return  HttpResponse( "Something wrong with the server", status=400 )



@vendor_required
def shipping(request):
	template = 'vendor/shipping.html'
	Sh_a_link = 'active'
	shop = request.user.shop_set.get()
	couriers = shop.courier_set.all()
	context   = { 'Sh_a_link': Sh_a_link, 'shop':shop,'couriers':couriers }
	return render(request,template,context)


@vendor_required
def shipping_edit(request,account):
	shop = request.user.shop_set.get()
	target_courier = shop.courier_set.get(pk=account)
	Sh_a_link = 'active'
	if not target_courier.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'Sh_a_link': Sh_a_link }
		return render(request,template,context)

	data = json.loads(target_courier.credentials)
	data['courier']   = target_courier.slug
	data['warehouse'] = target_courier.warehouse.id
	form_name = str(target_courier.slug) + "Form(data,shop = shop)"
	form = eval(form_name)
	credentials = {}
	if request.method == 'POST':
		form_name = str(target_courier.slug) + "Form(request.POST,shop=shop)"
		form = eval(form_name)
		if form.is_valid():
			for o in form.cleaned_data:
				if not o  == 'warehouse':
					credentials[o] = form.cleaned_data[o]
			credentials_json    = json.JSONEncoder().encode(credentials)
			description = shop.name + " - [Ftrina.com] - " + target_courier.slug
			import easypost
			from django.conf import settings

			easypost.api_key = getattr(settings, "EASYPOST_API_KEY", None)
			ca = easypost.CarrierAccount.retrieve(target_courier.easypost_id)
			ca.description = description
			ca.credentials=json.loads(credentials_json)
			ca.save()
			return redirect('/dashboard/shipping/')
	template = 'vendor/shipping_courier_edit.html'
	context   = { 'Sh_a_link': Sh_a_link, 'form':form }
	return render(request,template,context)

@vendor_required
def shipping_courier_add(request,courier):
	shop = request.user.shop_set.get()
	Sh_a_link = 'active'
	form_name = str(courier) + "Form(shop=shop)"
	print courier
	try:
		form = eval(form_name)
	except SyntaxError:
		template = 'vendor/404.html'
		context   = { 'Sh_a_link': Sh_a_link }
		return render(request,template,context)
	credentials = {}
	if request.method == 'POST':
		form_name = str(courier) + "Form(request.POST,shop=shop)"
		form = eval(form_name)
		if form.is_valid():
			for o in form.cleaned_data:
				if not o  == 'warehouse':
					credentials[o] = form.cleaned_data[o]
			credentials_json    = json.JSONEncoder().encode(credentials)
			description = shop.name + " - [Ftrina.com] - " + courier
			from django.conf import settings
			import easypost
			easypost.api_key = getattr(settings, "EASYPOST_API_KEY", None)

			try:
				ca = easypost.CarrierAccount.create(
					type=courier,
					description=description,
					credentials=json.loads(credentials_json)
					)
			except Exception:
				form.errors['system'] = ErrorList([u"System Did not accept the information you entered."] )
			else:
				new_courier = shop.courier_set.create(
					name            = COURIER_LIST[ courier ],
					shop            = shop,
					warehouse       = form.cleaned_data['warehouse'],
					slug            = courier,
					credentials     = credentials_json,
					easypost_id     = ca.id
					)
				new_courier.save()
				return redirect('/dashboard/shipping/')
	template = 'vendor/shipping_courier_add.html'
	context   = { 'Sh_a_link': Sh_a_link, 'form':form}
	return render(request,template,context)

@vendor_required
def shipping_add(request):
	Sh_a_link = 'active'
	shop = request.user.shop_set.get()
	template = 'vendor/shipping_add.html'
	context   = { 'Sh_a_link': Sh_a_link}
	return render(request,template,context)
@vendor_required
def shipping_delete(request,account):
	shop = request.user.shop_set.get()
	target_courier = shop.courier_set.get(pk=account)
	Sh_a_link = 'active'
	if not target_courier.shop.id == shop.id:
		template = 'vendor/404.html'
		context   = { 'Sh_a_link': Sh_a_link }
		return render(request,template,context)
	else:
		from django.conf import settings
		import easypost
		easypost.api_key = getattr(settings, "EASYPOST_API_KEY", None)
		ca = easypost.CarrierAccount.retrieve(target_courier.easypost_id)
		ca.delete()
		target_courier.delete()					
		return redirect('/dashboard/shipping/')


@vendor_required
def shipping_labels(request):
	template = 'vendor/shipping_labels.html'
	Sh_l_link = 'active'
	shop = request.user.shop_set.get()
	#print shop.invoice_set.all().count()
	#print shop.invoice_set.all()
	#print shop.invoice_set.filter(finished=False)
	context   = { 'Sh_l_link': Sh_l_link, 'shop':shop }
	return render(request,template,context)

@vendor_required
def shipping_settings(request):
	template = 'vendor/shipping_settings.html'
	Sh_s_link = 'active'
	shop = request.user.shop_set.get()
	#print shop.invoice_set.all().count()
	#print shop.invoice_set.all()
	#print shop.invoice_set.filter(finished=False)
	context   = { 'Sh_s_link': Sh_s_link, 'shop':shop }
	return render(request,template,context)



