from django.contrib import admin
from .models import UserViewLog


class ViewLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'viewed_at',)
    list_filter = ('user', 'content_type', 'viewed_at')
    search_fields = ('user__username', 'content_type__name', 'object_id')


admin.site.register(UserViewLog, ViewLogAdmin)
