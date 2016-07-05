'''
Created on 04-Jun-2016

@author: craft
'''
from django import forms
from taggit.models import Tag

class TagField(forms.ModelMultipleChoiceField):
    search_fields = ['name__icontains', ]
    def get_model_field_values(self, value):
        return {'name': value}
    
    def __init__(self):
        super(forms.ModelMultipleChoiceField, self).__init__(
                                                    queryset=Tag.objects.all(),
                                                    required=False,
                                                    widget=forms.CheckboxSelectMultiple,)
