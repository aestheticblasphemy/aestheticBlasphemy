'''
Created on 09-Jun-2016

@author: craft
'''

from django.urls import path, re_path, include
from comments.views import *
from rest_framework.urlpatterns import format_suffix_patterns

app_name="comments"

comment_post = CommentPost.as_view({
    'post': 'create'
    })

urlpatterns = [
    re_path(r'^(?P<postID>\d+)/$', CommentList.as_view(), name='view-comments-by-post'),
    re_path(r'^(?P<postID>\d+)(?:/)?(?P<commentID>\d+)?/form/$', comment_form),
    re_path(r'^comment/(?P<cid>\d+)$', comment_detail, name="view-comment"),
    re_path(r'^comment-list/$', CommentList.as_view(), {'postID':None}, name='view-comments'),

    re_path(r'^approve/$',comment_approve, name='comments-approval'),
    re_path(r'^manage/$', comment_list, name='comments-manage'),
    re_path(r'^$', comment_post, name="comment-post"),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)