from django.utils import timezone

import sys
from django.db import models
from django.db.models import Q

from django.contrib import auth
from mptt.models import MPTTModel, TreeForeignKey
#from treebeard.mp_tree import MP_Node

from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItem, Tag


from django.conf import settings
from django.db.models import Count, Sum

from blogging.utils import get_imageurl_from_data, truncatewords, slugify_name
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from django.urls import reverse

import reversion

import traceback
import json

from aestheticBlasphemy.models import BaseContentClass

use_reversion = getattr(settings, 'BLOGGING_USE_REVERSION', False)
if use_reversion:
    import reversion
#from south.v2 import DataMigration

# Create your models here.

LATEST_PLUGIN_TEMPLATES = (
  ('blogging/plugin/plugin_teaser.html', 'Teaser View'),
  ('blogging/plugin/plugin_section.html', 'Section View'),
  ('blogging/plugin/sidebar_list.html', 'Text List'),
  ('blogging/plugin/teaser_list.html', 'Stacked List'),
)


class RelatedManager(models.Manager):

    def get_queryset(self):
        qs = super(RelatedManager, self).get_queryset()
        return qs

    def get_tags(self, language):
        """Returns tags used to tag post and its count. Results are ordered by count."""

        # get tagged post
        entries = self.get_query_set().distinct()
        if not entries:
            return []
        kwargs = TaggedItem.bulk_lookup_kwargs(entries)

        # aggregate and sort
        counted_tags = dict(TaggedItem.objects
                                      .filter(**kwargs)
                                      .values('tag')
                                      .annotate(count=models.Count('tag'))
                                      .values_list('tag', 'count'))

        # and finally get the results
        tags = Tag.objects.filter(pk__in=list(counted_tags.keys()))
        for tag in tags:
            tag.count = counted_tags[tag.pk]
        return sorted(tags, key=lambda x: -x.count)

class PublishedManager(RelatedManager):
    def get_queryset(self):
        qs = super(PublishedManager, self).get_queryset()
        now = timezone.now()
        qs = qs.filter(publication_start__lte=now)
        qs = qs.filter(Q(published_flag=True)).order_by('-publication_start')
        return qs



class BlogContentType(BaseContentClass):
    """
    This class is used to create composite content-types for content creation or
    new sections.
    """
    content_type = models.CharField(max_length = 100,unique = True)
    is_leaf = models.BooleanField('Is leaf node?', default = 0)

    def __unicode__(self):
        return self.content_type

    def __str__(self):
        return str(self.content_type) or ''

    def save(self, *args, **kwargs):
        self.content_type = slugify_name(self.content_type)
        super(BlogContentType, self).save(*args, **kwargs)

from mptt.managers import TreeManager

class BlogParent(MPTTModel):
#class BlogParent(MP_Node):
    """
    This represents the Parent Section of any other section or of a Blog Content
    Sections can be made into tree-like hierarchies depending on how the user
    wants to organize their data.
    As a rule, if an Article belongs to Section A, which is a child of Section B
    then the article implicitly belongs to Section B also (while driving views).

    There would be cases when an article is not assigned to any section. A ghost
    section is created on setup to handle such cases. This 'Orphan' section is
    the default section for any article created without a section.
    """
    title = models.CharField(max_length = 50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
    #parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
					db_index=True,on_delete = models.SET_NULL)

    #node_order_by = ['title']
    data = models.TextField(null= False)
    content_type = models.ForeignKey(BlogContentType,null=True,default=None,
							on_delete = models.SET_NULL)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        blogs = BlogContent.objects.filter(section=self.parent)
        if blogs:
            try:
                orphan_parent = BlogParent.objects.get(title='Orphan')
                for blog in blogs:
                    blog.section = orphan_parent
                    blog.save()
            except:
                print('FATAL ERROR CAN DO NOTHING')
        super(BlogParent, self).save(*args, **kwargs)

    def form_url(self):
        parent_list = self.get_ancestors(include_self=True)
        return_path = '/'.join(word.slug for word in parent_list)
        #print( "inside absolute URL ", return_path)
        return return_path

    def get_image_url(self):
        try:
            json_obj = json.loads(self.data)
            for value in json_obj.values():
                image =  get_imageurl_from_data(value)
                if image:
                    return image
        except:
            return get_imageurl_from_data(self.data)
        return ""

    def get_absolute_url(self):
        kwargs = {'slug': str(self.form_url())}
        return reverse('blogging:view-sections', kwargs=kwargs)

    def get_content_url(self):
        kwargs = {'slug': str(self.form_url())}
        return reverse('blogging:view-posts-by-section', kwargs=kwargs)

    def get_menu_title(self):
        return self.title

    def get_child_count(self):
        return self.children.count()

    def get_article_count(self):
        return BlogContent.published.filter(section = self).count()


    def get_title(self):
        return self.title

    class MPTTMeta:
            order_insertion_by = ['title']

