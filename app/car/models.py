from django.db import models
from app.users.models import User

CARABKA_TRANSFER = (
    ("Автомат", "Автомат"),
    ("Механика", "Механика"),
    ("Эдекторкар", "Эдекторкар"),
)

TYPE_CAR = (
    ("Седан", "Седан"),
    ("Универсал", "Универсал"),
    ("Грузовой", "Грузовой"),
)


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    
    brand = models.CharField(max_length=155, verbose_name='Бранд')
    model = models.CharField(max_length=155, verbose_name='Модел')
    number = models.CharField(max_length=50, verbose_name='Номер машины')
    probeg = models.CharField(max_length=155, verbose_name='Пробег')
    
    carabka_transfer = models.CharField(
        max_length=155,
        verbose_name='Коробка передач',
        choices=CARABKA_TRANSFER,
        default=None
    )
    
    type_car = models.CharField(
        max_length=155,
        verbose_name='Тип',
        choices=TYPE_CAR,
        default=None
    )
    
    date = models.CharField(max_length=100, verbose_name='Год выпуска')

    vin = models.CharField(max_length=50, blank=True, null=True, verbose_name='VIN')
    is_vin_valid = models.BooleanField(default=False, verbose_name='VIN проверен')
    has_preview = models.BooleanField(default=False, verbose_name='Есть превью')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок объявления')
    owner_email = models.EmailField(blank=True, null=True, verbose_name='Email владельца')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.date})"

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
