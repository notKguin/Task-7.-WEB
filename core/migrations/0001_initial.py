from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("location", models.CharField(max_length=255, verbose_name="Локация")),
                ("starts_at", models.DateTimeField(verbose_name="Начало")),
                ("ends_at", models.DateTimeField(verbose_name="Окончание")),
            ],
            options={"ordering": ("-starts_at",)},
        ),
        migrations.CreateModel(
            name="VolunteerApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("motivation", models.TextField(verbose_name="Мотивация")),
                ("status", models.CharField(choices=[("PENDING", "На рассмотрении"), ("APPROVED", "Одобрено"), ("REJECTED", "Отклонено")], default="PENDING", max_length=16, verbose_name="Статус")),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="core.event")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",), "unique_together": {("user", "event")}},
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="core.event")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "event")}},
        ),
    ]
