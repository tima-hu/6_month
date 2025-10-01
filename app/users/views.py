from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from celery.result import AsyncResult

from app.tasks import send_email_task, create_car_advertisement
from app.users.models import User
from app.users.serializers import (
    UserSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    SendEmailSerializers,
)

import requests
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPIList(GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterAPI(GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SendEmailView(APIView):
    def post(self, request):
        serializer = SendEmailSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]
        delay = serializer.validated_data.get("delay", 0)

        # Планируем задачу Celery
        if delay > 0:
            async_result = send_email_task.apply_async(
                args=[email, subject, body],
                countdown=delay
            )
        else:
            async_result = send_email_task.delay(email, subject, body)

        return Response(
            {"task_id": async_result.id, "status": async_result.status},
            status=status.HTTP_202_ACCEPTED,
        )


class TaskStatusApiView(APIView):
    def get(self, request, task_id: str):
        async_result = AsyncResult(task_id)
        data = {
            "task_id": task_id,
            "status": async_result.status,
            "ready": async_result.ready(),
            "result": async_result.result if async_result.ready() else None,
        }
        return Response(data)


class FacebookLoginAPIView(APIView):
    def post(self, request):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response(
                {"error": "Missing access_token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fb_response = requests.get(
            "https://graph.facebook.com/me",
            params={"fields": "id,name,email", "access_token": access_token},
            timeout=10,
        )
        fb_data = fb_response.json()

        if "error" in fb_data:
            return Response(
                {"error": "Invalid Facebook token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Используем кастомную модель User
        user, _ = User.objects.get_or_create(
            username=fb_data["id"],
            defaults={
                "first_name": fb_data.get("name", ""),
                "email": fb_data.get("email", ""),
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)}
        )
