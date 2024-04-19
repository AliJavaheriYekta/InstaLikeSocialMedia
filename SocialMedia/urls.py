"""
URL configuration for SocialMedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from SocialMedia import settings, local_settings
from SocialMedia.local_settings import ADMIN_PATH

urlpatterns = [
    path(f'{ADMIN_PATH}/', admin.site.urls),
    path('', include("auth_app.urls")),
    # path("accounts/", include("allauth.urls")),  # most important
    path('content/', include("contents.urls")),
    path('profile/', include("user_profile.urls")),
    path('direct/', include("directs.urls")),
    path('logger/', include("logger.urls"))
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(local_settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
