'''
Created on 07-Jun-2015

@author: craft
'''
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        PrimaryKeyRelatedField, CharField,
                                        DateTimeField,
                                        EmailField, URLField)

from blogging.models import BlogContent
from django.contrib.auth.models import User
from django.conf import settings
from dashboard.models import UserProfile
from comments.models import Comment

class UserSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, 
                                                 queryset=Comment.objects.all())
    gravatar = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 
                  'gravatar', 'url', 'comments', 'is_admin')
        
    def get_gravatar(self, obj):
        print("in get_gravatar")
        print(obj)
        return UserProfile.objects.get(user=obj).get_avatar_url()
    
    def get_url(self, obj):
        return UserProfile.objects.get(user=obj).get_profile_page()
    
    def get_is_admin(self, obj):
        return obj.is_staff
        


class AnonymousUserSerializer(serializers.Serializer):
    username = serializers.CharField();

class BlogContentSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, 
                                                 queryset=Comment.objects.all())
    class Meta:
        model = BlogContent
        fields =('id', 'title', 'create_date', 'data', 'url_path', 
                 'author_id', 'published_flag', 'section',
                 'comments',)
     

class CommentSerializer(ModelSerializer):
    post_url = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    def get_post_url(self, obj):
        return obj.post.get_absolute_url()

    class Meta:
        model=Comment
        fields = ('id', 'post',
                  'body', 
                  'author', 'author_name', 'author_email', 'author_url', 
                  'date_created', 'date_modified', 
                  'parent_comment', 'published', 'post_url')
        
    def create(self, validated_data):
        """
        Create and return a new 'Comment' instance, given the validated data
        This is like the form class's save method.
        
        Serializers have a save method, which will in turn invoke these 
        functions
        """
        
        print('In create')
        
        comment = Comment()
        
        comment.author = validated_data.get('author')
        
        if comment.author == None:
            comment.author_name = validated_data.get('author_name', None)
            comment.author_email = validated_data.get('author_email', None)
            comment.author_url = validated_data.get('author_url', None)
            
            if comment.author_name == None and comment.author_email == None:
                return None 
        
        comment.body = validated_data.get('body')
        
        comment.post = validated_data.get('post')
        comment.published = False
        if comment.author != None and settings.COMMENT_MODERATION_ENABLED != True:
            comment.published = True
        elif comment.author != None and comment.author.is_staff:
            comment.published = True
        
        comment.parent_comment = validated_data.get('parent_comment', None)
        print(comment.parent_comment)

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
