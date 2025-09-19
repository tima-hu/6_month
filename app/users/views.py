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