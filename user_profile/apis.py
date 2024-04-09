import http

from rest_framework.routers import DefaultRouter

from user_profile.views import FollowViewSet

router = DefaultRouter()
router.register(r'follows', FollowViewSet)

# , basename='follows'