# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.context_processors import csrf
from django.template import Context, RequestContext


from django.template.response import TemplateResponse


from django.shortcuts import render
from .forms import SubscribersForm
from .models import Subscribers

# Create your views here.

def SubscribeNewsLetter(request):
	certificate = {}
	certificate.update(csrf(request))
	subscribers_form = SubscribersForm()
	context = {'subscribers_form': subscribers_form }
	if request.method == 'POST':
		subscribers_form = SubscribersForm(request.POST)

		if subscribers_form.is_valid():
			#print "form is valid"	
			email = subscribers_form.data['email']
			subscriber = Subscribers.objects.create( email = email )
			subscriber.save()
			return render( request, 'subscription_done.html', context )

		else:
			context = {'subscribers_form': subscribers_form }
			#print "form Not valid"
			#print subscribers_form.errors
			return TemplateResponse(request, 'newsletter.html' , context)
	else:
		return render(request, 'newsletter.html', context)