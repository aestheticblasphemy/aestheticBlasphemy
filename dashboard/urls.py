__author__ = 'Abhishek Rai'

from django.conf.urls import include, url
from .views import *
urlpatterns = [
    url(r'^$',dashboard_home, name='dashboard-home'),
    url(r'^(?P<user_id>\d+)/profile/?$',dashboard_profile, name='dashboard-profile'),
    url(r'^manage-articles/?$',manage_articles, name='dashboard-admin-articles'),
    url(r'^published/?$',published_articles, name='dashboard-published'),
    url(r'^pending/?$',pending_articles, name='dashboard-pending'),
    url(r'^draft/?$',draft_articles, name='dashboard-draft'),
    url(r'^bookmarks/?$',bookmark_articles, name='dashboard-bookmarks'),
]