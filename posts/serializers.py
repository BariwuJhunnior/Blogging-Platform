from rest_framework import serializers
from .models import Post, Category, Tag, Comment

class PostSerializer(serializers.ModelSerializer):
  # Use StringRelatedField to show the author's username instead of their ID
  author = serializers.ReadOnlyField(source='author.username')
  # Use SlugRelatedField to show category name, and make it required
  category_name = serializers.SlugRelatedField(
    source='category', # Link to the 'category' field in the Post model
    slug_field='name',
    queryset = Category.objects.all(), # Used for validation in POST/PUT
  )

  # Tags are optional, allow reading/writing names
  tags = serializers.SlugRelatedField(
    many=True,
    slug_field='name', 
    queryset=Tag.objects.all(),
    required=False, #Tages are optional requirement
  )

  likes_count = serializers.IntegerField(read_only=True)
  avg_rating = serializers.FloatField(read_only=True)

  class Meta:
    model = Post
    fields = ['id', 'title', 'content', 'author', 'category_name', 'published_date', 'created_at', 'tags', 'likes_count', 'avg_rating']
    
    read_only_fields = ('author', 'created_at') #These are set by the server, not the user


class CommentSerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source='post.id')

  class Meta:
    model = Comment
    fields = ['id', 'post', 'author', 'content', 'created_at']
