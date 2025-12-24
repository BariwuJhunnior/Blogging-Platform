from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Rating

@receiver(post_save, sender=Rating)
def notify_author_of_five_star(sender, instance, created, **kwargs):
  #Only send if the score is 5
  if instance.score == 5:
    post = instance.post
    author_email = post.author.email

    if author_email:
      send_mail(
        subject='Your post got a 5-star rating',
        message=f'Hi {post.author.username}, \n\n'
        f"Great news! Your post '{post.title}' just received a 5-star rating.",
        from_email='notifications@blogapi.com', 
        recipient_list=[author_email],
        fail_silently=True
      )