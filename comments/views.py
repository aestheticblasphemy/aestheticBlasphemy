from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.status import (HTTP_200_OK,HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT)
from comments.models import Comment
from comments.serializers import CommentSerializer

# Create your views here.
class JSONResponse(HttpResponse):
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def comment_list(request, postID=None):
    """
    List all comments on the post
    """
    if request.method == 'GET':
        if postID is not None:
            comments = Comment.objects.filter(post_id=postID)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if postID is None:
            return JSONResponse(serializer.data, status=HTTP_400_BAD_REQUEST)
        data['post'] = data.get('post', postID)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=HTTP_200_OK)
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