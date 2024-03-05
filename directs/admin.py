from django.contrib import admin

from directs.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'get_content_type', 'get_content_preview', 'is_read', 'created_at')
    list_filter = ('sender', 'receiver', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')

    def get_content_type(self, obj):
        return obj.content_type.app_label  # Extract content type app name

    def get_content_preview(self, obj):
        if obj.content_type.model_class() == Message:  # Check for text message
            return obj.content[:20]  # Display the first 20 characters
        else:
            return f"Media content: {obj.media_type}"  # Indicate media type for non-text messages

    get_content_preview.short_description = 'Content Preview'


admin.site.register(Message, MessageAdmin)
