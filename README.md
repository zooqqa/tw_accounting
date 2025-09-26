# TW Accounting System

Система учета и аналитики для управления финансами и трафиком.

## Архитектура

Система состоит из микросервисов:
- **Accounting Service** - сервис бухгалтерии (порт 8001)
- **Traffic Analytics Service** - сервис аналитики трафика (порт 8002)
- **API Gateway** - шлюз для объединения сервисов (порт 8000)
- **Frontend** - пользовательский интерфейс (порт 3000)

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd tw_accounting
```

### 2. Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 3. Доступ к сервисам

- **API Gateway**: http://localhost:8000
- **Accounting Service**: http://localhost:8001
- **Traffic Analytics Service**: http://localhost:8002
- **Frontend**: http://localhost:3000 (будет добавлен позже)

### 4. Документация API

- **API Gateway**: http://localhost:8000/docs
- **Accounting Service**: http://localhost:8001/docs
- **Traffic Analytics Service**: http://localhost:8002/docs

## Разработка

### Структура проекта

```
tw_accounting/
├── services/
│   ├── accounting/          # Сервис бухгалтерии
│   ├── traffic-analytics/   # Сервис аналитики
│   └── api-gateway/         # API шлюз
├── frontend/                # React приложение
├── shared/                  # Общие библиотеки
├── docs/                    # Документация
└── docker-compose.yml       # Docker конфигурация
```

### Технологический стек

#### Backend
- **FastAPI** - веб-фреймворк
- **SQLModel** - ORM (Pydantic + SQLAlchemy)
- **PostgreSQL + TimescaleDB** - база данных
- **Redis** - кэширование
- **FastAPI-Users** - аутентификация

#### Frontend
- **React 18 + TypeScript** - UI фреймворк
- **Vite** - сборщик
- **Tailwind CSS + Shadcn/UI** - стилизация
- **TanStack Query** - управление состоянием

## Конфигурация

### Переменные окружения

Скопируйте `config.env` файлы в соответствующие сервисы:

```bash
# Для Accounting Service
cp services/accounting/config.env services/accounting/.env

# Для Traffic Analytics Service
cp services/traffic-analytics/config.env services/traffic-analytics/.env

# Для API Gateway
cp services/api-gateway/config.env services/api-gateway/.env
```

### База данных

PostgreSQL с TimescaleDB автоматически инициализируется при первом запуске.

## API Endpoints

### Accounting Service (порт 8001)

- `GET /health` - проверка состояния
- `GET /docs` - документация API

### Traffic Analytics Service (порт 8002)

- `GET /health` - проверка состояния
- `GET /docs` - документация API

### API Gateway (порт 8000)

- `GET /health` - проверка состояния
- `GET /docs` - документация API

## Разработка

### Запуск в режиме разработки

```bash
# Запуск только базы данных и Redis
docker-compose up -d postgres redis

# Запуск Accounting Service локально
cd services/accounting
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Тестирование

```bash
# Запуск тестов
pytest

# Запуск тестов с покрытием
pytest --cov=app tests/
```

## Лицензия

MIT License
