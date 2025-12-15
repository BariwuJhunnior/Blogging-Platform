from django.urls import path
from .views import PostListCreateView, PostDetailView

urlpatterns = [
  #GET (List) and POST (Create)
  path('', PostListCreateView.as_view(), name='post-list-create'),
  #GET (Retrieve), PUT/PATCH (Update), DELETE(Destroy)
  path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
