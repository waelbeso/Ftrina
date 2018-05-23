# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

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
			from django.conf import settings
			url = 'https://sandbox-api.postmen.com/v3/shipper-accounts/' + str(target_courier.postmen_id) + '/credentials'
			postmen_api_key = getattr(settings, "POSTMEN_API_KEY", None)
			headers = {
			'postmen-api-key': postmen_api_key ,
			'content-type': 'application/json'
			}
			payload = json.loads(credentials_json)
			postmen_response = requests.request('PUT', url, data=json.JSONEncoder().encode(payload), headers=headers)
			print(postmen_response.text)
			json_response = json.loads(postmen_response.text)
			if json_response['meta']['code'] == 200:
				target_courier.credentials = credentials_json
				target_courier.save()
			else:
				form.errors['system'] = ErrorList([u"System Did not accept the information you entered."] )

			url = 'https://sandbox-api.postmen.com/v3/shipper-accounts/' + str(target_courier.postmen_id) + '/info'
			payload ={
			"description": description ,
			"timezone": "Asia/Hong_Kong",
			}
			payload["address"] = form.cleaned_data['warehouse'].ship_from
			postmen_response = requests.request('PUT', url, data=json.JSONEncoder().encode(payload), headers=headers)
			print(postmen_response.text)
			if json_response['meta']['code'] == 200:
				target_courier.warehouse = form.cleaned_data['warehouse']
				target_courier.save()
				return redirect('/dashboard/shipping/')
			else:
				form.errors['system'] = ErrorList([u"System Did not accept the information you entered."] )
	template = 'vendor/shipping_courier_edit.html'
	context   = { 'Sh_a_link': Sh_a_link, 'form':form }
	return render(request,template,context)

@vendor_required
def shipping_courier_add(request,courier):
	shop = request.user.shop_set.get()
	Sh_a_link = 'active'
	form_name = str(courier) + "Form(shop=shop)"
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

			
			url = 'https://sandbox-api.postmen.com/v3/shipper-accounts'
			postmen_api_key = getattr(settings, "POSTMEN_API_KEY", None)
			headers = {
			'postmen-api-key': postmen_api_key ,
			'content-type': 'application/json'
			}
			payload ={
			"slug":courier,
			"description": description ,
			"timezone": "Asia/Hong_Kong",
			}
			payload["credentials"] = json.loads(credentials_json)
			payload["address"] = form.cleaned_data['warehouse'].ship_from
			postmen_response = requests.request('POST', url, data=json.JSONEncoder().encode(payload), headers=headers)
			print(postmen_response.text)
			json_response = json.loads(postmen_response.text)
			if json_response['meta']['code'] == 200:
				new_courier = shop.courier_set.create(
					name            = COURIER_LIST[ courier ],
					shop            = shop,
					warehouse       = form.cleaned_data['warehouse'],
					slug            = courier,
					credentials     = credentials_json,
					postmen_id      = json_response['data']['id']
					)
				new_courier.save()
				return redirect('/dashboard/shipping/')
			else:
				form.errors['system'] = ErrorList([u"System Did not accept the information you entered."] )
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
		url = 'https://sandbox-api.postmen.com/v3/shipper-accounts/' + str(target_courier.postmen_id)
		postmen_api_key = getattr(settings, "POSTMEN_API_KEY", None)
		headers = {
		'postmen-api-key': postmen_api_key ,
		'content-type': 'application/json'
		}
		postmen_response = requests.request('DELETE', url, headers=headers)
		json_response = json.loads(postmen_response.text)
		if json_response['meta']['code'] == 200:
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

