from rest_framework import routers
from contents import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'stories', views.StoryViewSet)
