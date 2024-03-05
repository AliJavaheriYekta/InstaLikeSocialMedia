from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, serializers

from user_profile.models import Follow
from user_profile.serializers import FollowSerializer


# Create your views here.
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def perform_create(self, serializer):
        try:
            following_user = User.objects.get(pk=self.request.data['following'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID for following.")
        serializer.save(follower=self.request.user, following=following_user)

    def get_queryset(self):
        # Filter the queryset based on user context (e.g., following list)
        user = self.request.user
        return Follow.objects.filter(follower=user)
