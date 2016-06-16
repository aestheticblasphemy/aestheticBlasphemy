'''
Created on 09-Jun-2016

@author: craft
'''
from django.conf.urls import include, url
from .views import *

urlpatters = [
    url(r'^(?P<postID>\d+)/$', comment_list),
    url(r'^comment/(?<cid>\d+)$', comment_detail),
    ]