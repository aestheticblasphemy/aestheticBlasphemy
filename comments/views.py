from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import (HTTP_200_OK,HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT)
from comments.models import Comment
from rest.serializers import CommentSerializer

from forms import CommentForm

import traceback, sys
# Create your views here.
class JSONResponse(HttpResponse):
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def comment_list(request, postID=None):
    """
    List all comments on the post
    """
    if request.method == 'GET':
        if postID is not None:
            comments = Comment.objects.filter(post_id=postID).order_by('date_created')
        else:
            comments = Comment.objects.all().order_by('date_created')
        serializer = CommentSerializer(comments, many=True)
        return JSONResponse(serializer.data)


def comment_post(request):
    """
    Make a new comment
    """
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            postID = int(data.get('post', None))
            
            if postID is None:
                print 'postID not found'
                return JSONResponse(CommentSerializer.data, 
                                                        status=HTTP_400_BAD_REQUEST)
            
            if request.user.is_authenticated():
                print 'User is authenticated'
                data[u'author'] =  str(request.user.id).encode('utf-8')
            else:
                data[u'author'] = None

            serializer = CommentSerializer(data=data)
            
            print serializer
            
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=HTTP_200_OK)

            print 'Invalid data'
            print serializer.errors
            
            return JSONResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except:
            print 'Some exception occurred.'
            print "Unexpected error:", sys.exc_info()[0]
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print "Error in %s on line %d" % (fname, lineno)
            return JSONResponse(serializer.data, status=HTTP_400_BAD_REQUEST)
    
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
def comment_form(request, postID):
    print 'Fetch form'
    
    if len(postID) is 0:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        try:
            post = Comment.objects.get(pk=int(postID))
            comment = CommentForm(initial={'post': post})
            return(Response(data={'request':request,
                                  'comment':comment},
                            template_name="comments/form.html"))
        except Comment.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)