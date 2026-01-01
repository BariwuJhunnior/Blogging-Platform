from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

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
  followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['follower', 'followed_user'], name='unique_followers')
    ]