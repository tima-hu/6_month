from rest_framework.routers import DefaultRouter
from django.urls import path

from app.users.views import UserAPIList, UserRegisterAPI, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register("list-user", UserAPIList, basename='list')
router.register("register-user", UserRegisterAPI, basename='register')

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name='token'),
    path("refresh/", TokenRefreshView.as_view(), name='refresh')
]

urlpatterns += router.urls