from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email address', unique=True)
    username = models.CharField(max_length=250, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
