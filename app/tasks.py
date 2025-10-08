import time
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from app.car.models import Car
import asyncio
from bot import send_car_notification

logger = get_task_logger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_email_task(self, to_email: str, subject: str, body: str):
    try:
        time.sleep(4)
        result = {"status": "sent", "to": to_email, "subject": subject}
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task
def create_car_advertisement(data):
    car = Car.objects.create(**data)
    if getattr(car, "vin", None):  # если у Car есть поле vin
        check_vin_task.delay(car.id)
    generate_preview_task.delay(car.id)
    send_notification_task.delay(car.id)
    return car.id


@shared_task
def check_vin_task(car_id):
    time.sleep(3)  # эмуляция долгой операции
    car = Car.objects.get(id=car_id)
    car.is_vin_valid = True
    car.save()
    return f"VIN для {car_id} проверен"


@shared_task
def generate_preview_task(car_id):
    time.sleep(5)  # эмуляция долгого рендера
    car = Car.objects.get(id=car_id)
    car.has_preview = True
    car.save()
    return f"Превью для {car_id} сгенерировано"


@shared_task
def send_notification_task(car_id):
    car = Car.objects.get(id=car_id)
    if getattr(car, "owner_email", None):
        send_mail(
            subject="Ваше объявление создано!",
            message=f"Объявление '{car.title}' успешно создано!",
            from_email="noreply@carsite.com",
            recipient_list=[car.owner_email],
            fail_silently=True,
        )
    return f"Уведомление отправлено владельцу {car_id}"


@shared_task
def send_car_notification_task(car_data):
    asyncio.run(send_car_notification(car_data))