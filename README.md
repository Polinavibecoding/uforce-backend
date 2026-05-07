# Uforce Case Console — Backend

Бэкенд для консоли кейсов маркетингового агентства Uforce. Позволяет тимлидам заполнять кейсы голосом или текстом, GPT обрабатывает и причёсывает ответы, после чего кейс публикуется и автоматически попадает в Google Sheets.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0 + aiosqlite** — асинхронная ORM и БД
- **OpenAI GPT-4o** — обработка и форматирование ответов, генерация описаний
- **Google Sheets API** — синхронизация данных
- **Pydantic** — валидация данных

## Быстрый старт

### 1. Установка зависимостей

```bash
cd uforce_cases_backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
```

Отредактируй `.env`:
- `OPENAI_API_KEY` — ключ от OpenAI
- `GOOGLE_SHEETS_CREDENTIALS_PATH` — путь к service account JSON
- `GOOGLE_SHEETS_SPREADSHEET_ID` — ID таблицы

### 3. Google Sheets Credentials

1. Перейди в [Google Cloud Console](https://console.cloud.google.com/)
2. Создай Service Account
3. Сгенерируй JSON ключ и сохрани как `credentials.json`
4. Дай доступ Service Account на редактирование таблицы (share по email)

### 4. Инициализация БД и заполнение тестовыми данными

```bash
python seed_data.py
```

### 5. Запуск

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

## API Endpoints

### Тимлиды
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/teamleads/` | Список тимлидов |
| GET | `/teamleads/{id}` | Тимлид по ID |
| POST | `/teamleads/` | Создать тимлида |
| PATCH | `/teamleads/{id}` | Обновить тимлида |
| DELETE | `/teamleads/{id}` | Деактивировать тимлида |

### Кейсы
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/cases/` | Список кейсов |
| GET | `/cases/{id}` | Кейс по ID |
| POST | `/cases/start` | Начать создание кейса |
| POST | `/cases/{id}/answer` | Ответить на вопрос (текст) |
| POST | `/cases/{id}/voice-answer` | Ответить на вопрос (голос/текст) |
| GET | `/cases/{id}/draft` | Получить черновик |
| POST | `/cases/{id}/edit` | Редактировать поле вручную |
| POST | `/cases/{id}/generate-descriptions` | Сгенерировать описания для скриптов |
| POST | `/cases/{id}/publish` | Опубликовать кейс |
| POST | `/cases/{id}/archive` | Архивировать кейс |
| GET | `/cases/marketing/notifications` | Уведомления для маркетинга |

### Шаблоны описаний
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/templates/` | Список шаблонов |
| POST | `/templates/` | Создать шаблон |
| PATCH | `/templates/{id}` | Обновить шаблон |
| DELETE | `/templates/{id}` | Деактивировать шаблон |

## Поток заполнения кейса

```
1. POST /cases/start
   → Создаётся черновик, возвращается первый вопрос

2. POST /cases/{id}/voice-answer (или /answer)
   → Тимлид отвечает голосом/текстом
   → GPT обрабатывает и форматирует
   → Возвращается следующий вопрос

3. Повторять шаг 2 пока не закончатся вопросы

4. GET /cases/{id}/draft
   → Показывается полный черновик

5. POST /cases/{id}/edit (опционально)
   → Ручная корректировка полей

6. POST /cases/{id}/generate-descriptions
   → Автогенерация описаний для скриптов

7. POST /cases/{id}/publish
   → Кейс публикуется
   → Автоматически записывается в Google Sheets
   → Генерируется уведомление для маркетинга
```

## Структура проекта

```
uforce_cases_backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── core/
│   │   ├── config.py        # Настройки
│   │   └── security.py      # Безопасность
│   ├── db/
│   │   └── database.py      # Подключение к БД
│   ├── models/
│   │   └── models.py        # SQLAlchemy модели
│   ├── schemas/
│   │   └── schemas.py       # Pydantic схемы
│   ├── services/
│   │   ├── openai_service.py   # GPT интеграция
│   │   └── google_sheets.py    # Google Sheets API
│   └── routers/
│       ├── teamleads.py     # CRUD тимлидов
│       ├── cases.py         # CRUD кейсов
│       └── templates.py     # CRUD шаблонов
├── seed_data.py             # Начальные данные
├── requirements.txt
├── .env.example
└── README.md
```

## Поля кейса

| Поле | Описание |
|------|----------|
| `client_name` | Название бренда (внутреннее) |
| `product_description` | Описание продукта / ниши |
| `nda_status` | NDA: с брендом / обезличено / нет |
| `geo` | Страна/регион |
| `target_audience` | Целевая аудитория |
| `period` | Период работ |
| `goal` | Цель сотрудничества |
| `tools_channels` | Ключевые инструменты / каналы |
| `team_actions` | Что делала команда uforce |
| `metrics` | Метрики |
| `results` | Результаты |
| `insights` | Комментарий / инсайты для маркетинга |
| `date_added` | Дата добавления (авто) |
| `medium_description` | Среднее описание для скриптов (авто) |
| `short_description` | Супер короткое описание (авто) |

## Лицензия

Внутренний проект Uforce.
