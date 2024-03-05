from os.path import join

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=265, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
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
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call parent save


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)  # Simplified active management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created_at', )

    def __str__(self):
        return f'{self.created_at.ctime()} // {self.user} on {self.post.title}'


def media_upload_path(instance, filename):
    return join('post', instance.post.title, filename)


class Media(BaseModel):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video')
    )
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=media_upload_path)
    filesize = models.BigIntegerField(blank=True, null=True)  # Add filesize
    resolution = models.CharField(max_length=20, blank=True, null=True)  # Add resolution
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'{self.post.title} - {self.media_type}: {self.file.name}'


class Story(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # Additional fields
    duration = models.DurationField(null=True)  # Optional story duration
    is_visible_to_all = models.BooleanField(default=True)  # Visibility control
    views_count = models.PositiveIntegerField(default=0)  # Track story views


class Mention(BaseModel):
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    # Additional fields
    content_object = models.ForeignKey(
        ContentType,  # Use contents type model for generic relations
        on_delete=models.CASCADE,
        related_name='mentions')
    start_index = models.PositiveIntegerField()  # Index of mention start in contents
    end_index = models.PositiveIntegerField()  # Index of mention end in contents


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")
