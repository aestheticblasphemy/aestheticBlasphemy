'''
Created on 23-Jun-2016

@author: craft
'''
from django.apps import AppConfig

class BloggingConfig(AppConfig):
    name = 'blogging'
    verbose_name = "Blogging App."
    
    def ready(self):
        try:
            BlogContentType = self.get_model('BlogContentType')
            defaultSection = BlogContentType.objects.filter(content_type='defaultsection')
            if len(defaultSection) == 0:
                defaultSection = BlogContentType()
                defaultSection.content_type='defaultsection'
                defaultSection.is_leaf = False
                defaultSection.save()
            defaultBlog = BlogContentType.objects.filter(content_type='defaultblog')
            if len(defaultBlog) == 0:
                defaultBlog = BlogContentType()
                defaultBlog.content_type='defaultblog'
                defaultBlog.is_leaf = True
                defaultBlog.save()
        except:
            print('Something is wrong')
