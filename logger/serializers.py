from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import UserViewLog


class ViewLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.CharField(source='content_type.app_label')
    content_type_model = serializers.CharField(source='content_type.model', read_only=True)
    mentioned_username = serializers.CharField(source='mentioned_user.username', read_only=True)

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
            viewlog = UserViewLog.objects.create(content_type=content_type,
                                                 object_id=object_id,
                                                 **validated_data)
        except Exception as e:  # Catch generic exception for broader error handling
            raise ValidationError({'non_field_errors': str(e)})

        return viewlog

    class Meta:
        model = UserViewLog
        fields = '__all__'
