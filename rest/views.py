from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status

from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView

from rest.serializers import *
from rest.utils import IsOwnerOrReadOnly, AnnotationIsOwnerOrReadOnly, VoteIsOwnerOrReadOnly, BookmarkIsOwnerOrReadOnly


@api_view(('GET',))
#If not set, the API root will assert for not having appropriate permissions.
@permission_classes((permissions.IsAuthenticatedOrReadOnly, ))
def api_root(request, format=None):
    return Response({
        'blogcontent': reverse('rest:blogcontent-list', request=request, format=format),
        'user': reverse('rest:user-list', request=request, format=format),
        'currentUser': reverse('rest:current-user', request=request, format=format),            
        })
 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        user_obj = self.request.user
        if(user_obj.id != None):
            serializer = UserSerializer(user_obj)
        else:
            serializer = AnonymousUserSerializer(user_obj)
            #print(serializer.data)
             
        return Response(serializer.data)    
        
class BlogContentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
