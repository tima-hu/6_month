from rest_framework.routers import DefaultRouter
from django.urls import path

from app.users.views import UserAPIList, UserRegisterAPI

router = DefaultRouter()
router.register("list-user", UserAPIList, basename='list')
router.register("register-user", UserRegisterAPI, basename='register')

urlpatterns = [
    
]

urlpatterns += router.urls