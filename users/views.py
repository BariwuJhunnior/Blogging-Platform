from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()

  permission_classes = [permissions.AllowAny]
  serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
  serializer_class = UserProfileSerializer
  # This ensures only logged-in users can access this endpoint
  permission_classes = [IsAuthenticated]

  # Override get_object to ensure users can only access their OWN profile
  def get_object(self):
    # The request.user is automatically set by the TokenAuthentication 
    # middleware if the user is logged in.
    return self.request.user
  