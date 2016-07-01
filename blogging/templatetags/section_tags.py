'''
Created on 01-July-2016

@author: craft
'''
from __future__ import unicode_literals

from django import template

from blogging.models import BlogParent

register = template.Library()

@register.inclusion_tag('blogging/section_index.html', takes_context=True)
def section_tree(context):
    sections = BlogParent.objects.all()

    print "Template Tag: Sections"
    
    return {'sections':sections,
            'request': context['request']}