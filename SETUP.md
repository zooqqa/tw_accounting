# Инструкции по установке и настройке

## Предварительные требования

### 1. Установка Docker Desktop

1. Скачайте Docker Desktop для Windows с официального сайта: https://www.docker.com/products/docker-desktop/
2. Установите Docker Desktop
3. Запустите Docker Desktop
4. Убедитесь, что Docker работает: `docker --version`

### 2. Установка Python (для локальной разработки)

1. Скачайте Python 3.11+ с https://www.python.org/downloads/
2. Установите Python с опцией "Add to PATH"
3. Убедитесь, что Python установлен: `python --version`

### 3. Установка Node.js (для frontend)

1. Скачайте Node.js LTS с https://nodejs.org/
2. Установите Node.js
3. Убедитесь, что Node.js установлен: `node --version`

## Запуск проекта

### Вариант 1: Полный запуск через Docker

```bash
# Запуск всех сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

### Вариант 2: Локальная разработка

#### 1. Запуск базы данных и Redis

```bash
# Запуск только PostgreSQL и Redis
docker compose up -d postgres redis
```

#### 2. Настройка Accounting Service

```bash
cd services/accounting

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса
uvicorn app.main:app --reload --port 8001
```

#### 3. Настройка Traffic Analytics Service

```bash
cd services/traffic-analytics

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса
uvicorn app.main:app --reload --port 8002
```

#### 4. Настройка API Gateway

```bash
cd services/api-gateway

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса
uvicorn app.main:app --reload --port 8000
```

## Проверка работы

После запуска сервисов проверьте:

1. **PostgreSQL**: `http://localhost:5432` (через клиент БД)
2. **Redis**: `http://localhost:6379` (через Redis клиент)
3. **Accounting Service**: `http://localhost:8001/docs`
4. **Traffic Analytics Service**: `http://localhost:8002/docs`
5. **API Gateway**: `http://localhost:8000/docs`

## Устранение проблем

### Проблема с портами

Если порты заняты, измените их в `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Измените 8001 на другой порт
```

### Проблема с базой данных

```bash
# Очистка данных Docker
docker compose down -v

# Пересоздание контейнеров
docker compose up -d postgres redis
```

### Проблема с зависимостями Python

```bash
# Обновление pip
python -m pip install --upgrade pip

# Переустановка зависимостей
pip install -r requirements.txt --force-reinstall
```

## Следующие шаги

1. Установите Docker Desktop
2. Запустите проект через Docker Compose
3. Проверьте работу всех сервисов
4. Начните разработку согласно плану в `docs/plan.md`
