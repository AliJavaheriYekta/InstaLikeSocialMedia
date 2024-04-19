from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from SocialMedia.local_settings import GOOGLE_CALLBACK_URL
from auth_app.serializers import LoginSerializer

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from SocialMedia.settings import SOCIALACCOUNT_PROVIDERS as social_providers


# from SocialMedia.local_settings import ADMIN_PATH


# Create your views here.
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is not None and password is not None:
        try:
            User.objects.get(username=username)
            return Response({'error': 'User already registered!'})
        except User.DoesNotExist:
            user = User.objects.create_user(username, password=password)
            if user:
                return Response({'success': 'User registered!'})
            # token = Token.objects.create(user=user)
            # return Response({'token': token.key})
            else:
                return Response({'error': 'An error occurred during user registration!'})
    else:
        return Response({'error': 'Username and password are required'})


# @api_view(['POST'])
# def logins(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     if username is not None and password is not None:
#         user = User.objects.get(username=username)
#         if user:
#             token = Token.objects.get(user__=user)
#             if token:
#                 token.delete()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'User with this credential does not exist!'})
#     else:
#         return Response({'error': 'Username and password are required'})


# @csrf_exempt
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URL
    client_class = OAuth2Client


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


class SocialAuthGoogleURLRedirectView(APIView):
    # pattern_name = 'google-login-redirect'
    def get(self, request, *args, **kwargs):
        params = social_providers['google']
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' \
              'redirect_uri={GOOGLE_CALLBACK_URL}&prompt=consent&response_type=code&' \
              'client_id={CLIENT_ID}&scope=openid%20email%20profile&access_type={ACCESS_TYPE}'\
            .format(GOOGLE_CALLBACK_URL=GOOGLE_CALLBACK_URL,
                    CLIENT_ID=params.get('CLIENT_ID'),
                    ACCESS_TYPE=params.get('AUTH_PARAMS').get('access_type'))

        return HttpResponseRedirect(url)
