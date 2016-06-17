'''
Created on 16-Jun-2016

@author: craft
'''
from django.test import TestCase
from django.http import HttpRequest

from blogging.views import teaser
from django.template.loader import render_to_string
from django.conf import settings

class BloggingViewsTest(TestCase):

    def test_teaser_without_slug(self):
        """
        Tests the main summary page.
        """
        request = HttpRequest()
        response = teaser(request, slug=None)
        
        expected_html = render_to_string('blogging/teaser.html',
                                         dictionary={'parent':None,
                                                     'nodes': None,
                                                     'page': {'title':settings.SITE_TITLE, 
                                                              'tagline':settings.SITE_TAGLINE, 
                                                              'image': None
                                                              }})

        self.assertEqual(response.content.decode(), 
                         expected_html, 
                         "Template HTML do not match")
        