'''
Created on 28-May-2016

@author: Anshul Thakur
'''

from django.db import models
from django.contrib.contenttypes.models import ContentType

class BaseContentClass(models.Model):
    
    @classmethod
    def get_content_type(cls):
        class_type = ContentType.objects.get_for_model(cls, for_concrete_model=True)
        return class_type.id
     
    class Meta:
        abstract = True