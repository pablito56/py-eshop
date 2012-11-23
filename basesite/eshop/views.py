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
# Custom eshop imports
from services import ItemsService
from serializers import ItemSerializer


class RootController(APIView):
    '''Controller for root URI
    '''

    def get(self, request, format=None):
        '''Get the name and version of the API
        '''
        data = {"name": settings.API_NAME, "version": settings.API_VERSION,
                'items': reverse('itemlist', request=request, format=format)}
        return Response(data)


items_service = ItemsService()


class ItemListController(APIView):
    def get(self, request):
        return Response(items_service.get_all())

    def post(self, request):
        ser_item = ItemSerializer(data=request.DATA)
        if not ser_item.is_valid():
            return Response({"msg": "Invalid incoming Item Json"}, status.HTTP_406_NOT_ACCEPTABLE)
        item = items_service.create(request.DATA)
        headers = {'Location': reverse('itemdetail', request=request, args=[item['id']])}
        return Response(item, status.HTTP_201_CREATED, headers=headers)


class ItemController(APIView):
    def get(self, request, item_id):
        return Response(items_service.get_one(item_id))

    def put(self, request, item_id):
        items_service.update(item_id, request.DATA)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, item_id):
        items_service.delete(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
