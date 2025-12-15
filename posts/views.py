from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

# Create your views here.
#View for listing all posts and creating new posts
class PostListCreateView(generics.ListCreateAPIView):
  queryset = Post.objects.all().order_by('-created_at') #Oder by newest first
  serializer_class = PostSerializer
  #Allow any user to view the list of posts
  permission_classes = [permissions.AllowAny]

#View for retrieving a single post (Read) and updating/deleting 
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  #Allow any user to view the details of a post
  permission_classes = [permissions.AllowAny]