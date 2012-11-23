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
        dbconn.drop_collection(settings.IDS_COLL)

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
        item = {"name": "Super item 12345", "description": "This is the most amazing super item 12345",
                "category": "Strange items", "price": 17.99, "stock": 3
                }
        response = self.post(self.itemspath, data=json.dumps(item))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        db_item = dbconn[settings.ITEMS_COLL].find_one({'id': 1})
        del db_item['_id']
        del db_item['id']
        del db_item['updated']
        self.assertEqual(db_item, item)

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

    def test_get_wrong_id(self):
        '''ItemControllerTest test GET single Item not found error for wrong id format
        '''
        response = self.get(self.itemspath + 'abcd')
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
        expected_desc = 'new description'
        response = self.put(self.itemspath + '1/', json.dumps({'description': expected_desc}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        db_item = dbconn[settings.ITEMS_COLL].find_one({'id': 1})
        self.assertTrue(db_item["updated"] >= item["updated"])
        self.assertEqual(db_item["description"], expected_desc)

    def test_put_stock(self):
        '''ItemControllerTest test PUT single Item incrementing stock
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
        expected_cat = 'new cat'
        new_stock = -2
        response = self.put(self.itemspath + '1/', json.dumps({'category': expected_cat,
                                                               'stock': new_stock}))
        expected_stock = item['stock'] + new_stock
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        db_item = dbconn[settings.ITEMS_COLL].find_one({'id': 1})
        self.assertTrue(db_item["updated"] >= item["updated"])
        self.assertEqual(db_item["category"], expected_cat)
        self.assertEqual(db_item["stock"], expected_stock)

    def test_put_not_found(self):
        '''ItemControllerTest test PUT single Item not found error
        '''
        response = self.put(self.itemspath + '1111/', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_put_wrong_id(self):
        '''ItemControllerTest test PUT single Item not found error for wrong id format
        '''
        response = self.put(self.itemspath + 'xyz', json.dumps({'description': 'new description'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_delete(self):
        '''ItemControllerTest test DELETE single Item
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
        response = self.delete(self.itemspath + str(item['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check DB content
        self.assertEqual(dbconn[settings.ITEMS_COLL].count(), 0)

    def test_delete_not_found(self):
        '''ItemControllerTest test DELETE single Item not found
        '''
        response = self.delete(self.itemspath + '157/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wrong_id(self):
        '''ItemControllerTest test DELETE single Item not found for wrong id format
        '''
        response = self.delete(self.itemspath + 'klm')
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
