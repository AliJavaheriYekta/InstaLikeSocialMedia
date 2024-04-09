from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.serializers import LoginSerializer


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
