#-*- coding: utf-8 -*-
u'''
Created on Nov 20, 2012

@author: pev
@author: jacobcr
'''
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
                       (r'^{0}/'.format(settings.API_NAME), include('eshop.urls')),
                       )
