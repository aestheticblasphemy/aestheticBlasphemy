from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import json
from django.db.models import Q
from mptt.forms import TreeNodeChoiceField

from aestheticBlasphemy.forms import TagField
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""

class DefaultblogForm(forms.ModelForm):
    content =  forms.CharField(widget = CKEditorUploadingWidget(config_name='author',
                                                                attrs={'row': 20,
                                                                       'cols': 25}))
    title = forms.CharField(max_length = 100,
                            widget=forms.TextInput(attrs={  'placeholder': 'Title of post',
                                                            'class':"form-control",}),
                            required= True)
    tags = TagField()
    section = TreeNodeChoiceField(queryset=BlogParent.objects.all(),
                                  required=True,
                                  empty_label=None,
                                  label = "Select Section",
                                  widget=forms.Select(attrs={'class': "form-control"}))
    pid_count = forms.IntegerField(required=False,
                                   widget=forms.HiddenInput(attrs={'class': 'hidden-xs-up'}))
    def __init__(self,action, *args, data=None, initial=None, instance=None, **kwargs):
        initial = {} if initial is None else initial
        if data is not None:
            data['data'] = ''
        if instance is not None:
            initial['content'] = json.loads(instance.data).get('content', None)

        super(DefaultblogForm, self).__init__(*args, instance=instance, initial=initial, data=data, **kwargs)

        self.action = action
        self.order_fields(['title', 'section', 'content', 'pid_count', 'tags'])


    def save(self,post,commit=False):
        post.pop('section')
        post.pop('tags')
        post.pop('title')
        post.pop('csrfmiddlewaretoken')
        post.pop('submit')

        if commit == False:
            return json.dumps(post.dict())

        for k,v in post.items():
            if str(k) != 'pid_count' :
                tmp = {}
                tmp = tag_lib.insert_tag_id(str(v),self.cleaned_data["pid_count"])
                post[k] = tmp['content']
                post['pid_count'] = tmp['pid_count']

        return json.dumps(post.dict())

    class Meta:
        model = BlogContent
        fields = ['title', 'tags', 'section', 'content', 'pid_count']