from django.urls import path
from .views import (
  PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, LikePostView, RatePostView, TopPostsView, PostShareView, SubscribeCategoryView, UserFeedView, GlobalFeedView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
  #GET (List) and POST (Create)
  path('posts/', PostListCreateView.as_view(), name='post-list-create'),
  #GET (Retrieve), PUT/PATCH (Update), DELETE(Destroy)
  path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

  #Comments
  path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create' ),
  path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

  #Engagements (Likes/Ratings)
  path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
  path('posts/<int:pk>/rate/', RatePostView.as_view(), name='post-rate'),
  path('posts/top/', TopPostsView.as_view(), name='top-posts'),
  path('posts/<int:pk>/share/', PostShareView.as_view(), name='post-share'),

  #Category
  path('categories/<int:category_id>/subscribe/', SubscribeCategoryView.as_view(), name='category-subscribe'),

  #Feed
  path('feed/', UserFeedView.as_view(), name='user-feed'),
  path('explore/', GlobalFeedView.as_view(), name='global-feed'),


  #Documentation
  path('schema/', SpectacularAPIView.as_view(), name='schema'),
  path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
  path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
  path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
