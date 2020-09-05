'''
Created on 09-Jun-2016

@author: craft
'''

from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        PrimaryKeyRelatedField, CharField,
                                        DateTimeField,
                                        EmailField, URLField)
from comments.models import Comment
from django.contrib.auth.models import User

from django.conf import settings
from blogging.models import BlogContent

class CommentSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields = ('id', 'post',
                  'body', 
                  'author', 'author_name', 'author_email', 'author_url', 
                  'date_created', 'date_modified', 
                  'parent_comment', 'published')
        
    def create(self, validated_data):
        """
        Create and return a new 'Comment' instance, given the validated data
        This is like the form class's save method.
        
        Serializers have a save method, which will in turn invoke these 
        functions
        """
        print("CommentSerializer: In Create")
        comment = Comment()
        
        comment.author = validated_data.get('author', None)

        if comment.author is None:
            comment.author_name = validated_data.get('author_name', None)
            comment.author_email = validated_data.get('author_email', None)
            comment.author_url = validated_data.get('author_url', None)
            
            if comment.author_name is None and comment.author_email is None:
                return None 
        
        comment.body = validated_data.get('body')
        comment.post = validated_data.get('post')
        comment.published = False
        if comment.author is not None and settings.COMMENT_MODERATION_ENABLED is not True:
            comment.published = True
        elif comment.author is not None and comment.author.is_staff:
            comment.published = True 

        comment.save()
        return comment
    
    def update(self, instance, validated_data):
        """
        Update and return an existing 'Comment' instance, given the 
        validated data
        """
        print("CommentSerializer: In Update")
        instance.body = validated_data.get('body', instance.body)
        instance.author = validated_data.get('author', instance.author)
        instance.parent_comment = validated_data.get('parent_comment',
                                                     instance.parent_comment)
        instance.post = validated_data.get('post')
        instance.save()
        return instance
