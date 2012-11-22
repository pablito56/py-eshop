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
# Django ReST fwk imports
from rest_framework.exceptions import ParseError


class ItemsService(object):
    '''Business logic to handle Items
    '''
    ids = ["name", ]
    required = ["price", "stock"]
    not_modify = ["id", "purchases"]
    update_incrementally = ["stock"]
    has_updated = True
    
    itemslst = [{"id": "1",
                  "name": "Super item",
                  "description": "This is the most amazing super item",
                  "category": "Strange items",
                  "price": 17.99,
                  "stock": 3,
                  "purchases": 27,
                  "updated": datetime(2012, 11, 16, 12, 0, 0)
                  }]

    def create(self, new):
        '''Create a new Item
        '''
        for id_field in self.ids:
            if not id_field in new:
                raise ParseError("Not found identifier '{0}'".format(id_field))
        for req_field in self.required:
            if not req_field in new:
                raise ParseError("Not found required field '{0}'".format(req_field))
        if self.has_updated:
            new["updated"] = datetime.now()
        new['id'] = str(len(self.itemslst) + 1)
        self.itemslst.append(new)
        return new

    def get_all(self):
        '''Retrieve all Items
        '''
        return self.itemslst

    def get_one(self, resource_id):
        '''Retrieve single Item
        '''
        result = filter(lambda x: x['id'] == resource_id, self.itemslst)
        if result:
            return result[0]
        raise Http404()

    def update(self, resource_id, new):
        '''Update one Item
        '''
        old = filter(lambda x: x['id'] == resource_id, self.itemslst)
        if not old:
            raise Http404()
        for nm_field in self.not_modify:
            new.pop(nm_field, None)
        if self.has_updated:
            new["updated"] = datetime.now()
        for ui_field in self.update_incrementally:
            if ui_field in new:
                new[ui_field] += old[0][ui_field] 
        new.pop("id", None)
        old[0].update(new)
        return True

    def delete(self, resource_id):
        '''Delete one Item
        '''
        result = filter(lambda x: x['id'] == resource_id, self.itemslst)
        if not result:
            raise Http404()
        self.itemslst.remove(result[0])
        return True
