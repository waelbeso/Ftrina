"""remaketory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from order import views
from . import views as main_view
from . import reset as reset_view
from newsletter.views import SubscribeNewsLetter
from blog.views import blog, categorie,BlogDetail
from postmen.views import rates
from vendor import views as vendor_view
from rest_framework import routers
from shop.views import ShopSearchView

router = routers.DefaultRouter()
router.register("shop", ShopSearchView, base_name="shop-search")

urlpatterns = [
    url(r'^$', main_view.home, name='home'),
    url(r'^wael/admin/', admin.site.urls),
    url(r'^s/',  include(router.urls)),
    url(r'^search/', main_view.search.as_view() , name='search'),

    url(r'^dashboard/$', vendor_view.dashboard , name='dashboard'),
    url(r'^dashboard/products/$', vendor_view.products , name='dashboard_products'),
    url(r'^dashboard/products/upload/$', vendor_view.add_product_Photo , name='add_product_Photo'),
    url(r'^dashboard/products/upload/delete/(?P<photo>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', vendor_view.delete_product_Photo , name='delete_product_Photo'),
    
    url(r'^dashboard/products/add/$', vendor_view.products_add , name='dashboard_products_add'),
    url(r'^dashboard/products/edit/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.products_edit , name='dashboard_products_edit'),
    url(r'^dashboard/products/delete/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.products_delete , name='dashboard_products_delete'),
    url(r'^dashboard/products/duplicate/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.products_duplicate , name='dashboard_products_duplicate'),
    url(r'^dashboard/products/variant/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.products_variant , name='dashboard_products_variant'),
    url(r'^dashboard/products/variant/edit/(?P<variant>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.variant_edit , name='dashboard_variant_edit'),

    url(r'^dashboard/warehouse/$', vendor_view.warehouse , name='dashboard_warehouse'),
    url(r'^dashboard/warehouse/add/$', vendor_view.warehouse_add , name='dashboard_warehouse_add'),
    url(r'^dashboard/warehouse/edit/(?P<warehouse>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.warehouse_edit , name='dashboard_warehouse_edit'),
    url(r'^dashboard/warehouse/delete/(?P<warehouse>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.warehouse_delete , name='dashboard_warehouse_delete'),

    url(r'^dashboard/collection/$', vendor_view.collection , name='dashboard_collection'),
    url(r'^dashboard/collection/add/$', vendor_view.collection_add , name='dashboard_collection_add'),
    url(r'^dashboard/collection/edit/(?P<collection>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.collection_edit , name='dashboard_collection_edit'),
    url(r'^dashboard/collection/delete/(?P<collection>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.collection_delete , name='dashboard_collection_delete'),

    url(r'^dashboard/branches/$', vendor_view.branches , name='dashboard_branches'),
    url(r'^dashboard/branches/add/$', vendor_view.branches_add , name='dashboard_branches_add'),
    url(r'^dashboard/branches/edit/(?P<branch>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.branches_edit , name='dashboard_branches_edit'),
    url(r'^dashboard/branches/delete/(?P<branch>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.branches_delete , name='dashboard_branches_delete'),

    url(r'^dashboard/setting/$', vendor_view.setting , name='dashboard_setting'),
    url(r'^dashboard/setting/edit/contact/$',  vendor_view.edit_default_contact , name='dashboard_edit_default_contact'),
    url(r'^dashboard/setting/edit/warehouse/$', vendor_view.edit_default_warehouse , name='dashboard_edit_default_warehouse'),
    url(r'^dashboard/setting/edit/currency/$', vendor_view.edit_default_currency , name='dashboard_edit_default_currency'),
    url(r'^dashboard/setting/edit/status/$', vendor_view.edit_default_status , name='dashboard_edit_default_status'),

    url(r'^dashboard/information/$', vendor_view.information , name='dashboard_information'),
    url(r'^dashboard/information/edit/basic/$',  vendor_view.edit_basic_info , name='dashboard_edit_basic_info'),
    url(r'^dashboard/information/edit/business/$', vendor_view.edit_business_info , name='dashboard_edit_business_info'),
    url(r'^dashboard/information/edit/location/$', vendor_view.edit_location_info , name='dashboard_edit_location_info'),


    url(r'^dashboard/inventory/$', vendor_view.inventory , name='dashboard_inventory'),
    url(r'^dashboard/inventory/edit/(?P<inventory>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',    vendor_view.inventory_edit ,   name='dashboard_inventory_edit'),
    url(r'^dashboard/inventory/add/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',       vendor_view.inventory_add ,    name='dashboard_inventory_add'),
    url(r'^dashboard/inventory/delete/(?P<inventory>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.inventory_delete , name='dashboard_inventory_delete'),


    url(r'^dashboard/orders/new/$', vendor_view.orders_new , name='dashboard_orders_new'),
    url(r'^dashboard/orders/new/edit/(?P<order>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', vendor_view.orders_new_edit , name='dashboard_orders_new_edit'),
    url(r'^dashboard/orders/new/view/(?P<order>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', vendor_view.orders_new_view , name='dashboard_orders_new_view'),

    url(r'^dashboard/orders/archivd/$', vendor_view.orders_archivd , name='dashboard_orders_archivd'),
    url(r'^dashboard/orders/archivd/view/(?P<order>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', vendor_view.orders_archivd_view , name='dashboard_orders_archivd_view'),
    url(r'^dashboard/orders/expected/$', vendor_view.orders_expected , name='dashboard_orders_expected'),

    url(r'^dashboard/shipping/$', vendor_view.shipping , name='dashboard_shipping'),
    url(r'^dashboard/shipping/add/$', vendor_view.shipping_add , name='dashboard_shipping_add'),
    url(r'^dashboard/shipping/add/(?P<courier>[\w-]+)/$',  vendor_view.shipping_courier_add , name='dashboard_shipping_courier_add'),
    
    url(r'^dashboard/shipping/edit/(?P<account>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.shipping_edit , name='dashboard_shipping_edit'),
    url(r'^dashboard/shipping/delete/(?P<account>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.shipping_delete , name='dashboard_shipping_delete'),

    url(r'^dashboard/shipping/labels/$', vendor_view.shipping_labels , name='dashboard_shipping_labels'),
    url(r'^dashboard/shipping/settings/$', vendor_view.shipping_settings , name='dashboard_shipping_settings'),


    url(r'^dashboard/customers/$', vendor_view.customers , name='dashboard_customers'),

    url(r'^dashboard/visuals/$', vendor_view.visuals , name='dashboard_visuals'),
    url(r'^dashboard/visuals/upload/$', vendor_view.add_store_logo , name='dashboard_add_store_logo'),

    

    url(r'^dashboard/contacts/$', vendor_view.contacts , name='dashboard_contacts'),
    url(r'^dashboard/contacts/add/$', vendor_view.contacts_add , name='dashboard_contacts_add'),
    url(r'^dashboard/contacts/edit/(?P<contact>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.contacts_edit , name='dashboard_contacts_edit'),
    url(r'^dashboard/contacts/delete/(?P<contact>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',  vendor_view.contacts_delete , name='dashboard_contacts_delete'),


    url(r'^about$', main_view.about, name='about'),
    url(r'^privacy$', main_view.privacy, name='privacy'),
    url(r'^terms$', main_view.terms, name='terms'),
    url(r'^cookie$', main_view.cookie, name='cookie'),
    url(r'^faq$', main_view.faq, name='faq'),
    url(r'^blog$', blog, name='blog'),
    url(r'^blog/(?P<categorie>[\w-]+)$', categorie, name='blog_categorie'),
    url(r'^blog/(?P<categorie>[\w-]+)/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', BlogDetail, name='blog_detail'),
    url(r'^directory$', main_view.directory, name='directory'),
    url(r'^refund$', main_view.refund, name='refund'),
    url(r'^prohibited$', main_view.prohibited, name='prohibited'),
    url(r'^subscribenewsletter$', SubscribeNewsLetter, name='subscribe_news_letter'),


    url(r'^login/$', main_view.loginView, name='login'),
    url(r'^logout/$', main_view.logoutView, name='logout'),
    url(r'^register/$', main_view.registerView, name='register'),
    url(r'^register/confirm/(?P<code>[\w-]+)/$', main_view.register_confirms_view, name='register_confirm'),
    url(r'^cart/$', main_view.cart, name='cart'),
    url(r'^checkout/$', main_view.checkout, name='checkout'),
    url(r'^checkout/delivery/(?P<checkout>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', main_view.checkout_shipping, name='checkout_shipping'),
    url(r'^cart/pay/(?P<checkout>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', main_view.pay, name='pay'),
    url(r'^finish/$', main_view.finish, name='finish'),
    url(r'^profile/$', main_view.profile, name='profile'),
    url(r'^profile/edit/$', main_view.edit_profile, name='edit_profile'),
    url(r'^address/$', main_view.address, name='address'),
    url(r'^address/add/$', main_view.add_address, name='add_address'),
    url(r'^address/edit/(?P<id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', main_view.edit_address, name='edit_address'),
    url(r'^history/$', main_view.history, name='history'),
    url(r'^password/$', main_view.change_password, name='change_password'),
    url(r'^add/to/cart/(?P<product>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', main_view.add_to_cart, name='add_to_cart'),
    url(r'^remove/from/cart/(?P<order>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', main_view.remove_from_cart, name='remove_from_cart'),
    url(r'^resetpassword/$', reset_view.password_reset , {'template_name': 'registration/password_reset_form.html'}, name='password_reset' ),
    url(r'^resetpassword/passwordsent/$', reset_view.password_reset_done, {'template_name': 'registration/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', reset_view.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'},name='password_reset_confirm'),
    url(r'^reset/done/$', reset_view.password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},name='password_reset_complete'),

    url(r'^(?P<shop>[\w-]+)/shipping/$', rates, name='shop_shipping'),
    url(r'^(?P<shop>[\w-]+)/location/$', main_view.location, name='shop_location'),
    url(r'^(?P<shop>[\w-]+)/(?P<product>[\w-]+)$',  main_view.product ),
    url(r'^(?P<shop>[\w-]+)$', main_view.shop ),
    url(r'^(?P<shop>[\w-]+)/(?P<collection>[\w-]+)/$', main_view.collection ),


]
