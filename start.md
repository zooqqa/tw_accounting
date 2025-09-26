# 🚀 Руководство по запуску TW Accounting

## Быстрый старт

### 1. Запуск Backend сервисов
```bash
# Находясь в корневой папке проекта
docker compose up -d
```

Это запустит все backend сервисы:
- Accounting Service (порт 8001)
- API Gateway (порт 8000) 
- Traffic Analytics (порт 8002)
- PostgreSQL (порт 5432)
- Redis (порт 6379)

### 2. Запуск Frontend (для разработки)
```bash
# Переход в папку frontend
cd frontend

# Установка зависимостей (только при первом запуске)
npm install

# Запуск dev сервера
npm run dev
```

Frontend будет доступен на http://localhost:3000

### 3. Проверка работы системы

**Backend API документация:**
http://localhost:8001/docs

**Health check:**
http://localhost:8001/health

**Frontend приложение:**
http://localhost:3000

## Демо-доступ

Для входа в систему используйте:
- **Email:** `test@example.com`
- **Пароль:** `testpassword123`

## Остановка системы

```bash
# Остановка всех сервисов
docker compose down

# Остановка с удалением volumes (полная очистка)
docker compose down -v
```

## Полезные команды

### Просмотр логов
```bash
# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f accounting
```

### Перезапуск сервиса
```bash
# Перезапуск после изменений кода
docker compose restart accounting
```

### Подключение к базе данных
```bash
# Через Docker
docker exec -it tw_accounting_postgres psql -U postgres -d tw_accounting

# Через внешний клиент
Host: localhost
Port: 5432
Database: tw_accounting
Username: postgres
Password: postgres
```

## Что дальше?

После запуска системы вы можете:

1. **Изучить API** - перейти на http://localhost:8001/docs
2. **Войти в веб-интерфейс** - http://localhost:3000
3. **Создать транзакции** через API или интерфейс
4. **Протестировать крипто-функции** с TRX/USDT
5. **Изучить код** в папках `services/` и `frontend/`

## Troubleshooting

### Проблема: Frontend не запускается
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Проблема: База данных не инициализируется  
```bash
docker compose down -v
docker compose up -d
```

### Проблема: Порты заняты
Измените порты в `docker-compose.yml` или остановите процессы на портах 3000, 8000, 8001, 8002, 5432, 6379.

Система готова к использованию! 🎉
