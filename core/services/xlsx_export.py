from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Type

from django.apps import apps
from django.db.models import Model
from openpyxl import Workbook


@dataclass(frozen=True)
class ExportModelMeta:
    label: str
    model: Type[Model]
    fields: List[str]


class ExportService:
    """Сервис экспорта XLSX с выбором модели и полей.

    Принцип: на UI выбираем "таблицу" и список полей -> формируем XLSX.
    """

    MODEL_MAP = {
        "users": ("Пользователи", "accounts", "User", ["id", "email", "username", "is_staff", "is_active", "date_joined"]),
        "events": ("Мероприятия", "core", "Event", ["id", "title", "location", "starts_at", "ends_at", "created_at", "updated_at"]),
        "applications": ("Заявки", "core", "VolunteerApplication", ["id", "user_id", "event_id", "status", "created_at", "updated_at"]),
        "likes": ("Лайки", "core", "Like", ["id", "user_id", "event_id", "created_at", "updated_at"]),
    }

    def get_models(self) -> Dict[str, Dict[str, Any]]:
        models: Dict[str, Dict[str, Any]] = {}
        for key, (label, app_label, model_name, fields) in self.MODEL_MAP.items():
            models[key] = {"label": label, "fields": fields}
        return models

    def build_xlsx(self, model_key: str, fields: List[str]) -> Tuple[bytes, str]:
        if model_key not in self.MODEL_MAP:
            raise ValueError("Неизвестная таблица для экспорта.")

        label, app_label, model_name, default_fields = self.MODEL_MAP[model_key]
        model = apps.get_model(app_label=app_label, model_name=model_name)
        if model is None:
            raise ValueError("Модель для экспорта не найдена.")

        if not fields:
            fields = default_fields

        # Разрешаем только whitelisted поля
        allowed = set(default_fields)
        fields = [f for f in fields if f in allowed]
        if not fields:
            raise ValueError("Не выбрано ни одного допустимого поля.")

        qs = model.objects.all().values(*fields)

        wb = Workbook()
        ws = wb.active
        ws.title = "Report"

        ws.append(fields)
        for row in qs:
            ws.append([row.get(f) for f in fields])

        out = io.BytesIO()
        wb.save(out)
        out.seek(0)

        filename = f"report_{model_key}.xlsx"
        return out.read(), filename
