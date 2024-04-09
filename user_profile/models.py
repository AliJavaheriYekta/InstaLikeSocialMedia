# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Common profile fields
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    # Avatar picture
    avatar = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    # Privacy status
    is_private = models.BooleanField(default=False)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Enforce unique follower-following pair

        constraints = [
            models.CheckConstraint(
                check=~Q(follower=F('following')),  # Validate follower and following are different
                name='cannot_follow_self'
            )
        ]