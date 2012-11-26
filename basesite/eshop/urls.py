#-*- coding: utf-8 -*-
u'''
Created on Nov 18, 2012

@author: pev
@author: jacobcr
'''
from django.conf.urls.defaults import patterns, url
from eshop import views

urlpatterns = patterns('',
                       url(r'^/?$', views.RootController.as_view(), name='api-root'),
                       url(r'^items/?$', views.ItemListController.as_view(), name='itemlist'),
                       url(r'^items/(?P<item_id>[^\/]+)/?$', views.ItemController.as_view(), name='itemdetail'),
                       url(r'^users/?$', views.UserListController.as_view(), name='userlist'),
                       url(r'^users/(?P<user_id>[^\/]+)/?$', views.UserController.as_view(), name='userdetail'),
                       url(r'^users/(?P<user_id>[^\/]+)/cart/?$', views.CartListController.as_view(), name='cartlist'),
                       url(r'^users/(?P<user_id>[^\/]+)/cart/(?P<cart_id>[^\/]+)/?$', views.CartController.as_view(), name='cartdetail'),
                       )
