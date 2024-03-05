from django.urls import include, path
from .apis import router

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
