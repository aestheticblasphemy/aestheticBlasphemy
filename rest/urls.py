from django.urls import path, re_path, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from django.contrib.contenttypes.views import shortcut

from .views import (api_root, BlogContentViewSet, 
                   UserViewSet, CurrentUserView)

from rest_framework.urlpatterns import format_suffix_patterns

app_name="rest"

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


urlpatterns = [
    re_path(r'^$', api_root),
    re_path(r'^blogcontent/$', blogcontent_list, name='blogcontent-list'),
    re_path(r'^blogcontent/(?P<pk>[0-9]+)/$', blogcontent_detail, name='blogcontent-detail'),
    
    re_path(r'^users/$', user_list, name='user-list'),
    re_path(r'^users/current/$', CurrentUserView.as_view(), name='current-user'),
    re_path(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    
    ]

urlpatters = format_suffix_patterns(urlpatterns)
