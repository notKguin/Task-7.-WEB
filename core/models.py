from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Абстрактная базовая модель с общими полями created_at/updated_at."""

    created_at = models.DateTimeField("Создано", default=timezone.now, editable=False)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True


class Event(TimeStampedModel):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    location = models.CharField("Локация", max_length=255)
    starts_at = models.DateTimeField("Начало")
    ends_at = models.DateTimeField("Окончание")

    class Meta:
        ordering = ("-starts_at",)

    def __str__(self) -> str:
        return self.title


class VolunteerApplication(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "На рассмотрении"
        APPROVED = "APPROVED", "Одобрено"
        REJECTED = "REJECTED", "Отклонено"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="applications")
    motivation = models.TextField("Мотивация")
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.PENDING)

    class Meta:
        unique_together = ("user", "event")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user} -> {self.event}"


class Like(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "event")

    def __str__(self) -> str:
        return f"{self.user} ❤ {self.event}"
