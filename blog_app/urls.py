from django.urls import path
from django.contrib.auth import views as auth_views #Django's built-in views
from . import views

urlpatterns = [
    # Custom Registration and Profile views
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.profile_edit, name='profile_edit'),
    

    # Built-in Login View
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Custom Logout View with explicit redirect
    path('logout/', views.custom_logout, name='logout'),
]
