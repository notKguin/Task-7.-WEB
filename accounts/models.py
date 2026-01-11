from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь (нужно для потенциального расширения под роли).

    В данной работе роли решаются стандартно:
    - гость: неавторизован
    - пользователь: is_authenticated = True
    - администратор: is_staff (и/или is_superuser)
    """

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email
