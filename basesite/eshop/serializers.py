#-*- coding: utf-8 -*-
u'''
Created on Nov 19, 2012

@author: pev
'''
# Standard library imports
from datetime import datetime
# Django imports
from django.forms import widgets
# Django ReST fwk imports
from rest_framework import serializers
# Custom import
from documents import Item


class ItemSerializer(serializers.Serializer):
    '''Serializer fot Item documents
    '''
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500, required=False)
    # TODO: Make categories a ChoiceField
    category = serializers.CharField(max_length=200, required=False)
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    updated = serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance.
        """
        if instance:
            print "Updating Item", instance, "with", attrs
            stock = attrs.pop("stock", 0)
            id = attrs.pop("id", None)
            instance.update(attrs)
            # Update existing instance
            instance.stock += stock
            instance.updated = datetime.now()
            return instance
        print "Creating Item with", attrs
        # Create new instance
        return dict(attrs)
