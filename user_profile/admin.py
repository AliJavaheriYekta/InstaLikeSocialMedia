from django.contrib import admin
from .models import Profile, Follow


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'is_private')  # Customize displayed fields
    list_filter = ('is_private',)  # Filter by private status
    search_fields = ('user__username', 'user__first_name', 'user__last_name')  # Search by user fields

    def get_full_name(self, obj):
        return obj.user.get_full_name()  # Example custom method for full name


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')  # Customize displayed fields
    search_fields = ('follower__username', 'following__username')  # Search by user fields

    def get_full_name(self, obj):
        return obj.user.get_full_name()


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
