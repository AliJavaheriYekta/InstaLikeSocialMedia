from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Comment, Like


@receiver(post_save, sender=Comment)
def update_comment_count_on_create(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comments_count += 1
        post.save()


@receiver(post_delete, sender=Comment)
def update_comment_count_on_delete(sender, instance, **kwargs):
    post = instance.post
    post.comments_count -= 1
    post.save()


@receiver(post_save, sender=Like)
def update_like_count_on_create(sender, instance, created, **kwargs):
    if created:
        post = instance.content_object  # Access the associated Post object
        post.update_like_count()
        post.save()


@receiver(post_delete, sender=Like)
def update_like_count_on_delete(sender, instance, **kwargs):
    post = instance.content_object  # Access the associated Post object
    post.update_like_count()
    post.save()


def register_signals():
    # Connect signal handlers here
    update_comment_count_on_create.connect(sender=Comment)
    update_comment_count_on_delete.connect(sender=Comment)
