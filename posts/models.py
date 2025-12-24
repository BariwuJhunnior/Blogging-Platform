from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name
  

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name

class Post(models.Model):
  #Required Fields
  title = models.CharField(max_length=255)
  content = models.TextField()

  #Relationships 
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  tags = models.ManyToManyField(Tag, blank=True)

  #Date Fields
  published_date = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title


class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.author} on {self.post}"
  

class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
    ]
  
class Rating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
  score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  class Meta:
    constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_rating')]