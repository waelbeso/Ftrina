# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from ftrina.forms import LoginForm
from ftrina.forms import SearchForm
from newsletter.forms import SubscribersForm
from shop.models import Shop

import requests







def rates(request,shop):
	store = Shop.objects.get(slug = shop)
	loginForm=LoginForm()
	subscribersForm = SubscribersForm()
	searchForm = SearchForm()



	print store.name
	print store.ship_from
	url = 'https://sandbox-api.postmen.com/v3/rates'

	headers = {
	'postmen-api-key': '592c0074-5ade-4f28-a9ad-772465bd590f',
	'content-type': 'application/json'
	}

	
	payload = '''
{
  "async": false,
  "shipper_accounts": [
    {
      "id": "3fad06c4-b325-45e9-b635-a1dc7fafd102"
    }
  ],
  "is_document": false,
  "shipment": {
    "ship_from": {
      "contact_name": "[Bring] Contact name",
      "company_name": "[Bring] Testing Company",
      "street1": "330-340 W 34th St",
      "country": "NOR",
      "type": "business",
      "postal_code": "7600",
      "city": "Oslo",
      "phone": "+47 32 654 310",
      "street2": null,
      "tax_id": null,
      "street3": null,
      "state": "TX",
      "email": "test@test.com",
      "fax": null
    },
    "ship_to": {
      "contact_name": "Dr. Moises Corwin",
      "phone": "1-140-225-6410",
      "email": "Giovanna42@yahoo.com",
      "street1": "28292 Daugherty Orchard",
      "city": "Beverly Hills",
      "postal_code": "90209",
      "state": "CA",
      "country": "USA",
      "type": "residential"
    },
    "parcels": [
      {
        "description": "Food XS",
        "box_type": "custom",
        "weight": {
          "value": 2,
          "unit": "kg"
        },
        "dimension": {
          "width": 20,
          "height": 40,
          "depth": 40,
          "unit": "cm"
        },
        "items": [
          {
            "description": "Food Bar",
            "origin_country": "USA",
            "quantity": 2,
            "price": {
              "amount": 3,
              "currency": "USD"
            },
            "weight": {
              "value": 0.6,
              "unit": "kg"
            },
            "sku": "imac2014"
          }
        ]
      }
    ]
  }
}
	'''

	#response = requests.request('POST', url, data=payload, headers=headers)
	#print(response.text)

	model = store.model_set.all()
	template = 'shipping.html'
	context   = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'shop': store,'searchForm':searchForm,'model':model }
	return render(request,template,context)


	