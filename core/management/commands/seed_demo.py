from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from core.models import Event

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт демо‑данные: admin/user и пару мероприятий."

    def handle(self, *args, **options):
        admin_email = "admin@example.com"
        user_email = "user@example.com"

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                username="admin",
                password="admin123",
            )
            self.stdout.write(self.style.SUCCESS("Created admin@example.com / admin123"))

        if not User.objects.filter(email=user_email).exists():
            User.objects.create_user(
                email=user_email,
                username="user",
                password="user123",
            )
            self.stdout.write(self.style.SUCCESS("Created user@example.com / user123"))

        if Event.objects.count() == 0:
            now = timezone.now()
            Event.objects.create(
                title="Сбор гуманитарной помощи",
                description="Нужны волонтёры для сортировки и упаковки вещей.",
                location="Amsterdam",
                starts_at=now + timezone.timedelta(days=3),
                ends_at=now + timezone.timedelta(days=3, hours=3),
            )
            Event.objects.create(
                title="Забег благотворительности",
                description="Помощь на маршруте, регистрация участников, выдача воды.",
                location="Rotterdam",
                starts_at=now + timezone.timedelta(days=7),
                ends_at=now + timezone.timedelta(days=7, hours=5),
            )
            self.stdout.write(self.style.SUCCESS("Created demo events"))
