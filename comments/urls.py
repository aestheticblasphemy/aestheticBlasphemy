'''
Created on 09-Jun-2016

@author: craft
'''
from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^(?P<postID>\d+)/$', comment_list),
    url(r'^(?P<postID>\d+)(?:/)?(?P<commentID>\d+)?/form/$', comment_form),
    url(r'^comment/(?P<cid>\d+)$', comment_detail),

    url(r'^$', comment_post),
    ]