# TW Accounting - Система учета и аналитики

Современная микросервисная система для ведения бухгалтерского учета с поддержкой криптовалют и веб-аналитики.

## 🏗️ Архитектура

Система состоит из следующих компонентов:

### Backend Services
- **Accounting Service** (порт 8001) - Основной сервис бухгалтерии
- **API Gateway** (порт 8000) - Шлюз для маршрутизации запросов
- **Traffic Analytics Service** (порт 8002) - Сервис веб-аналитики
- **PostgreSQL + TimescaleDB** (порт 5432) - База данных с поддержкой временных рядов
- **Redis** (порт 6379) - Кэширование и очереди

### Frontend
- **React Application** (порт 3000) - Современный веб-интерфейс

## 🚀 Быстрый старт

### Требования
- Docker & Docker Compose
- Node.js 18+ (для frontend разработки)
- Git

### Запуск системы

1. **Клонирование репозитория:**
```bash
git clone https://github.com/zooqqa/tw_accounting.git
cd tw_accounting
```

2. **Запуск backend сервисов:**
```bash
docker compose up -d
```

3. **Запуск frontend (для разработки):**
```bash
cd frontend
npm install
npm run dev
```

### Проверка работы

- **Backend API:** http://localhost:8001/docs
- **Frontend:** http://localhost:3000
- **Health check:** http://localhost:8001/health

## 🔐 Демо-доступ

Для тестирования системы используйте:
- **Email:** `test@example.com`
- **Пароль:** `testpassword123`

## 📋 Функционал

### ✅ Реализовано

#### Инфраструктура
- ✅ Docker контейнеризация всех сервисов
- ✅ PostgreSQL с TimescaleDB для временных рядов
- ✅ Redis для кэширования и очередей
- ✅ API Gateway для маршрутизации

#### Аутентификация и безопасность
- ✅ JWT токены для аутентификации
- ✅ Регистрация и управление пользователями
- ✅ Хэширование паролей с Argon2
- ✅ Защищенные API endpoints

#### Основная бухгалтерия
- ✅ Управление счетами (банковские, наличные, крипто, инвестиционные)
- ✅ Система проектов с статусами и датами
- ✅ Категории доходов/расходов с иерархией
- ✅ Справочник контрагентов
- ✅ CRUD операции для всех справочников

#### Система транзакций
- ✅ **Принцип двойной записи** - каждая транзакция балансируется
- ✅ Автоматическое обновление балансов счетов
- ✅ Типы операций: доходы, расходы, переводы
- ✅ Сложные транзакции с множественными проводками
- ✅ Отслеживание статусов транзакций

#### Поддержка криптовалют
- ✅ Поддержка TRX и USDT (TRC20)
- ✅ Автоматическая конвертация курсов через CoinGecko API
- ✅ Валидация TRON адресов кошельков
- ✅ Интеграция с TronScan API для проверки транзакций
- ✅ Хранение метаданных крипто-операций

#### Frontend интерфейс
- ✅ Modern React + TypeScript + Vite
- ✅ Адаптивный дизайн с Tailwind CSS
- ✅ Система аутентификации с Zustand
- ✅ Главная панель с виджетами и статистикой
- ✅ Защищенные маршруты
- ✅ API интеграция с React Query

### 🔄 В процессе разработки
- Детальные страницы управления справочниками
- Интерфейсы создания и редактирования транзакций
- Формы для крипто-операций

### 📋 Планируется
- Система счетов на оплату (Invoice)
- Отчеты и аналитика
- Экспорт данных
- Уведомления и интеграции

## 🛠️ Технологический стек

### Backend
- **FastAPI** - Современный веб-фреймворк для Python
- **SQLModel** - ORM с поддержкой Pydantic и SQLAlchemy
- **PostgreSQL + TimescaleDB** - Реляционная БД с поддержкой временных рядов
- **Redis** - Кэширование и очереди задач
- **Pydantic** - Валидация данных
- **Alembic** - Миграции базы данных
- **Docker** - Контейнеризация

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - Типизированный JavaScript
- **Vite** - Быстрый сборщик и dev сервер
- **Tailwind CSS** - Utility-first CSS фреймворк
- **React Query** - Управление состоянием сервера
- **Zustand** - Легковесное управление состоянием
- **React Router** - Клиентская маршрутизация
- **Axios** - HTTP клиент

