from os.path import join

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=265, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # text = models.TextField()
    # Additional fields
    caption = models.TextField(blank=True)  # Optional longer description
    likes_count = models.PositiveIntegerField(default=0)  # Track likes
    comments_count = models.PositiveIntegerField(default=0)  # Track comments

    # Add methods to update like count
    def update_like_count(self):
        likes = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
        ).count()
        self.likes_count = likes
        # self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call parent save


def media_upload_path(instance, filename):
    return join(
        instance.content_type.app_labeled_name.split('|')[1].strip(),
        str(instance.object_id),
        filename)


class Media(BaseModel):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video')
    )
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name='object',
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=media_upload_path)
    filesize = models.BigIntegerField(blank=True, null=True)  # Add filesize
    resolution = models.CharField(max_length=20, blank=True, null=True)  # Add resolution
    # caption = models.TextField(blank=True)

    def __str__(self):
        return f' {self.content_type} - {self.media_type}: {self.file.name}'

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        storage.delete(path)
        super().delete()


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)


class Story(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DurationField(null=True)  # Optional story duration
    is_visible_to_all = models.BooleanField(default=True)  # Visibility control
    views_count = models.PositiveIntegerField(default=0)  # Track story views

    class Meta:
        verbose_name_plural = 'Stories'

    def update_view_count(self):
        views = StoryView.objects.filter(
            story=self
        ).count()
        self.views_count = views

    def __str__(self):
        return str(self.id)


class StoryMedia(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)


class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    viewer = models.ForeignKey('user_profile.Profile', on_delete=models.CASCADE)


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)  # Simplified active management
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created_at', )

    def __str__(self):
        return f'{self.created_at.ctime()} // {self.user} on {self.post.title}'


class Mention(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    # Additional fields
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name='subject',
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    start_index = models.PositiveIntegerField(null=True)  # Index of mention start in contents
    end_index = models.PositiveIntegerField(null=True)  # Index of mention end in contents

    def clean(self):
        try:
            if self.user == self.content_object.user:
                raise ValidationError(
                    "You cannot mention yourself in your own post.")
            elif self.user == self.mentioned_user:
                raise ValidationError(
                    "You cannot mention yourself.")
        except:
            pass

    def __str__(self):
        return f'{self.user.username} Mentioned {self.mentioned_user.username} on {self.content_object}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name='content',
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def __str__(self):
        return f'{self.user.username} Liked {self.content_object}'


