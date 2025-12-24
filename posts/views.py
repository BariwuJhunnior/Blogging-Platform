from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, inline_serializer
from rest_framework import generics
from rest_framework import serializers

#A simple serializer for one-off messages
MessageSerializer = inline_serializer(
  name='MessageResponse',
  fields={
    'message': serializers.CharField()
  }
)

#View for listing all posts and creating new posts
#API documentation with drf-spectacular
@extend_schema_view(
  list=extend_schema(
    summary='List all posts.',
    responses={
      201: PostSerializer, #Succesful Creation
      400: OpenApiResponse(description='Bad Request - Invalid data provided.'),
      401: OpenApiResponse(description='Unauthorized - Token is missing or invalid'),
    },
    description='Retrieve a list of blog posts with support for search and category filtering',
    tags=['Public Feed']
  ),
  create=extend_schema(
    summary='Create a blog post.',
    description='Authorized users can create posts. Author is set automatically.',
    tags=['Author Actions']
  ),
)
class PostListCreateView(generics.ListCreateAPIView):
  queryset = Post.objects.all().order_by('-created_at') #Order by newest first
  serializer_class = PostSerializer
  filterset_class = PostFilter

  filter_backends = [
    DjangoFilterBackend,
    filters.SearchFilter
  ]

  search_fields = ['title', 'content', 'author__username', 'tags__name']
  
  #Only Authenticated users can CREATE posts
  def get_permissions(self):
    if self.request.method == 'POST':
      #Require authentication for the POST (Creation)
      return [IsAuthenticated()]
    #Allow anyone to view the list (GET)
    return [permissions.AllowAny()]
  
  def perform_create(self, serializer):
    #Called right before post object is saved, sets the author to the logged-in User
    serializer.save(author=self.request.user)


@extend_schema_view(
  update=extend_schema(
    summary='Update a post',
    responses={
      200: PostSerializer,
      403: OpenApiResponse(
        description='Forbidden - You are not the author of this post',
        response=MessageSerializer
      ),
      404: OpenApiResponse(description='Not Found - Post ID does not exits')
    }
  ),
  destroy=extend_schema(
    summary='Delete a post',
    responses={
      204: OpenApiResponse(description='No Content - Successfully deleted'),
      403: OpenApiResponse(description='Forbidden - Only authors can delete.')
    }
  )
)
#View for retrieving a single post (Read) and updating/deleting 
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all().order_by('-created_at') #Order by newest first
  serializer_class = PostSerializer
  
  # 1. User must be logged in (IsAuthenticated) to attempt modification.
  # 2. They must pass the custom check (IsAuthorOrReadOnly).
  permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

@extend_schema_view(
  list=extend_schema(summary='List comments for a post', tags=['Comments']),
  create=extend_schema(summary='Add a comment to a post', tags=['Comments']),
)
class CommentListCreateView(generics.ListCreateAPIView):
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get_queryset(self):
    #Only return comments for the post specified in the URL
    return Comment.objects.filter(post_id=self.kwargs['post_pk']).order_by('-created_at')
  
  def perform_create(self, serializer):
    # Automatically assign author and post
    post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
    serializer.save(author=self.request.user, post=post)

@extend_schema_view(
  update=extend_schema(summary='Edit a comment', tags=['Comments']),
  destroy=extend_schema(summary='Delete a comment', tags=['Comments']),
)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all().order_by('-created_at')
  serializer_class = CommentSerializer
  permission_classes = [IsAuthorOrReadOnly] #Reusing our custom permissions