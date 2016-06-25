'''
Created on 25-Jun-2016

@author: craft
'''
from django import forms
from models import Comment

class CommentForm(forms.ModelForm):
    
    body = forms.Textarea()
    class Meta:
        model = Comment
        exclude = ('published', 'date_created', 'date_modified', 'author')