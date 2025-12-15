from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User

# Create your views here.
class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()

  permission_classes = [permissions.AllowAny]
  serializer_class = UserRegistrationSerializer
