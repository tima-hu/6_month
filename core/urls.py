from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app.users.views import FacebookLoginAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/", include("app.users.urls")),
    path("api/v1/car/", include("app.car.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/github/", include("allauth.socialaccount.urls")),
    path("accounts/", include("allauth.urls")), 
    path("auth/social/", include("allauth.socialaccount.urls")),
    path('api/auth/facebook/', FacebookLoginAPIView.as_view(), name='facebook-login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
