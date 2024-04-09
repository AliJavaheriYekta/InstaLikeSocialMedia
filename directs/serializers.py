from rest_framework import serializers
from rest_framework.authtoken.admin import User

from directs.models import Message
from user_profile.models import Follow


class MessageReceiveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'created_at',
            'content',
            'media_file',
            'media_type']


class MessageSendSerializers(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none())

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'created_at',
            'content',
            'media_file',
            'media_type'
        ]
        read_only_fields = ['sender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = self.get_queryset()

    def get_queryset(self):
        user = self.context['request'].user
        followings = Follow.objects.filter(follower=user)
        following_users = User.objects.filter(
            username__in=[following.following.username for following in followings])
        return following_users

    def create(self, validated_data):
        # Assign the sender to the current authenticated user
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
