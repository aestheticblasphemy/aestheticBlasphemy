from __future__ import unicode_literals

from django.db import models
from aestheticBlasphemy.models import BaseContentClass
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from blogging.models import BlogContent

# Create your models here.
class Comment(BaseContentClass):
    post = models.ForeignKey(BlogContent, related_name="comments", null=False)
    body = models.TextField()
    
    author = models.ForeignKey(User, related_name="comments", 
                               null=True,
                               verbose_name=_("Annotation author"))
    author_name = models.CharField(max_length=50, null=True)
    author_email = models.EmailField(null=True)
    author_url = models.URLField(null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    parent_comment = models.ForeignKey('self', 
                                       on_delete=models.CASCADE,
                                       verbose_name=_("Parent Comment"),
                               related_name="parent_comment_for_comment",
                               null=True
                               )
    published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.body
    
    def __str__(self):
        return self.body
    
    class Meta:
        app_label = 'comments'

