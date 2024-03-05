from rest_framework import serializers
from .models import Follow, Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'  # Include all profile fields (adjust as needed)


class FollowSerializer(serializers.ModelSerializer):
    following = ProfileSerializer(source='following.profile', read_only=True)  # Nested serializer

    class Meta:
        model = Follow
        fields = ('id', 'following')  # Adjust fields as needed
