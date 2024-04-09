from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import Comment, Like, StoryView


@receiver(pre_delete, sender=Like)
def update_comment_count_on_like_deletion(sender, instance, **kwargs):
    content_object = instance.content_object
    try:
        if content_object.likes_count > 0:
            content_object.likes_count -= 1
            content_object.save()
    except:
        print('some error in content like deletion!')


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


@receiver(post_save, sender=StoryView)
def update_view_count_on_create(sender, instance, created, **kwargs):
    if created:
        story = instance.story  # Access the associated Post object
        story.update_view_count()
        story.save()


def register_signals():
    # Connect signal handlers here
    update_comment_count_on_create.connect(sender=Comment)
    update_comment_count_on_delete.connect(sender=Comment)
