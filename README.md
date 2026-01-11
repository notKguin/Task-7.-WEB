# VolunteerEvents (Django + PostgreSQL + Docker)

Веб‑приложение по предметной области **«Заявка на мероприятие в роли волонтёра»**.

## Функционал
- PostgreSQL БД с 4 связанными таблицами: `accounts_user`, `core_event`, `core_volunteerapplication`, `core_like`
- Общие поля `created_at` / `updated_at` вынесены в абстрактную модель `TimeStampedModel`
- Регистрация/авторизация (гость/пользователь/админ)
- Основная услуга: подача заявки волонтёра на мероприятие
- Доп. функционал: поиск/фильтрация/сортировка + собственный REST API (DRF)
- Админ‑панель: Django admin + отдельная страница экспорта XLSX с выбором таблицы и полей

## Запуск в Docker
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
```

Открыть: http://localhost:8000/

Демо‑аккаунты (создаются командой `seed_demo`):
- admin: `admin@example.com` / `admin123` (доступ к /admin/ и экспорту)
- user: `user@example.com` / `user123`

## Экспорт XLSX
Доступен только staff‑пользователям:
- страница: `/admin-tools/export/`
- можно выбрать модель (таблицу) и нужные поля, получить `.xlsx`

## REST API
- `/api/events/` (GET/POST для staff)
- `/api/events/<id>/` (GET/PUT/PATCH/DELETE для staff)
- `/api/applications/` (GET/POST авторизованным)
- `/api/likes/` (GET/POST авторизованным)