class BlogContent(BaseContentClass):
    """
    Class representing the Blog Content. This contains the actual post/article.
    """
    title = models.CharField(max_length = 100)
    data = models.TextField(null= False)
    author_id = models.ForeignKey(auth.models.User, related_name="blogcontent",
								on_delete = models.CASCADE)

    create_date = models.DateTimeField('date created', auto_now_add=True)
    last_modified = models.DateTimeField('date modified',auto_now=True)

    published_flag = models.BooleanField('is published?',default = 0)
    publication_start = models.DateTimeField('published on',
                                          null=True,
                                          blank=True,
                                          default=None)
    special_flag = models.BooleanField(default = 0)

    url_path = models.CharField(max_length= 255)
    section = models.ForeignKey(BlogParent,
							on_delete = models.CASCADE)

    content_type = models.ForeignKey(BlogContentType,null=True,
							on_delete = models.SET_NULL)
    slug = models.SlugField(max_length= 100)

    tags = TaggableManager(blank=True)

    objects = RelatedManager()
    published = PublishedManager()

    def get_absolute_url(self):
        kwargs = {'slug': self.url_path,
                  'post_id': self.id,}
        #print "LOGS:: Fetching URI for node", self.id, self.slug
        return reverse('blogging:view-post-detail', kwargs=kwargs)

    def get_image_url(self):
        try:
            json_obj = json.loads(self.data)
            for value in list(json_obj.values()):
                image =  get_imageurl_from_data(value)
                if image:
                    return image
            return self.section.get_image_url()
        except:
            image =  get_imageurl_from_data(self.data)
            if image:
                return image
            return self.section.get_image_url()
    def get_summary(self):
        json_obj = json.loads(self.data)
        # Instantiate the Meta class
        description = strip_tags(list(json_obj.values())[0])
        return mark_safe(truncatewords(description,120))


    def get_title(self):
        return self.title


    def find_path(self,section):
        parent_list = section.get_ancestors(include_self=True)
        return_path = '/'.join(word.slug for word in parent_list)
        return_path = return_path + str("/") + self.slug
        #print(return_path)
        return return_path

    def get_menu_title(self):
        return self.title

    def get_parent(self):
        return self.section

    def get_tags(self):
        tags = self.tags.all()
        tag_list = []
        for tag in tags:
            try:
                tmp = {}
                tmp['name'] = tag.name
                #print(tag.name)
                kwargs = {'tag': tag.name,}
                tmp['url'] = reverse('blogging:tagged-posts',kwargs=kwargs)
                tag_list.append(tmp)
            except:
                print(tag.name)
                print(("Unexpected error:", sys.exc_info()[0]))
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print(("Error in %s on line %d" % (fname, lineno)))
        return tag_list

    def get_author(self):
        return self.author_id
        #return self.author_id.first_name or self.author_id.username
    def get_modified_year(self):
        #print(("LAst Modified year is ", self.last_modified.year))
        return self.last_modified.year

    def get_modified_month(self):
        return self.last_modified.month
    def get_modified_day(self):
        return self.last_modified.day

    def get_modified_time(self):
        current_year = timezone.now().year
        current_day = timezone.now().day
        #print(("Printing localtime ", timezone.localtime(self.last_modified)))
        desired_time = timezone.localtime(self.last_modified)

        if(self.last_modified.year < current_year):
            return self.last_modified.strftime("%d/%m/%Y")
        elif(current_day == self.last_modified.day):
            return desired_time.strftime("%I:%M %P")
            #return self.last_modified
        else:
            return self.last_modified.strftime("%B, %d")

    def is_published(self):
        return self.published_flag

    def get_published_year(self):
        pass
    def get_published_month(self):
        pass
    def get_published_day(self):
        pass

    def get(self, member):
        if hasattr(self, member):
            #print('Get', member)
            return getattr(self, member)
        else:
            print('return None')
            return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogContent, self).save(*args, **kwargs)
        self.url_path = self.find_path(self.section)
        super(BlogContent, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_start']


def get_published_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=True,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=True).count()

def get_pending_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=False,special_flag=False,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=False,special_flag=False).count()

def get_draft_count(user = None):
    if user:
        return BlogContent.objects.filter(published_flag=False,special_flag=True,author_id=user).count()
    else:
        return BlogContent.objects.filter(published_flag=False,special_flag=True).count()

def get_contribution_count(user):
    if user:
        return BlogContent.objects.filter(author_id=user).count()
    else:
        return None
def get_top_articles(user = None, limit = 5):
    if user:
#         return BlogContent.objects.filter(author_id=user).annotate(score=Sum('vote')).order_by('score')
        return BlogContent.published.filter(author_id=user)
    else:
        return BlogContent.published.filter(author_id=user)


if use_reversion and not reversion.is_registered(BlogContent):
    reversion.register(BlogContent,fields=["title","data"])
if use_reversion and not reversion.is_registered(BlogParent):
    reversion.register(BlogParent,fields=["title","data"])