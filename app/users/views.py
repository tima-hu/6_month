from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.models import User
from app.users.serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer

class UserAPIList(GenericViewSet, 
                mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegisterAPI(GenericViewSet, 
                        mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class FacebookLoginAPIView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')

        # Проверка токена у Facebook
        fb_response = requests.get(
            f'https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}'
        )
        fb_data = fb_response.json()

        if 'error' in fb_data:
            return Response({'error': 'Invalid Facebook token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Создание/поиск пользователя в Django
        user, created = User.objects.get_or_create(
            username=fb_data['id'],
            defaults={'first_name': fb_data.get('name', '')}
        )

        # Генерация JWT через Simple JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
