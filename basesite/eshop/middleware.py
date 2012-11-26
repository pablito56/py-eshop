#-*- coding: utf-8 -*-
u'''
Created on Nov 19, 2012

@author: pev
'''
# Rest framework imports
from rest_framework import status
from rest_framework.response import Response


class EshopMiddleware(object):
    '''Middleware class to handle internal exceptions
    '''
    def process_exception(self, request, exception):
        import traceback
        print traceback.format_exc()
        return Response({"msg": "Unexpected error ({0}): {1}".format(exception.__class__.__name__,
                                                                     exception)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
