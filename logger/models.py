from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.authtoken.admin import User


class UserViewLog(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    viewed_at = models.DateTimeField(auto_now_add=True)
