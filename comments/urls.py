'''
Created on 09-Jun-2016

@author: craft
'''
from django.conf.urls import include, url
from comments.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^(?P<postID>\d+)/$', CommentList.as_view(), name='view-comments-by-post'),
    url(r'^(?P<postID>\d+)(?:/)?(?P<commentID>\d+)?/form/$', comment_form),
    url(r'^comment/(?P<cid>\d+)$', comment_detail, name="view-comment"),
    url(r'^comment-list/$', CommentList.as_view(), {'postID':None}, name='view-comments'),

    url(r'^approve/$',comment_approve),

    url(r'^$', comment_post),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)