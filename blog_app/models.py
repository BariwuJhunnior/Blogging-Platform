from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200)
  content = models.TextField()
  published_date = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    ordering = ['-published_date']

  def __str__(self):
    return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'


