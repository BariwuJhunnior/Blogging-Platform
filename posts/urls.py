from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
  #GET (List) and POST (Create)
  path('posts/', PostListCreateView.as_view(), name='post-list-create'),
  #GET (Retrieve), PUT/PATCH (Update), DELETE(Destroy)
  path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

  #Documentation
  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
  path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
  path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
  path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
