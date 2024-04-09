from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # content_type = models.ForeignKey(
    #     'contenttypes.ContentType', on_delete=models.CASCADE, null=True)
    # object_id = models.PositiveIntegerField(null=True)
    # content_object = GenericForeignKey("content_type", "object_id")
    content = models.TextField()  # Store textual contents
    # Additional fields for multimedia
    media_file = models.FileField(upload_to='direct_messages/', blank=True, null=True)
    media_type = models.CharField(max_length=255, blank=True, null=True)  # Optional: store media type

    # Message status
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
