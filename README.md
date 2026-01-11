# VolunteerEvents (Django + PostgreSQL + Docker)

Учебное веб‑приложение по предметной области **«Заявка на мероприятие в роли волонтёра»**.

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

## Запуск без Docker
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Экспорт XLSX
Доступен только staff‑пользователям:
- страница: `/admin-tools/export/`
- можно выбрать модель (таблицу) и нужные поля, получить `.xlsx`

## REST API
- `/api/events/` (GET/POST для staff)
- `/api/events/<id>/` (GET/PUT/PATCH/DELETE для staff)
- `/api/applications/` (GET/POST авторизованным)
- `/api/likes/` (GET/POST авторизованным)

## Требование “3+ коммита”
Пример последовательности:
```bash
git init
git add .
git commit -m "Initial Django project with Docker and DB schema"

# ... доделали страницы/авторизацию
git commit -am "Add auth, events UI and volunteer applications"

# ... доделали export + API
git commit -am "Add XLSX export tool and REST API"

git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```
