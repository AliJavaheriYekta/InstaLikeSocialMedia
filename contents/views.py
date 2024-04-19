from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import *

from .models import Post, Comment, Story, Media, StoryView, Mention
from .serializers import PostSerializer, CommentSerializer, StorySerializer, MediaSerializer, StoryViewSerializer, \
    MentionSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        post_pk = self.kwargs['pk']
        post_user = Post.objects.get(pk=self.kwargs['pk']).user
        if (not post_user.profile.is_private) or (post_user.id in user.followings.all().values_list('following', flat=True)):
            serializer = self.get_serializer(Post.objects.get(pk=post_pk))
            return Response(serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Post.objects.filter(user__in=user.followings.all().values_list('following', flat=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # Handle case where no story_pk is provided (optional)
        # return Response({'error': 'Missing story ID in URL'})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if request.user.username == instance.user.username:
            self.perform_destroy(instance)
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(data='You are not allowed to remove other\'s post!', status=HTTP_401_UNAUTHORIZED)

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if request.user.username == instance.user.username:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)
        else:
            return Response(data='You are not allowed to modify other\'s post!', status=HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None, *args, **kwargs):
        # For full updates using PUT requests
        instance = self.get_object()
        if request.user.username == instance.user.username:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(data='You are not allowed to modify other\'s post!', status=HTTP_401_UNAUTHORIZED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        post_pk = self.kwargs['pk']
        story_user = Story.objects.get(pk=self.kwargs['pk']).user
        if (not story_user.profile.is_private) or (story_user.id in user.followings.all().values_list('following', flat=True)):
            serializer = self.get_serializer(Story.objects.get(pk=post_pk))
            return Response(serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

        # queryset = re

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Story.objects.filter(user__in=user.followings.all().values_list('following', flat=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, pk=None, *args, **kwargs):
        media = self.get_object()
        invalid_update = False
        for key, _ in request.data.items():
            if key != 'view_count':
                invalid_update = True
                break

        serializer = self.get_serializer(media, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if invalid_update:
            warning = {'WARN': 'Only view_count is updatable!'}
            return Response(serializer.data | warning)
        else:
            return Response(serializer.data)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def destroy(self, request, pk=None, *args, **kwargs):
        media = self.get_object()
        serializer = MediaSerializer(media, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        try:
            serializer.undo_create_actions(media)  # Call the undo function
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Handle any errors during undo or deletion
            return Response(e.args[0], status=status.HTTP_403_FORBIDDEN)


class BaseStoryViewViewSet(viewsets.ModelViewSet):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializer


class StoryViewViewSet(BaseStoryViewViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListStoryViewSet(BaseStoryViewViewSet):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializer
    http_method_names = ['get', ]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, story_pk=None, *args, **kwargs):
        # Override list method to filter by story ID
        if story_pk:
            queryset = self.get_queryset().filter(story=story_pk)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Handle case where no story_pk is provided (optional)
            return Response({'error': 'Missing story ID in URL'})


class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

