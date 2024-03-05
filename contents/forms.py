from django import forms

from contents.models import Comment


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'content', 'is_active']