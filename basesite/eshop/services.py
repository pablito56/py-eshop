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
from django.conf import settings
# Django ReST fwk imports
from rest_framework.exceptions import ParseError
# Custom eshop imports
from daos import ItemsDao


class ItemsService(object):
    '''Business logic to handle Items
    '''
    required = ["name", "price", "stock"]
    not_modify = ["id", "purchases"]
    update_incrementally = ["stock"]

    dao = ItemsDao()

    def create(self, new):
        '''Create a new Resource
        '''
        for req_field in self.required:
            if not req_field in new:
                raise ParseError("Not found required field '{0}'".format(req_field))
        new["updated"] = datetime.now()
        return self.dao.insert(new)

    def get_all(self):
        '''Retrieve all Resources
        '''
        return list(self.dao.find_all())

    def get_one(self, resource_id):
        '''Retrieve single Resource
        '''
        try:
            resource = self.dao.find(int(resource_id))
        except ValueError:
            raise Http404()
        if resource:
            return resource
        raise Http404()

    def update(self, resource_id, new):
        '''Update one Resource
        '''
        try:
            old = self.dao.find(int(resource_id))
        except ValueError:
            raise Http404()
        if not old:
            raise Http404()
        new["updated"] = datetime.now()
        try:
            self.dao.update(int(resource_id), new)
        except ValueError:
            raise Http404()
        return True

    def delete(self, resource_id):
        '''Delete one Resource
        '''
        try:
            old = self.dao.find(int(resource_id))
        except ValueError:
            raise Http404()
        if not old:
            raise Http404()
        try:
            return self.dao.remove(int(resource_id))
        except ValueError:
            raise Http404()
