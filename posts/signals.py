from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Rating, Post
from .tasks import send_rating_notification_email, notify_subscribers

@receiver(post_save, sender=Rating)
def notify_author_of_five_star(sender, instance, created, **kwargs):
  #Only notify if the score is 5
  if instance.score == 5 and instance.post.status == Post.Status.PUBLISHED:
    post = instance.post

    if post.author.email:
      #Execute synchronously for development (remove .delay() to avoid Celery dependency)
      send_rating_notification_email(  # type: ignore
        post.author.email,
        post.author.username,
        post.title
      )


@receiver(post_save, sender=Post)
def notify_subscribers_on_publish(sender, instance, created, **kwargs):
  if created and instance.status == Post.Status.PUBLISHED:
    #Execute synchronously for development (remove .delay() to avoid Celery dependency)
    notify_subscribers(instance.id)  # type: ignore
