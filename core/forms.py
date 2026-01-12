from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import VolunteerApplication


class SignUpForm(UserCreationForm):
    """Регистрация пользователя (используем стандартную модель User)."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ("motivation",)
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 4, "placeholder": "Почему вы хотите стать волонтёром?"}),
        }


class AdminExportForm(forms.Form):
    """
    Экспорт XLSX:
    1) выбрать модель
    2) выбрать поля (колонки) для выгрузки
       (по умолчанию — все доступные колонки)
    """
    model = forms.ChoiceField(
        label="Таблица (модель)",
        required=True,
        choices=[],  # заполняется в admin.py
    )

    fields = forms.MultipleChoiceField(
        label="Поля для выгрузки",
        required=False,  # пусто = выгрузить всё
        widget=forms.CheckboxSelectMultiple,
        choices=[],  # заполняется в admin.py после выбора модели
    )
