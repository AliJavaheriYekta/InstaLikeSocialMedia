from django.contrib import admin
from django.utils.html import mark_safe

from .forms import CommentAdminForm
from .models import Post, Media, Story, Mention, Comment, Like, PostMedia


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1  # Allow adding one extra media per post by default


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    form = CommentAdminForm
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


class PostAdmin(admin.ModelAdmin):
    inlines = [PostMediaInline, CommentInline]  # Inline display of related media
    list_display = ('id', 'user', 'caption', 'created_at', 'get_like_count')  # Customize displayed fields
    list_filter = ('user',)  # Filter by user
    readonly_fields = ('comments_count', 'likes_count')

    def get_like_count(self, obj):
        # Example method to display like count (implement logic to retrieve actual count)
        return obj.likes_count


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'get_thumbnail')  # Customize displayed fields

    def get_file_type(self, obj):
        return obj.content_type.app_label  # Extract content type app name

    def get_thumbnail(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" width="100px" height="auto" />')
        return 'No File'  # Display placeholder if no file

    readonly_fields = ('get_thumbnail',)  # Mark thumbnail field as read-only


class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_duration_display', 'is_visible_to_all', 'created_at')
    list_filter = ('user', 'is_visible_to_all')
    search_fields = ('user__username', 'content')

    def get_duration_display(self, obj):
        if obj.duration:
            # Implement logic to format the duration string (e.g., hours:minutes:seconds)
            # Replace this placeholder with your desired formatting
            return str(obj.duration)
        return 'No duration'


class MentionAdmin(admin.ModelAdmin):
    list_display = ('mentioned_user', 'object_repr', 'start_index', 'end_index')
    list_filter = ('mentioned_user',)
    search_fields = ('mentioned_user__username', 'content_type__app_label', 'content_type__model')

    def object_repr(self, obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
        try:
            # Attempt to retrieve the mentioned object
            mentioned_object = model_class.objects.get(pk=obj.object_id)
            return str(mentioned_object)
        except (model_class.DoesNotExist, PermissionError):
            return f"Object (pk={obj.content_object_id}) not found"


admin.site.register(Mention, MentionAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
