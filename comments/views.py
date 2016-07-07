from django.http import HttpResponse

from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import (HTTP_200_OK,HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)
from comments.models import Comment
from rest.serializers import CommentSerializer

from forms import CommentForm

import traceback, sys
from blogging.models import BlogContent

from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.db.models import Q
from django.conf import settings

# Create your views here.
class JSONResponse(HttpResponse):
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CommentList(GenericAPIView):
    """
    List all comments on the post
    """
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all().order_by('-date_created')
    page_size_query_param = 'size'
    
    max_page_size = 1000
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get(self, request, postID=None, format=None):
        if postID is not None:
            if request.user.is_authenticated() and request.user.is_staff:
                print 'Staff'
                self.queryset = Comment.objects.filter(post_id=postID).order_by('parent_comment','-date_created')
            elif request.user.is_authenticated():
                print 'User'
                self.queryset = Comment.objects.filter(post_id=postID).order_by('parent_comment','-date_created')
                self.queryset = self.queryset.filter(published=True)|self.queryset.filter(author=self.user)
            else:
                print 'Guest'
                self.queryset = Comment.objects.filter(post_id=postID).order_by('parent_comment','-date_created')
                self.queryset = self.queryset.filter(published=True)
        else:
            self.queryset = Comment.objects.all().order_by('-date_created')

        self.paginator.page_size_query_param = self.page_size_query_param

        comments = self.paginate_queryset(self.queryset)

        if comments is not None:
            serializer = self.get_serializer(comments, many=True)
            return JSONResponse(OrderedDict([
                                            ('count', self.paginator.page.paginator.count),
                                            ('next', self.paginator.get_next_link()),
                                            ('previous', self.paginator.get_previous_link()),
                                            ('results', serializer.data)
                                        ]))
        
        serializer = self.get_serializer(self.queryset, many=True)
        return JSONResponse(serializer.data)

def comment_list(request, postID=None):
    if request.method=='GET':
        if postID is not None:
            comments = Comment.objects.filter(post_id=postID).order_by('-date_created')
        else:
            comments = Comment.objects.all().order_by('-date_created')

        paginator = Paginator(comments, 50,orphans=30)
        page = request.GET.get('page')
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pages = paginator.page(paginator.num_pages)
        actions = [{"name":"Approve", "help":"Approve selected comments"},
                   {"name":"Unpublish", "help":"Approve selected comments"},
                   {"name":"Delete", "help":"Delete selected comments"},
                   ]
        context = {"comments": pages, "actions": actions
                   }
        
        template = loader.get_template('comments/manage.html')
        return HttpResponse(template.render(context, request))

class CommentPost(viewsets.ModelViewSet):
    """
    Make a new comment
    """
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        if self.request.user is not None and self.request.user.is_staff:
            published = True
            serializer.save(author=self.request.user, published=published)
        elif self.request.user is not None and self.request.user.is_authenticated() and settings.COMMENT_MODERATION_ENABLED is not True:
            print 'User'
            published = True 
            serializer.save(author=self.request.user, published=published)
        else:
            print 'Guest'
            published = False
            serializer.save(published=published)
        


def comment_detail(request, cid):
    try:
        comment = Comment.objects.get(pk=cid)
    except Comment.DoesNotExist:
        return HttpResponse(status=HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JSONResponse(serializer.data)
    
    elif request.method== 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        comment.delete()
        return HttpResponse(status = HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer,))
def comment_form(request, postID, commentID=0):
    print 'commentForm', postID, commentID
    if len(postID) is 0:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        try:
            post = BlogContent.objects.get(pk=int(postID))
            if commentID is not None:
                parent_comment = Comment.objects.get(pk=int(commentID))
                comment = CommentForm(initial={'post': post,
                                               'parent_comment': parent_comment})
            else:
                comment = CommentForm(initial={'post': post,})

            return(Response(data={'request':request,
                                  'comment':comment,
                                  'path': post.get_absolute_url()},
                            template_name="comments/form.html"))
        except Comment.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        except:
            print 'Some exception occurred.'
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            return Response(status=HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
def comment_approve(request):
    if request.method=='POST':
        try:
            data = JSONParser().parse(request)
            
            action = data.get('action')
            pks = data.get("selection")
            comment_ids =[]
            for pk in pks:
                comment_ids.append(int(pk))
            
            print action
            if len(comment_ids):
                objs = Comment.objects.filter(pk__in=comment_ids)

                if action == u'Approve':
                    print "LOGS: Promote the given comments"
                    for obj in objs:
                        obj.published = True
                        obj.save()
                elif action == u'Unpublish':
                    print "LOGS: Unpublish the given comments"
                    for obj in objs:
                        obj.published = False
                        obj.save()
                elif action == u'Delete':
                    print "LOGS: Delete the given comments"
                    for obj in objs:
                        obj.delete()
                else:
                    print "LOGS: Nothing"
                    return JSONResponse(pks, status=HTTP_400_BAD_REQUEST)
            return JSONResponse(pks, status=HTTP_200_OK)
        
        except:
            print 'Some exception occurred.'
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            return JSONResponse(None, status=HTTP_400_BAD_REQUEST)
