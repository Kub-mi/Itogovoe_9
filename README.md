# Itogovoe 9

Учебный проект на Django и DRF, подготовленный для демонстрации контейнеризации и CI/CD.

## Локальный запуск через Docker Compose

1. Скопируйте файл окружения и при необходимости измените значения:

   ```bash
   cp .env.example .env
   ```

2. Соберите и запустите контейнеры:

   ```bash
   docker compose up -d --build
   ```

3. Приложение будет доступно по адресу [http://localhost](http://localhost). Эндпоинт проверки здоровья: `http://localhost/api/health/`.

4. Для остановки контейнеров выполните:

   ```bash
   docker compose down
   ```

### Доступные сервисы

- **web** — Django + Gunicorn
- **celery** — Celery worker
- **celery_beat** — планировщик периодических задач
- **db** — PostgreSQL
- **redis** — брокер и хранилище результатов для Celery, а также кэш
- **nginx** — обратный прокси, отдаёт статические файлы

## Тестирование и линтинг локально

```bash
poetry install
poetry run black --check .
poetry run isort --check-only .
poetry run flake8
poetry run pytest
```

## CI/CD (GitHub Actions)

В репозитории настроен workflow `.github/workflows/ci.yml`, который выполняет следующие шаги:

1. Установка зависимостей и запуск линтеров/тестов.
2. Сборка Docker-образов.
3. Деплой на удалённый сервер при пуше в ветку `main`.

### Переменные окружения и секреты для деплоя

В настройках репозитория GitHub необходимо добавить секреты:

- `SSH_HOST` — адрес сервера
- `SSH_PORT` — порт SSH (по умолчанию `22`)
- `SSH_USER` — пользователь для подключения
- `SSH_KEY` — приватный SSH-ключ (OpenSSH)
- `DEPLOY_PATH` — путь до директории с проектом на сервере

Скрипт деплоя ожидает, что на сервере:

- установлен Docker и Docker Compose;
- репозиторий уже клонирован и доступен по пути `DEPLOY_PATH`;
- рядом с `docker-compose.yml` лежит заполненный `.env` с боевыми значениями.

После успешного деплоя приложение поднимается командой `docker compose up -d --build`.

## Подготовка удалённого сервера

1. Установите Docker и Docker Compose (например, через официальный репозиторий Docker).
2. Создайте пользователя, добавьте его в группу `docker`.
3. Настройте SSH-доступ по ключу, добавив публичный ключ в `~/.ssh/authorized_keys` на сервере.
4. Клонируйте репозиторий в директорию, указанную в `DEPLOY_PATH`.
5. Создайте файл `.env` на сервере на основе `.env.example` и заполните боевыми значениями.
6. Выполните первый запуск: `docker compose up -d --build`.

## Ручной деплой

При необходимости можно обновить проект вручную:

```bash
ssh user@host
cd /path/to/project
git pull origin main
docker compose up -d --build
docker compose run --rm web python manage.py migrate
```

## Полезные команды

- Просмотр логов Django: `docker compose logs -f web`
- Просмотр логов Celery: `docker compose logs -f celery`
- Создание суперпользователя: `docker compose run --rm web python manage.py createsuperuser`
