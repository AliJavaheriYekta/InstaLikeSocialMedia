from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .models import UserViewLog
from .serializers import ViewLogSerializer


class UserViewLogViewSet(viewsets.ModelViewSet):
    queryset = UserViewLog.objects.all()
    serializer_class = ViewLogSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id and self.request.user.is_staff:
            return queryset.filter(user_id=user_id)
        else:
            return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Override get_queryset to filter by user if requested in GET parameters