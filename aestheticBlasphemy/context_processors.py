from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject

from django.core.urlresolvers import reverse

from meta_tags.views import Meta

def site_processor(request):
    return {
        'site': SimpleLazyObject(lambda: get_current_site(request)),
        'feed_meta': Meta(title = None, 
                        description = None, 
                        section= None, 
                        url = None,
                        image = None, 
                        author = None, 
                        date_time = None,
                        object_type = None, 
                        keywords = None,
                        feed_list = [{'url':reverse('blogging:latest-posts-feed'),
                                     'title': 'Blog Post Feed'}]
                        )
            }