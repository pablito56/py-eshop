#-*- coding: utf-8 -*-
u'''
Created on Nov 20, 2012

@author: pev
@author: jacobcr
'''
import json
from django.test import TestCase as DjangoTestCase
from django.conf import settings
from rest_framework import status


class TestCase(DjangoTestCase):
    def get(self, *args, **kwargs):
        return self.client.get(*args, content_type='application/json', **kwargs)

    def put(self, *args, **kwargs):
        return self.client.put(*args, content_type='application/json', **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(*args, content_type='application/json', **kwargs)

    def delete(self, *args, **kwargs):
        return self.client.delete(*args, content_type='application/json', **kwargs)


root = "/%s/" % settings.API_NAME


class RootControllerTest(TestCase):
    def test_get(self):
        '''Test GET root
        '''
        response = self.get(root)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ItemListControllerTest(TestCase):
    itemspath = root + 'items/'

    def test_get_list(self):
        '''Test GET Items list
        '''
        response = self.get(self.itemspath)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        '''Test POST Item
        '''
        item = {"name": "Super item", "description": "This is the most amazing super item",
                "category": "Strange items", "price": 17.99, "stock": 3
                }
        response = self.post(self.itemspath, data=json.dumps(item))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_post_invalid(self):
        '''Test POST Item error
        '''
        item = {}
        response = self.post(self.itemspath, item)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        '''Test DELETE Items list error
        '''
        response = self.delete(self.itemspath)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ItemControllerTest(ItemListControllerTest):
    def test_get(self):
        '''Test GET single Item
        '''
        response = self.get(self.itemspath + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_found(self):
        '''Test GET single Item not found error
        '''
        response = self.get(self.itemspath + '2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put(self):
        '''Test PUT single Item
        '''
        response = self.put(self.itemspath + '1/', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

    def test_put_not_found(self):
        '''Test PUT single Item not found error
        '''
        response = self.put(self.itemspath + '1111/', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_delete(self):
        '''Test DELETE single Item
        '''
        response = self.delete(self.itemspath + '1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        '''Test DELETE single Item not found
        '''
        response = self.delete(self.itemspath + '2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post(self):
        '''Test POST single Item error
        '''
        response = self.post(self.itemspath + '1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
