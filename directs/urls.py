from rest_framework import routers
from django.urls import path, include
from .views import ReceiveMessageViewSet, SendMessageViewSet

router = routers.DefaultRouter()
router.register("receive", ReceiveMessageViewSet, basename='receiveMessage')
router.register("send", SendMessageViewSet, basename='sendMessage')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
