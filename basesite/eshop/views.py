#-*- coding: utf-8 -*-
u'''
Created on Nov 18, 2012

@author: pev
@author: jacobcr
'''
# Django imports
from django.conf import settings
# Django ReST fwk imports
from rest_framework.views import APIView
from rest_framework.response import Response

class RootController(APIView):
    '''Controller for root URI
    '''

    def get(self, request):
        '''Get the name and version of the API
        '''
        data = {"name": settings.API_NAME, "version": settings.API_VERSION}
        return Response(data)
