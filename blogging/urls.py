from django.conf.urls import url
import blogging.views as view

urlpatterns = [
    url(r'^sections/(?P<slug>.*)$', view.index, name='view-sections'),

    url(r'^$', view.teaser, {'slug':None}, name='view-posts-by-section'),
    url(r'^(?P<slug>[\w.+-/]+)/(?P<post_id>\d+)/$', view.detail, name='view-post-detail'),
    url(r'^(?P<slug>[\w.+-/]+)/$', view.teaser, name='view-posts-by-section'),
    
    url(r'^testing/$',view.testCase,name='migrate-db'),
    url(r'^contact/$', view.ContactUs, name='contact-us'),
    
    url(r'^create-post/$', view.new_post, name='create-post'),
    url(r'^edit-post/(?P<post_id>\d+)/$', view.edit_post, name='edit-post'),
    url(r'^edit-section/(?P<section_id>\d+)/$', view.edit_section, name='edit-section'),
    
    url(r'^content-type/$', view.content_type, name='content-type'),
    url(r'^get-index/?$', view.BuildIndex, name='build-index'),
    url(r'^add-model/(?P<model_name>[\w.+-/]+)/$', view.add_new_model, name='add-model-content-type'),
    
    url(r'^author/$', view.authors_list, name='author-list'),
    url(r'^author/(?P<slug>[\w.@+-]+)/(?P<post_id>\d+)$', view.author_post, name='author-posts'),
    
#    url(r'^feed/$', LatestEntriesFeed(), name='latest-posts-feed'),
    url(r'^(?P<year>\d{4})/$', view.archive, name='archive-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', view.archive, name='archive-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', view.archive, name='archive-day'),
#    url(r'^(?P<slug>[\w.+-/]+)/(?P<post_id>\d+)$', view.detail, name='post-detail'),

    url(r'^tag/(?P<tag>[-\w]+)/$', view.tagged_post, name='tagged-posts'),
    url(r'^manage/$', view.manage , name='manage_articles'),
]
