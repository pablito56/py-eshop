#-*- coding: utf-8 -*-
u'''
Created on Nov 21, 2012

@author: pev

For nose and coverage reporting use this settings:
python manage.py test eshop --settings basesite.settingstests
'''
from settings import *


INSTALLED_APPS = INSTALLED_APPS + ('django_nose', )


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


NOSE_ARGS = ['-s',
             '-v',
             '--cover-erase',
             '--cover-branches',
             '--with-cov',
             '--cover-xml',
             '--cover-package=frappe_api',
             '--cover-xml-file=../coverage.xml',
             '--with-xunit',
             '--xunit-file=../nosetests.xml'
             ]
