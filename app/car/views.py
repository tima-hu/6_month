from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app.car.models import Car
from app.car.serializers import CarSerializer
from app.filters import CarFilter
from app.pagination import CastumPagination
from app.tasks import create_car_advertisement


class CarViewSetAPI(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CastumPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['brand', 'model', 'number']
    ordering_fields = ['date', 'brand', 'probeg']

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        cache_key = f"user_cars_{user_id}"
        cars = cache.get(cache_key)

        if not cars:
            queryset = self.get_queryset().filter(user_id=user_id)
            serializer = self.get_serializer(queryset, many=True)
            cars = serializer.data
            cache.set(cache_key, cars, timeout=60 * 5)
        return Response(cars)

    def retrieve(self, request, *args, **kwargs):
        car_id = kwargs.get('pk')
        cache_key = f"car_{car_id}"
        car = cache.get(cache_key)

        if not car:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            car = serializer.data
            cache.set(cache_key, car, timeout=60 * 5)
        return Response(car)


class CarCreateView(APIView):
    def post(self, request):
        data = request.data.dict()
        task = create_car_advertisement.delay(data)
        return Response({"status": "processing", "task_id": task.id})
