from rest_framework.routers import DefaultRouter
from django.urls import path

from app.users.views import UserAPIList, UserRegisterAPI, MyTokenObtainPairView, SendEmailView, TaskStatusApiView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import FacebookLoginAPIView

router = DefaultRouter()
router.register("list-user", UserAPIList, basename='list')
router.register("register-user", UserRegisterAPI, basename='register')

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name='token'),
    path("refresh/", TokenRefreshView.as_view(), name='refresh'),
    path('send_email', SendEmailView.as_view(), name='email'),
    path('tasks/<str:task_id>/', TaskStatusApiView.as_view(), name='tasks'),
]

urlpatterns += router.urls