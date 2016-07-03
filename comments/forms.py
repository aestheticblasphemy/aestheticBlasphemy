'''
Created on 25-Jun-2016

@author: craft
'''
from django import forms
from models import Comment
from blogging.models import BlogContent

class CommentForm(forms.ModelForm):
    
    body = forms.Textarea()
    
    def __init__(self, *args, **kwargs):
        
        super(CommentForm, self).__init__(*args, **kwargs)
        
        if kwargs.get('initial', None) is not None:
            self.fields['parent_comment'].queryset = Comment.objects.filter(post= kwargs['initial']['post'])
            self.fields['post'].queryset = BlogContent.objects.filter(pk= kwargs['initial']['post'].id)
    class Meta:
        model = Comment
        exclude = ('published', 'date_created', 'date_modified', 'author')