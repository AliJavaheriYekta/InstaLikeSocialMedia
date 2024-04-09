from rest_framework import permissions
from rest_framework import viewsets

from .models import Message
from .serializers import MessageReceiveSerializers, MessageSendSerializers


class ReceiveMessageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageReceiveSerializers

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)


class SendMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSendSerializers

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)
