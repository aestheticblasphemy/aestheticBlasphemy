from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
import json
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""

class DefaultblogForm(forms.Form):
    content =  forms.CharField(widget = CKEditorUploadingWidget(config_name='author'))
    title = forms.CharField(max_length = 100)
    tags = TagField()
    section = TreeNodeChoiceField(queryset=BlogParent.objects.all(),required=True,empty_label=None, label = "Select Section" )
    pid_count = forms.IntegerField(required=False)
    def __init__(self,action, *args, **kwargs):
        self.helper = FormHelper()
        
        self.helper.form_id = 'id-DefaultblogForm'
#        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
#         self.helper.form_action = reverse('blogging:create-post')
        self.helper.form_action = action
        self.helper.layout = Layout(
                Fieldset(
                'Create Content of Type DefaultBlog',
                'tags',
                'title',
                Field('pid_count', type="hidden"),
                'section',
                'content',
            ),
            
            ButtonHolder(
                Submit('submit', 'Publish', css_class='button blue'),
                Submit('submit', 'Save Draft', css_class='button white')
            ),
            
            )
        super(DefaultblogForm, self).__init__(*args, **kwargs)
        
        self['tags'].label_tag(attrs={'class': 'checkbox-inline'})        
        self.order_fields(['title', 'section', 'content', 'pid_count', 'tags'])

    
    def save(self,post,commit=False):
        post.pop('section')
        post.pop('tags')
        post.pop('title')
        post.pop('csrfmiddlewaretoken')
        post.pop('submit')

        if commit == False:
            return json.dumps(post.dict())
        
        for k,v in post.iteritems():
            if str(k) != 'pid_count' :
                tmp = {}
                tmp = tag_lib.insert_tag_id(v,self.cleaned_data["pid_count"])
                post[k] = tmp['content']
                post['pid_count'] = tmp['pid_count']
            
        return json.dumps(post.dict())
        
