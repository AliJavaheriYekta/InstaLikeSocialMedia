from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response

from user_profile.models import Follow
from user_profile.serializers import FollowSerializer


# Create your views here.
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication
    # http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        try:
            following_user = User.objects.get(pk=self.request.data['following'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID for following.")
        if following_user.username == self.request.user.username:
            raise serializers.ValidationError("Self following is not allowed!")
        try:
            serializer.save(follower=self.request.user, following=following_user)
        except IntegrityError:
            raise serializers.ValidationError(detail="You've already followed this user!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Filter the queryset based on user context (e.g., following list)
        user = self.request.user
        return Follow.objects.filter(follower=user)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if instance.follower != request.user:
            return Response({'detail': 'You cannot unfollow for other users'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


