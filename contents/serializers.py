from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import StringRelatedField

from user_profile.models import Profile
from .models import Post, Comment, Media, Story, Mention, Like, PostMedia, StoryMedia, StoryView


class MediaSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.app_label')

    # object_id = serializers.IntegerField(source='object_id')

    def create(self, validated_data):
        # Extract content_type and object_id from validated data
        content_type_app_label = validated_data.pop('content_type')
        object_id = validated_data.pop('object_id')

        try:
            content_type = ContentType.objects.get(
                app_label=content_type_app_label['app_label'].split('|')[0].strip().lower(),
                model=content_type_app_label['app_label'].split('|')[1].strip().lower()
            )
        except ContentType.DoesNotExist:
            raise ValidationError({'content_type': 'Invalid content type provided.'})
        # Create the media object with remaining data and related object
        try:
            media = Media.objects.create(content_type=content_type, object_id=object_id, **validated_data)
        except Exception as e:  # Catch generic exception for broader error handling
            raise ValidationError({'non_field_errors': str(e)})

        related_object = content_type.get_object_for_this_type(pk=media.object_id)
        content_type_model = related_object._meta.object_name
        if content_type_model == 'Post':
            PostMedia.objects.create(post=related_object, media=media)
        elif content_type_model == 'Story':
            StoryMedia.objects.create(story=related_object, media=media)
        return media

    def undo_create_actions(self, media):
        """Undoes the actions taken in the create() method."""
        related_object = media.content_type.get_object_for_this_type(pk=media.object_id)
        content_type_model = related_object._meta.object_name

        # Delete associated model instances
        if content_type_model == 'Post':
            PostMedia.objects.filter(media_id=media.id).delete()
        elif content_type_model == 'Story':
            StoryMedia.objects.filter(media_id=media.id).delete()

        # Delete the media object itself
        media.delete()

    class Meta:
        model = Media
        fields = ('id', 'content_type', 'object_id', 'media_type', 'file', 'filesize', 'resolution')


class MentionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.CharField(source='content_type.app_label')
    content_type_model = serializers.CharField(source='content_type.model', read_only=True)
    mentioned_username = serializers.CharField(source='mentioned_user.username', read_only=True)

    def create(self, validated_data):
        # Extract content_type and object_id from validated data
        content_type_app_label = validated_data.pop('content_type')
        object_id = validated_data.pop('object_id')
        mentioned_user = validated_data.pop('mentioned_user')

        try:
            content_type = ContentType.objects.get(
                app_label=content_type_app_label['app_label'].split('|')[0].strip().lower(),
                model=content_type_app_label['app_label'].split('|')[1].strip().lower()
            )
        except ContentType.DoesNotExist:
            raise ValidationError({'content_type': 'Invalid content type provided.'})
        # Create the media object with remaining data and related object
        try:
            mention = Mention.objects.create(user=self.context['request'].user,
                                             mentioned_user=mentioned_user,
                                             content_type=content_type,
                                             object_id=object_id, **validated_data)
        except Exception as e:  # Catch generic exception for broader error handling
            raise ValidationError({'non_field_errors': str(e)})

        return mention

    class Meta:
        model = Mention
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    mentions = MentionSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    # likes = LikeSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    # media = MediaSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Story
        fields = '__all__'
        # read_only_fields = ('user', 'duration', 'is_visible_to_all')


class StoryViewSerializer(serializers.ModelSerializer):
    story = serializers.SlugRelatedField(slug_field='id', queryset=Story.objects.all())
    viewer = serializers.SlugRelatedField(slug_field='user_id', queryset=Profile.objects.all())

    def get_viewer_username(self, obj):
        return obj.user.username  # Access username from related User object

    class Meta:
        model = StoryView
        fields = '__all__'  # You can also specify a list of fields to include


class StoryDetailSerializer(serializers.ModelSerializer):
    views = StoryViewSerializer(many=True, read_only=True)  # Nested serializer for related views

    class Meta:
        model = StoryView
        fields = '__all__'
