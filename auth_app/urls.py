from django.contrib.auth import logout
from django.urls import path, include

from auth_app.views import register, LoginView, GoogleLoginView, UserRedirectView, SocialAuthGoogleURLRedirectView

app_name = 'auth'

urlpatterns = [
    path('register/', register),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/google/login/', SocialAuthGoogleURLRedirectView.as_view(), name='google-login-redirect'),
    path('accounts/registration/', include('dj_rest_auth.registration.urls')),
    path("rest-auth/google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    # path('login/', obtain_auth_token),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
]