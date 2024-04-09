from rest_framework import routers
from contents import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'stories', views.StoryViewSet, basename='stories')
router.register(r'stories/(?P<story_pk>\d+)/views', views.ListStoryViewSet, basename='story-views')
router.register(r'storyviews', views.StoryViewViewSet)
router.register(r'medias', views.MediaViewSet)
router.register(r'mentions', views.MentionViewSet)