### DevOps
- **Docker Compose** - Оркестрация контейнеров
- **Git** - Контроль версий
- **GitHub** - Хостинг кода

## 📊 API Endpoints

### Аутентификация
- `POST /api/auth/login` - Вход в систему
- `POST /api/auth/register` - Регистрация
- `GET /api/auth/me` - Профиль пользователя

### Справочники
- `GET/POST/PATCH/DELETE /api/accounts/` - Управление счетами
- `GET/POST/PATCH/DELETE /api/projects/` - Управление проектами  
- `GET/POST/PATCH/DELETE /api/categories/` - Управление категориями
- `GET/POST/PATCH/DELETE /api/counterparties/` - Управление контрагентами

### Транзакции
- `GET /api/transactions/` - Список транзакций
- `POST /api/transactions/income` - Создать доход
- `POST /api/transactions/expense` - Создать расход
- `POST /api/transactions/transfer` - Создать перевод
- `GET /api/transactions/{id}/entries` - Проводки транзакции

### Криптовалюты
- `GET /api/crypto/rates` - Текущие курсы
- `POST /api/crypto/income` - Крипто-доход
- `POST /api/crypto/expense` - Крипто-расход
- `GET /api/crypto/supported-currencies` - Поддерживаемые валюты
- `GET /api/crypto/wallet-validation/{address}` - Валидация адреса

## 🧪 Тестирование

Система полностью протестирована:
- ✅ Все API endpoints
- ✅ Принципы двойной записи
- ✅ Крипто-функционал с реальными курсами
- ✅ Аутентификация и авторизация
- ✅ Валидация данных

## 📁 Структура проекта

```
tw_accounting/
├── docs/                           # Документация
│   ├── architecture.md            # Архитектура системы
│   ├── plan.md                    # План разработки
│   └── rules&requirements.md      # Требования и правила
├── services/                      # Backend микросервисы
│   ├── accounting/                # Основной сервис бухгалтерии
│   │   ├── app/
│   │   │   ├── api/              # API роуты
│   │   │   ├── core/             # Конфигурация и безопасность
│   │   │   ├── models/           # SQLModel модели
│   │   │   ├── services/         # Бизнес-логика
│   │   │   └── main.py           # Точка входа FastAPI
│   │   ├── alembic/              # Миграции БД
│   │   └── requirements.txt      # Python зависимости
│   ├── api-gateway/              # API Gateway
│   └── traffic-analytics/        # Веб-аналитика
├── frontend/                      # React приложение
│   ├── src/
│   │   ├── components/           # React компоненты
│   │   ├── pages/               # Страницы приложения
│   │   ├── services/            # API клиенты
│   │   ├── types/               # TypeScript типы
│   │   └── utils/               # Утилиты
│   └── package.json             # Node.js зависимости
├── docker-compose.yml           # Конфигурация Docker
└── README.md                    # Этот файл
```

## 🔧 Конфигурация

### Переменные окружения

Backend сервисы настраиваются через переменные окружения в `docker-compose.yml`:

```yaml
# База данных
POSTGRES_DB=tw_accounting
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_URL=redis://redis:6379

# Приложение
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### Настройка разработки

Для локальной разработки скопируйте `.env.example` в `.env` и настройте:

```bash
cp services/accounting/.env.example services/accounting/.env
```

## 🤝 Разработка

### Команды для разработки

```bash
# Запуск всех сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f accounting

# Перезапуск сервиса после изменений
docker compose restart accounting

# Остановка всех сервисов  
docker compose down

# Frontend разработка
cd frontend
npm run dev
```

### Применение миграций

```bash
# Создание новой миграции
docker exec tw_accounting_service alembic revision --autogenerate -m "Description"

# Применение миграций
docker exec tw_accounting_service alembic upgrade head
```

## 📚 Дополнительная документация

- [Архитектура системы](docs/architecture.md)
- [План разработки](docs/plan.md)
- [Требования и правила](docs/rules&requirements.md)

## 📄 Лицензия

Этот проект предназначен для демонстрации современных подходов к разработке микросервисных систем с использованием Python, FastAPI, React и TypeScript.

## 👨‍💻 Автор

Разработано с использованием современных технологий для создания масштабируемой системы бухгалтерского учета.

---

**TW Accounting** - ваш надежный помощник в ведении учета! 🚀