'''
Created on 25-Jun-2016

@author: craft
'''
from django import forms
from models import Comment
from blogging.models import BlogContent

from django.contrib.auth.models import User

class CommentForm(forms.Form):
    
    post = forms.ModelChoiceField(queryset=BlogContent.published.all())
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 40,
    													 'rows': 4,
    													 'class':"form-control",
    													 'placeholder':'Enter your comment here...'}),
    											  required=True)

    author_name = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control",
    														    'placeholder':'Name'}), required=False)
    author_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control",
    														 	   'placeholder':'e-mail'}), required=False)
    author_url = forms.URLField(widget=forms.URLInput(attrs={'class':"form-control",
    														 'placeholder':'www.'}), 
    														 required=False)
    
    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):        
        super(CommentForm, self).__init__(*args, **kwargs)
        
        if kwargs.get('initial', None) is not None:
            self.fields['parent_comment'].queryset = Comment.objects.filter(post= kwargs['initial']['post'])
            self.fields['post'].queryset = BlogContent.objects.filter(pk= kwargs['initial']['post'].id)
         