'''
Created on 25-Jun-2016

@author: craft
'''
from __future__ import unicode_literals

from django import template

from comments.forms import CommentForm

register = template.Library()

@register.inclusion_tag('comments/form.html', takes_context=True)
def comment_form(context):
    comment = CommentForm(initial={'post': context['nodes']})
    print "Template Tag: {node}".format(node=context['nodes'].id)
    
    return {'comment':comment,
            'request': context['request']}