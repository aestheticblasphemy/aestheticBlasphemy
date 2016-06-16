'''
Created on 16-Jun-2016

@author: craft
'''
from django.core.urlresolvers import resolve
from django.test import TestCase

from blogging import views as blog_view

import aestheticBlasphemy

from django.test import Client
class URLTests(TestCase):
    def test_homepage(self):
        found = resolve('/', 
                        urlconf=aestheticBlasphemy.settings.ROOT_URLCONF)
        self.assertEqual(found.func, blog_view.teaser, 
                         '{found} is not {ref}'.format(found=found.func,
                                                       ref=blog_view.teaser))
    def test_Client(self):
        c = Client()
        response = c.get('/')
        print response