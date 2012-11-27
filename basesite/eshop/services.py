#-*- coding: utf-8 -*-
u'''
Created on Nov 21, 2012

@author: pev
@author: jacobcr
'''
# Standard library imports
from datetime import datetime
# Django imports
from django.http import Http404
# Custom eshop imports
from daos import ItemsDao, UsersDao, PurchaseDao


class ItemsService(object):
    '''Business logic to handle Items
    '''
    dao = ItemsDao()

    def create(self, new):
        '''Create a new Item
        '''
        new["updated"] = datetime.now()
        return self.dao.insert(new)

    def get_all(self):
        '''Retrieve all Items
        '''
        return list(self.dao.find_all())

    def get_one(self, resource_id):
        '''Retrieve single Item
        '''
        try:
            resource = self.dao.find(int(resource_id))
        except ValueError:
            raise Http404()
        if resource:
            return resource
        raise Http404()

    def update(self, resource_id, new):
        '''Update one Item
        '''
        new["updated"] = datetime.now()
        try:
            if not self.dao.update(int(resource_id), new):
                raise Http404()
            return True
        except ValueError:
            raise Http404()
        return True

    def delete(self, resource_id):
        '''Delete one Item
        '''
        try:
            if not self.dao.remove(int(resource_id)):
                raise Http404()
            return True
        except ValueError:
            raise Http404()

class UsersService(ItemsService):
    dao = UsersDao()

    def add_to_cart(self, user_id, item, quantity):
        doc = self.dao.add_to_cart(int(user_id), item['id'], item['name'], item['price'], quantity)
        if not doc:
            raise Http404('User not exists)')
        return doc

    def get_cart(self, user_id):
        return self.get_one(user_id).get('cart', [])

    def get_one_cart(self, user_id, cart_id):
        doc = self.dao.get_cart_item(user_id, cart_id)
        if not doc:
            raise Http404('Item not found in cart')
        return doc['cart'][0]

    def delete_cart(self, user_id, cart_id):
        if not self.dao.delete_cart_item(user_id, cart_id):
            raise Http404()

class PurchasesService(ItemsService):
    pdao = PurchaseDao()
    udao = UsersDao()

    def get_all(self, user_id):
        return list(self.pdao.get_by_user(int(user_id))) or []

    def buy(self, user_id):
        user_id = int(user_id)
        cart = self.udao.find(user_id).get('cart', [])
        if not cart:
            raise Http404('No cart for user')

        total = sum([x['price'] * x['quantity'] for x in cart])
        items = [x['id'] for x in cart]
        created = datetime.now()
        purchase = dict(total=total, items=items, created=created, user_id=user_id)
        self.udao.delete_cart(user_id)
        return self.pdao.insert(purchase)
