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
from pymongo import Connection, ReadPreference
from datetime import datetime


conn = None
dbconn = None


class TestCase(DjangoTestCase):
    @classmethod
    def setUpClass(cls):
        # Output whole diff when asserts fail
        cls.maxDiff = None
        # Output diff always when asserts fail
        cls.longMessage = True

    def setUp(self):
        global dbconn
        dbconn.drop_collection(settings.ITEMS_COLL)

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
        '''ItemListControllerTest test GET Items list
        '''
        response = self.get(self.itemspath)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        '''ItemListControllerTest test POST Item
        '''
        item = {"name": "Super item", "description": "This is the most amazing super item",
                "category": "Strange items", "price": 17.99, "stock": 3
                }
        response = self.post(self.itemspath, data=json.dumps(item))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_post_invalid(self):
        '''ItemListControllerTest test POST Item error
        '''
        item = {}
        response = self.post(self.itemspath, item)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        '''ItemListControllerTest test DELETE Items list error
        '''
        response = self.delete(self.itemspath)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ItemControllerTest(ItemListControllerTest):

    def test_get(self):
        '''ItemControllerTest test GET single Item
        '''
        global dbconn
        item = {"id": 1,
                "name": "Super item",
                "description": "This is the most amazing super item",
                "category": "Strange items",
                "price": 17.99,
                "stock": 3,
                "purchases": 27,
                "updated": datetime.now()
                }
        dbconn[settings.ITEMS_COLL].insert(item)
        response = self.get(self.itemspath + '1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_found(self):
        '''ItemControllerTest test GET single Item not found error
        '''
        response = self.get(self.itemspath + '222/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put(self):
        '''ItemControllerTest test PUT single Item
        '''
        global dbconn
        item = {"id": 1,
                "name": "Super item",
                "description": "This is the most amazing super item",
                "category": "Strange items",
                "price": 17.99,
                "stock": 3,
                "purchases": 27,
                "updated": datetime.now()
                }
        dbconn[settings.ITEMS_COLL].insert(item)
        response = self.put(self.itemspath + '1/', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)

    def test_put_not_found(self):
        '''ItemControllerTest test PUT single Item not found error
        '''
        response = self.put(self.itemspath + '1111/', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_delete(self):
        '''ItemControllerTest test DELETE single Item
        '''
        item = {"name": "Super item 2", "description": "This is the most amazing super item 2",
                "category": "Strange items 2", "price": 17.99, "stock": 3
                }
        response = self.post(self.itemspath, data=json.dumps(item))
        new_item = json.loads(response.content)
        response = self.delete(self.itemspath + str(new_item['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        '''ItemControllerTest test DELETE single Item not found
        '''
        response = self.delete(self.itemspath + '157/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post(self):
        '''ItemControllerTest test POST single Item error
        '''
        response = self.post(self.itemspath + '1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


def setUpModule():
    '''
    Restore settings DBNAME while running tests
    '''
    settings.MONGODB['dbname'] = settings.MONGODB['dbname'] + '_api_tests'
    if not settings.MONGODB['slave_ok']:
        read_preference = ReadPreference.PRIMARY
    else:
        read_preference = ReadPreference.SECONDARY
    global conn
    global dbconn
    conn = Connection(settings.MONGODB['hosts'][0],
                      safe=settings.MONGODB['savemode'],
                      replicaset=settings.MONGODB['replicaset'],
                      read_preference=read_preference)
    dbconn = conn[settings.MONGODB['dbname']]
#    print "CONNECTED TO DB", settings.MONGODB['DBNAME'], "@", settings.MONGODB['HOSTS'][0]


def tearDownModule(cls):
    global conn
    pass
#    conn.drop_database(settings.MONGODB['dbname'])
