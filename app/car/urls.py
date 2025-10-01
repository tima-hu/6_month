from rest_framework.routers import DefaultRouter
from app.car.views import CarViewSetAPI

router = DefaultRouter()
router.register('car', CarViewSetAPI, basename='car')

urlpatterns = [
    
]

urlpatterns += router.urls

