#-*- coding: utf-8 -*-
u'''
Created on Nov 18, 2012

@author: pev
@author: jacobcr
'''
# Django imports
from django.conf import settings
from django.http import Http404
# Django ReST fwk imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.reverse import reverse


class RootController(APIView):
    '''Controller for root URI
    '''

    def get(self, request, format=None):
        '''Get the name and version of the API
        '''
        data = {"name": settings.API_NAME, "version": settings.API_VERSION,
                'items': reverse('itemlist', request=request, format=format)}
        return Response(data)


itemlist = [{"id": "1",
             "name": "Super item",
             "description": "This is the most amazing super item",
             "category": "Strange items",
             "price": 17.99,
             "stock": 3,
             "purchases": 27,
             "updated": "2012-11-16T19:10:34"
             }]


class ItemListController(APIView):
    def get(self, request):
        return Response(itemlist)

    def post(self, request):
        if not 'name' in request.DATA:
            raise ParseError()
        item = request.DATA
        item['id'] = str(len(itemlist) + 1)
        itemlist.append(item)
        headers = {'Location': reverse('itemdetail', request=request, args=[item['id']])}
        return Response(item, status.HTTP_201_CREATED, headers=headers)


class ItemController(APIView):
    def get(self, request, item_id):
        result = filter(lambda x: x['id'] == item_id, itemlist)
        if not result:
            raise Http404()
        return Response(result[0])

    def put(self, request, item_id):
        result = filter(lambda x: x['id'] == item_id, itemlist)
        if not result:
            raise Http404()
        result[0].update(request.DATA)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, item_id):
        result = filter(lambda x: x['id'] == item_id, itemlist)
        if not result:
            raise Http404()
        itemlist.remove(result[0])
        return Response(status=status.HTTP_204_NO_CONTENT)
