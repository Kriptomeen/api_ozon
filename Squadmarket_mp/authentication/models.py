from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    inn = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.username

class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
    ozon_client_id = models.CharField(max_length=100, blank=True, null=True)
    ozon_api_key = models.CharField(max_length=100, blank=True, null=True)
    wildberries_client_id = models.CharField(max_length=100, blank=True, null=True)
    wildberries_api_key = models.CharField(max_length=100, blank=True, null=True)
    yandex_client_id = models.CharField(max_length=100, blank=True, null=True)
    yandex_api_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Настройки пользователя {self.user.username}"
