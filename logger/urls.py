from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewLogViewSet

router = DefaultRouter()
router.register(r'logs', UserViewLogViewSet, basename='logs')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