'''
	@property
	def parcels(self):
		data = []
		if self.weight < 600:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 0.5,
					"unit": "kg"
					},
				"dimension": {
				"width": 35,
				"height": 27.5,
				"depth": 1,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 1000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 1 ,
					"unit": "kg"
					},
				"dimension": {
				"width": 18.2,
				"height": 33.7,
				"depth": 10,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 2000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 2,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 10,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data

		if self.weight < 5000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 5,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 18,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data
		if self.weight < 10000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 10,
					"unit": "kg"
					},
				"dimension": {
				"width": 32.2,
				"height": 33.7,
				"depth": 34.5,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data
		if self.weight < 20000:
			data.append({
				"description": "Food XS",
				"box_type": "custom",
				"weight": {
					"value": 20,
					"unit": "kg"
					},
				"dimension": {
				"width": 40.4,
				"height": 48.1,
				"depth": 38.9,
				"unit": "cm"
				},
				"items": self.items
				},)
			return data





	#from zeep import Client
	#WebAuthenticationDetail = [ {'UserCredential':[{ "Key":"tnIkKEydGiS0IKls","Password":"759Q1CJUN1tUh5qm2yOrRUbjb"}],'ParentCredential':[{ "Key":"tnIkKEydGiS0IKls","Password":"759Q1CJUN1tUh5qm2yOrRUbjb"}] }]
	#WebAuthenticationDetail.append(  } )
	#ClientDetail=[]
	#TransactionDetail=[{'CustomerTransactionId':' *** Ftrina.com Request ***'}]
	#Version=[{'ServiceId':'crs','Major':'22','Intermediate':'0','Minor':'0'}]
	#ClientDetail.append( {'AccountNumber':'510087720','MeterNumber':'119039998'} )
	#ReturnTransitAndCommit = True
	
	#client = Client('/Users/waelel-begearmi/Downloads/RateService/RateService_v22.wsdl')
	#node = client.create_message(client.service, 'getRates', WebAuthenticationDetail=WebAuthenticationDetail, ClientDetail=ClientDetail,TransactionDetail=TransactionDetail,Version=Version,ReturnTransitAndCommit=ReturnTransitAndCommit  )
	#print 
	#client = Client('/Users/waelel-begearmi/Downloads/aramex-rates-calculator-wsdl.wsdl')
	
	#response = client.service
	#print response.getRates()
	#print dir(response)


	context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'data':user_checkout, 'form': form }
	return render(request,template,context)

	url = 'https://sandbox-api.postmen.com/v3/rates'
	postmen_api_key = getattr(settings, "POSTMEN_API_KEY", None)
	headers = {
	'postmen-api-key': postmen_api_key,
	'content-type': 'application/json'
	}
	payload = {
	"async": False,
	"shipper_accounts": shipper_accounts,
	"is_document": False,
	}

	data = payload
	data['shipment'] = {
	"ship_from" : first_warehouse.ship_from,
	"ship_to" : user_checkout.ship_to,
	"parcels":request.basket.parcels,
	}
	#print payload
	#print data
	response = requests.request('POST', url, data=json.JSONEncoder().encode(data), headers=headers)

	reply = response.json()
	print "--------------reply--------------------\n"
	print reply
	print "\n--------------reply--------------------"

	if not  reply['data']['rates'] is None:
		print reply['data']['rates'][0]['info_message']
		if not  reply['data']['rates'][0]['info_message'] == 'No rate quotes returned from carrier.':
			rates = reply['data']['rates']
			for o in rates:
				choices = []
				#print reply['data']['rates']

				name  = str(o['service_name']) + ' ' +  str(o['total_charge']['amount']) + ' ' + str(o['total_charge']['currency'])
				value = str(o['shipper_account']['id'])  + '@' + str(o['service_type'])  + '@' +   str(o['total_charge']['amount']) + '@' + str(o['total_charge']['currency'])  + '@' + str(o['service_name'])  
				choices.append( ( value  , name  ) )

				form.fields["shipping"].choices = choices
				#print form.fields["shipping"].choices
				context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'data':user_checkout, 'rates':rates, 'form': form }
				return render(request,template,context)
		else:
			error = 'No rate quotes returned from carrier.'
			context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'data':user_checkout, 'form': form,'error':error }
			return render(request,template,context)
	else:
		context      = { 'loginForm': loginForm, 'subscribersForm': subscribersForm,'searchForm':searchForm, 'data':user_checkout, 'form': form }
		return render(request,template,context)
'''



