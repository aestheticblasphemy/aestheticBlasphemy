from __future__ import unicode_literals

from django.db import models
from aestheticBlasphemy.models import BaseContentClass
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe


from blogging.models import BlogContent

def truncatewords(Value,limit=30):
    try:
        limit = int(limit)
        # invalid literal for int()
    except ValueError:
        # Fail silently.
        return Value

    # Make sure it's unicode
    Value = unicode(Value)

    # Return the string itself if length is smaller or equal to the limit
    if len(Value) <= limit:
        return Value

    # Cut the string
    Value = Value[:limit]

    # Break into words and remove the last
    words = Value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'

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
    
    def get_absolute_url(self):
        kwargs = {'cid': self.id}
        return reverse("comments:view-comment", kwargs=kwargs)
    
    def get_summary(self):
        description = self.body
        return mark_safe(truncatewords(description,50))
    
    def __unicode__(self):
        return self.body
    
    def __str__(self):
        return self.body
    
    class Meta:
        app_label = 'comments'

