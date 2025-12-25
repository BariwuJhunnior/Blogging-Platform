from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  bio = models.TextField(max_length=500, blank=True)
  profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
  location = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return f"{self.user.username}'s Profile"
  

class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['follower', 'author'], name='unique_followers')
    ]