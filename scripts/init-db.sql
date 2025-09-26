-- Инициализация базы данных для TW Accounting System

-- Создание расширения TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Создание базы данных для аналитики трафика (если нужна отдельная)
-- CREATE DATABASE tw_traffic_analytics;

-- Настройка для работы с JSONB
-- (PostgreSQL уже поддерживает JSONB из коробки)

-- Создание пользователя для приложения (опционально)
-- CREATE USER tw_app_user WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON DATABASE tw_accounting TO tw_app_user;

-- Комментарий: Остальные таблицы будут созданы через Alembic миграции
