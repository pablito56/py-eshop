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
from rest_framework import status
from rest_framework.reverse import reverse
# Custom eshop imports
from serializers import ItemSerializer, ItemUpdateSerializer, UserSerializer, UserUpdateSerializer, CartItemSerializer
from services import ItemsService, UsersService, PurchasesService


class RootController(APIView):
    '''Controller for root URI
    '''

    def get(self, request, format=None):
        '''Get the name and version of the API
        '''
        data = {"name": settings.API_NAME, "version": settings.API_VERSION,
                'items': reverse('itemlist', request=request, format=format),
                'users': reverse('userlist', request=request, format=format)}
        return Response(data)


items_service = ItemsService()
users_service = UsersService()
purchases_service = PurchasesService()


class ItemListController(APIView):
    def get(self, request):
        return Response(items_service.get_all())

    def post(self, request):
        item_ser = ItemSerializer(data=request.DATA)
        if not item_ser.is_valid():
            errs_lst = [": ".join((wrong, " ".join(item_ser.errors[wrong]))) for wrong in item_ser.errors]
            msg = ", ".join(errs_lst)
            return Response({"msg": "Wrong input. " + msg}, status.HTTP_406_NOT_ACCEPTABLE)
        item = items_service.create(item_ser.object)
        if item is None:
            return Response({"msg": "Item 'name' already exists"}, status.HTTP_409_CONFLICT)
        headers = {'Location': reverse('itemdetail', request=request, args=[item['id']])}
        return Response(item, status.HTTP_201_CREATED, headers=headers)


class ItemController(APIView):
    def get(self, request, item_id):
        return Response(items_service.get_one(item_id))

    def put(self, request, item_id):
        item_ser = ItemUpdateSerializer(data=request.DATA)
        if not item_ser.is_valid():
            errs_lst = [": ".join((wrong, " ".join(item_ser.errors[wrong]))) for wrong in item_ser.errors]
            msg = ", ".join(errs_lst)
            return Response({"msg": "Wrong input. " + msg}, status.HTTP_406_NOT_ACCEPTABLE)
        items_service.update(item_id, item_ser.object)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, item_id):
        items_service.delete(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListController(APIView):
    def get(self, request):
        return Response(users_service.get_all())

    def post(self, request):
        user_ser = UserSerializer(data=request.DATA)
        if not user_ser.is_valid():
            errs_lst = [": ".join((wrong, " ".join(user_ser.errors[wrong]))) for wrong in user_ser.errors]
            msg = ", ".join(errs_lst)
            return Response({"msg": "Wrong input. " + msg}, status.HTTP_406_NOT_ACCEPTABLE)

        user = users_service.create(user_ser.object)
        if user is None:
            return Response({"msg": "User 'name' already exists"}, status.HTTP_409_CONFLICT)

        headers = {'Location': reverse('userdetail', request=request, args=[user['id']])}
        return Response(user, status.HTTP_201_CREATED, headers=headers)


class UserController(APIView):
    def get(self, request, user_id):
        return Response(users_service.get_one(user_id))

    def put(self, request, user_id):
        user_ser = UserUpdateSerializer(data=request.DATA)
        if not user_ser.is_valid():
            errs_lst = [": ".join((wrong, " ".join(user_ser.errors[wrong]))) for wrong in user_ser.errors]
            msg = ", ".join(errs_lst)
            return Response({"msg": "Wrong input. " + msg}, status.HTTP_406_NOT_ACCEPTABLE)
        if user_ser.object:
            users_service.update(user_id, user_ser.object)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, user_id):
        users_service.delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartListController(APIView):
    def get(self, request, user_id):
        return Response(users_service.get_cart(user_id))

    def post(self, request, user_id):
        item_ser = CartItemSerializer(data=request.DATA)
        if not item_ser.is_valid():
            errs_lst = [": ".join((wrong, " ".join(item_ser.errors[wrong]))) for wrong in item_ser.errors]
            msg = ", ".join(errs_lst)
            return Response({"msg": "Wrong input. " + msg}, status.HTTP_406_NOT_ACCEPTABLE)

        item = items_service.get_one(item_ser.object['id'])
        cartitem = users_service.add_to_cart(user_id, item, item_ser.object['quantity'])
        headers = {'Location': reverse('cartdetail', request=request, args=[user_id, item['id']])}
        return Response(cartitem, status.HTTP_201_CREATED, headers=headers)


class CartController(APIView):
    def get(self, request, user_id, cart_id):
        return Response(users_service.get_one_cart(user_id, cart_id))

    def delete(self, request, user_id, cart_id):
        users_service.delete_cart(user_id, cart_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchasesListController(APIView):
    def get(self, request, user_id):
        return Response(purchases_service.get_all(user_id))

    def post(self, request, user_id):
        return Response(purchases_service.buy(user_id))
