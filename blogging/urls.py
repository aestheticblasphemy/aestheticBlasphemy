from django.urls import path, re_path

import blogging.views as view
from blogging.feeds import LatestBlogEntiresFeed

app_name="blogging"

urlpatterns = [
    path('', view.teaser, {'slug':None}, name='view-posts-by-section'),

    re_path(r'^sections/(?P<slug>.*)/?$', view.section_index, name='view-sections'),
    re_path(r'^edit-section/(?P<section_id>\d+)/$', view.edit_section, name='edit-section'),

    path('contact/', view.ContactUs, name='contact-us'),

    path('create-post/', view.new_post, name='create-post'),
    re_path(r'^edit-post/(?P<post_id>\d+)/$', view.edit_post, name='edit-post'),

    path('content-type/', view.content_type, name='content-type'),
    path('get-index/', view.BuildIndex, name='build-index'),
    re_path(r'^add-model/(?P<model_name>[\w.+-/]+)/$', view.add_new_model, name='add-model-content-type'),

    path('author/', view.authors_list, name='author-list'),
    re_path(r'^author/(?P<slug>[\w.@+-]+)/(?P<post_id>\d+)$', view.author_post, name='author-posts'),

    path('tag/<str:tag>/', view.tagged_post, name='tagged-posts'),
    path('manage/', view.manage , name='manage_articles'),

    path('feed/', LatestBlogEntiresFeed(), name='latest-posts-feed'),

    re_path(r'^(?P<slug>[a-z0-9.+-/]+)/(?P<post_id>\d+)/?$', view.detail, name='view-post-detail'),

    re_path(r'^(?P<year>\d{4})/$', view.archive, name='archive-year'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', view.archive, name='archive-month'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', view.archive, name='archive-day'),
    re_path(r'^(?P<slug>[a-z0-9.+-/]+)/$', view.teaser, name='view-posts-by-section'),
#    url(r'^(?P<slug>[\w.+-/]+)/(?P<post_id>\d+)$', view.detail, name='post-detail'),

]
