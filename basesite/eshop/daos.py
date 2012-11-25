#-*- coding: utf-8 -*-
u'''
Created on Nov 19, 2012

@author: pev
@author: jacobcr
'''
# Standard lib imports
from itertools import repeat
# Django imports
from django.conf import settings
# PyMongo imports
from pymongo import Connection, ReadPreference, ASCENDING
from pymongo.errors import AutoReconnect


_db_connection = None


def _get_connection(**dbconfig):
    '''Retrieve or create DB connection. It is handled as singleton to avoid reconnecting in each request
    :param hosts: hosts list (string of the format 'hostname:port')
    :param dbname: database name
    :param savemode: safe or not (boolean)
    :param slave_ok: preference to read from the secondary node
    :param replicaset: replicaset to connect to
    :param autostart: auto_start_request (one socket allocated per thread)
    '''
    if not dbconfig:
        dbconfig = settings.MONGODB
    global _db_connection
    if _db_connection is None:
        for host in dbconfig["hosts"]:
            try:
                if dbconfig["slave_ok"]:
                    read_preference = ReadPreference.SECONDARY
                else:
                    read_preference = ReadPreference.PRIMARY
                _db_connection = Connection(host,
                                            safe=dbconfig["savemode"],
                                            replicaset=dbconfig["replicaset"],
                                            read_preference=read_preference,
                                            auto_start_request=dbconfig["autostart"])
                return _db_connection[dbconfig["dbname"]]
            except AutoReconnect:
                print "Cannot connect to '{0}' trying next host".format(host)
        raise SystemError("Cannot establish connection with hosts {0}".format(dbconfig["hosts"]))
#    print "CONNECTED TO DB", _MONGODB['DBNAME'], "@", _MONGODB['HOSTS'][0]
    return _db_connection[dbconfig["dbname"]]


class BaseDao(object):
    '''DAO holding basic common DAO features
    '''

    def __init__(self):
        '''Constructor
        '''
        if self.coll is None:
            raise NotImplementedError("{0}.coll method must defined when overriding".format(self.__class__.__name__))
        self.dbconn = _get_connection()
        self.dbcoll = self.dbconn[self.coll]

    def _get_id_value(self):
        '''Retrieve max new value of the id for DAO collection
        :param coll_name: name of the collection whose max counter has to be retrieved
        :return counter value
        '''
        coll = self.dbconn[settings.IDS_COLL]
        counter_doc = coll.find_and_modify(query={'_id': self.coll},
                                           update={'$inc': {'val': 1}},
                                           upsert=True,
                                           safe=True,
                                           new=True)
        return counter_doc['val']


class ItemsDao(BaseDao):
    '''Dao to handle 'items' documents
    '''
    coll = settings.ITEMS_COLL

    def __init__(self, *args, **kwargs):
        '''Instantiate DAO and set unique index for 'name'
        '''
        super(ItemsDao, self).__init__(*args, **kwargs)
        keys_list = [("name", ASCENDING)]
        self.dbcoll.ensure_index(keys_list, name='unique_name', unique=True)

    def insert(self, item_doc, safe=True):
        '''Insert a new Item document
        :param item_doc: document to store to the DB
        :param safe: validate operation (slower)
        :raises DuplicateKeyError with safe=True
        '''
        item_doc.pop("_id", None)
        item_doc["id"] = self._get_id_value()
        self.dbcoll.insert(item_doc, safe=safe)
        item_doc.pop("_id", None)
        return item_doc

    def find(self, id):
        '''Find one item document by its ids
        :param id: id values to retrieve
        :returns retrieved document or None
        '''
        dbdoc = self.dbcoll.find_one({"id": id}, {"_id": 0})
        return dbdoc

    def find_all(self):
        '''Find Items documents
        :returns retrieved documents cursor
        '''
        return self.dbcoll.find(fields={"_id": 0})

    def update(self, id, doc, safe=True):
        '''Update a single DB document
        :param id: id of the Item to be updated
        :param doc: new Item document
        :param safe: validate operation (slower)
        '''
        doc.pop("_id", None)
        db_doc = {"$set": doc}
        # Stock must be incremented, not updated
        if "stock" in doc:
            db_doc["$inc"] = {"stock": doc["stock"]}
            del doc["stock"]
        res = self.dbcoll.update({"id": id}, db_doc, upsert=False, safe=safe)
        if safe:
            if res.get('ok', False) and res.get('n', 0) == 1 and res.get('updatedExisting', False):
                return True
            return False
        return True

    def remove(self, id, safe=True):
        '''Remove one document by its id
        :param id: id of the Item to remove
        :returns remove result
        '''
        res = self.dbcoll.remove({"id": id}, safe=safe)
        if safe:
            if res.get('ok', False) and res.get('n', 0) == 1:
                return True
            return False
        return True

class UsersDao(BaseDao):
    '''Dao to handle 'items' documents
    '''
    coll = settings.USERS_COLL

    def __init__(self, *args, **kwargs):
        '''Instantiate DAO and set unique index for 'name'
        '''
        super(UsersDao, self).__init__(*args, **kwargs)
        keys_list = [("name", ASCENDING), ("surname", ASCENDING)]
        self.dbcoll.ensure_index(keys_list, name='unique_name_surname', unique=True)

    def insert(self, user_doc, safe=True):
        '''Insert a new User document
        :param item_doc: document to store to the DB
        :param safe: validate operation (slower)
        :raises DuplicateKeyError with safe=True
        '''
        user_doc.pop("_id", None)
        user_doc["id"] = self._get_id_value()
        self.dbcoll.insert(user_doc, safe=safe)
        user_doc.pop("_id", None)
        return user_doc

    def find(self, id):
        '''Find one item document by its ids
        :param id: id values to retrieve
        :returns retrieved document or None
        '''
        return self.dbcoll.find_one({"id": id}, {"_id": 0})

    def find_all(self):
        '''Find Users documents
        :returns retrieved documents cursor
        '''
        return self.dbcoll.find(fields={"_id": 0})

    def update(self, id, doc, safe=True):
        '''Update a single DB document
        :param id: id of the User to be updated
        :param doc: new Item document
        :param safe: validate operation (slower)
        '''
        doc.pop("_id", None)
        db_doc = {"$set": doc}
        res = self.dbcoll.update({"id": id}, db_doc, upsert=False, safe=safe)
        if safe:
            if res.get('ok', False) and res.get('n', 0) == 1 and res.get('updatedExisting', False):
                return True
            return False
        return True

    def remove(self, id, safe=True):
        '''Remove one document by its id
        :param id: id of the User to remove
        :returns remove result
        '''
        res = self.dbcoll.remove({"id": id}, safe=safe)
        if safe:
            if res.get('ok', False) and res.get('n', 0) == 1:
                return True
            return False
        return True

    def add_to_cart(self, user_id, item_id, name, price, quantity):
        res = self.dbcoll.find_and_modify(query={'id': user_id, 'cart.id': item_id}, update={'$set': {'cart.$.name': name, 'cart.$.price': price}, '$inc':
                    {'cart.$.quantity': quantity}}, safe=True, new=True)
        if res:
            return res['cart']
        doc = {'id': item_id, 'name': name, 'price': price, 'quantity': quantity}
        res = self.dbcoll.update({'id': user_id}, {'$addToSet': {'cart': doc}}, safe=True)
        if res.get('ok', False) and res.get('n', 0) == 1 and res.get('updatedExisting', False):
            return doc
