#-*- coding: utf-8 -*-
u'''
Created on Nov 19, 2012

@author: pev
<<<<<<< HEAD
@author: jacobcr
'''
# Django imports
from django.http import HttpResponse
# Rest framework imports
from rest_framework import status
from rest_framework.renderers import JSONRenderer
# Pymongo imports
from pymongo.errors import DuplicateKeyError


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    renderer = JSONRenderer()

    def __init__(self, data, **kwargs):
        content = self.renderer.render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class EshopMiddleware(object):
    '''Middleware class to handle internal exceptions
    '''
    def process_exception(self, request, exception):
        # Check for MongoDB unique indexes exception 
        if isinstance(exception, DuplicateKeyError):
            msg = "Trying to create a resource which already exists"
            return JSONResponse({"msg": msg}, status=status.HTTP_409_CONFLICT)
        # Check if failed accesing a key of a dict
        elif isinstance(exception, KeyError):
            msg = "Trying to retrieve a wrong document key '{0'}".format(KeyError)
            return JSONResponse({"msg": msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Otherwise
        import traceback
        print "Unexpected e-shop exception caught.", traceback.format_exc()
        msg = "Unexpected error ({0}): {1}".format(exception.__class__.__name__, exception)
        return JSONResponse({"msg": msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
