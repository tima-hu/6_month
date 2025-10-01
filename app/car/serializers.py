from rest_framework import serializers
from app.car.models import Car


class CarSerializer(serializers.ModelSerializer):
    delay = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Отложить выполнение в секундах"
    )

    class Meta:
        model = Car
        fields = "__all__"
