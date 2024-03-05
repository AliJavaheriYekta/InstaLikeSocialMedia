from django.contrib.auth import logout
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from auth_app.views import register, LoginView

app_name = 'auth'

urlpatterns = [
    path('register/', register),
    # path('login/', obtain_auth_token),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
]