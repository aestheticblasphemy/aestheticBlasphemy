from django.conf.urls import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from views import (api_root, BlogContentViewSet, 
                   UserViewSet, AnnotationViewSet, 
                   BlogContentCommentView, CurrentUserView)

from rest_framework.urlpatterns import format_suffix_patterns


blogcontent_list = BlogContentViewSet.as_view({
    'get': 'list'                                           
    })
blogcontent_detail = BlogContentViewSet.as_view({
    'get': 'retrieve',
    })

user_list = UserViewSet.as_view({
    'get': 'list'
    })
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
    })

annotation_list = AnnotationViewSet.as_view({
    'get': 'list',
    'post': 'create'
    })
annotation_detail = AnnotationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
    })

urlpatterns = ['rest.views',
    url(r'^$', api_root),
    url(r'^blogcontent/$', blogcontent_list, name='blogcontent-list'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/$', blogcontent_detail, name='blogcontent-detail'),
    url(r'^blogcontent/(?P<pk>[0-9]+)/comments/$', BlogContentCommentView.as_view(), name='blogcontent-comments'),
    
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/current/$', CurrentUserView.as_view(), name='current-user'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    
    url(r'^annotations/$', annotation_list, name='annotations-list'),
    url(r'^annotations/(?P<pk>[0-9]+)/$', annotation_detail, name='annotations-detail'),
]

urlpatters = format_suffix_patterns(urlpatterns)