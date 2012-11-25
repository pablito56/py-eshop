#-*- coding: utf-8 -*-
u'''
Created on Nov 19, 2012

@author: pev
'''
# Django ReST fwk imports
from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    '''Serializer fot Item documents
    '''
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=500, required=False)
    category = serializers.CharField(max_length=150, required=False)
    price = serializers.FloatField()
    stock = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        """Create or update a new Item (dict) instance.
        """
        return dict(attrs)


class ItemUpdateSerializer(serializers.Serializer):
    '''Serializer fot Item documents (when updating)
    '''
    name = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=500, required=False)
    category = serializers.CharField(max_length=150, required=False)
    price = serializers.FloatField(required=False)
    stock = serializers.IntegerField(required=False)

    def restore_object(self, attrs, instance=None):
        """Create or update a new Item (dict) instance.
        """
        return dict(attrs)

    def validate(self, attrs):
        '''Custom validate method to ensure that at least one field is provided
        '''
        if super(ItemUpdateSerializer, self).validate(attrs):
            req_fields = ["name", "description", "category", "price", "stock"]
            for f in req_fields:
                if f in attrs:
                    return attrs
        raise serializers.ValidationError("No Item fields provided for update")

class UserSerializer(serializers.Serializer):
    '''Serializer fot User documents
    '''
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=150)
    surname = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    address = serializers.CharField(max_length=150)

    def restore_object(self, attrs, instance=None):
        """Create or update a new User (dict) instance.
        """
        return dict(attrs)

class UserUpdateSerializer(serializers.Serializer):
    '''Serializer fot User documents
    '''
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=150, required=False)
    surname = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(max_length=150, required=False)
    address = serializers.CharField(max_length=150, required=False)

    def restore_object(self, attrs, instance=None):
        """Create or update a new User (dict) instance.
        """
        return dict(attrs)

class CartItemSerializer(serializers.Serializer):
    '''Serializer for Item's for cart
    '''
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def restore_object(self, attrs, instance=None):
        """Create or update a new Item (dict) instance.
        """
        return dict(attrs)
