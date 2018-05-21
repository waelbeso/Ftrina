# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from ftrina.forms import LoginForm , RegisterForm
from newsletter.forms import SubscribersForm
from .models import Category, Article


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import DateTimeField
from django.db.models.functions import Trunc



def blog(request):
	#request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
	page = request.GET.get('page', 1)

	template  = 'blog.html'
	loginForm = LoginForm()
	subscribersForm = SubscribersForm()
	categories = Category.objects.all()
	articles_list   = Article.objects.filter(recommended='True', published='True' )
	paginator = Paginator(articles_list, 4)

	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
		
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'categories': categories, 'articles':articles }

	return render(request,template,context)


def categorie(request,categorie):
	page = request.GET.get('page', 1)

	category = Category.objects.get(name=categorie)
	template  = 'blog_categorie.html'
	loginForm = LoginForm()
	subscribersForm = SubscribersForm()
	categories = Category.objects.all()
	articles_list   = category.article_set.filter(published='True').order_by('date').reverse()
	paginator = Paginator(articles_list, 10)

	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'categories': categories , 'categorie':categorie, 'articles':articles }

	return render(request,template,context)

def BlogDetail(request,categorie,pk):
	#request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
	
	template  = 'blog-detail.html'
	loginForm = LoginForm()
	subscribersForm = SubscribersForm()
	categories = Category.objects.all()
	article   = Article.objects.get(pk=pk)

	context = { 'loginForm': loginForm, 'subscribersForm': subscribersForm, 'categories': categories, 'article':article }

	return render(request,template,context)
