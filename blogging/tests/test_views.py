'''
Created on 16-Jun-2016

@author: craft
'''
from django.test import TestCase

class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1+1+1, 3, 'Your maths is wrong!')