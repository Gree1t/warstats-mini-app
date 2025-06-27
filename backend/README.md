# War Thunder Stats API Backend

FastAPI бэкенд для получения статистики игроков War Thunder.

## Возможности

- Получение статистики игроков
- Топ игроков
- Сравнение игроков
- Кэширование данных
- Поддержка регионов (en, ru, de, fr)
- CORS для фронтенда

## Быстрый старт

### Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Откройте http://localhost:8000/docs для документации API

### Docker

```bash
docker build -t warstats-backend .
docker run -p 8000:8000 warstats-backend
```

## Развертывание

### Render (Рекомендуется)

1. Создайте аккаунт на [Render](https://render.com)
2. Подключите ваш GitHub репозиторий
3. Создайте новый Web Service
4. Выберите репозиторий и папку `backend`
5. Настройте:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11

### Railway

1. Создайте аккаунт на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. Выберите папку `backend`
4. Railway автоматически определит Python проект

### Heroku

1. Создайте аккаунт на [Heroku](https://heroku.com)
2. Установите Heroku CLI
3. Выполните команды:
```bash
heroku create your-app-name
git subtree push --prefix backend heroku main
```

## API Endpoints

### GET /player/{username}
Получение статистики игрока

**Параметры:**
- `username` (path): Имя игрока
- `region` (query): Регион (en, ru, de, fr)

**Пример:**
```
GET /player/PlayerName?region=en
```

### GET /top
Получение топ игроков

**Параметры:**
- `region` (query): Регион (en, ru, de, fr)
- `limit` (query): Количество игроков (1-1000)

**Пример:**
```
GET /top?region=en&limit=100
```

### GET /compare
Сравнение двух игроков

**Параметры:**
- `player1` (query): Первый игрок
- `player2` (query): Второй игрок
- `region` (query): Регион (en, ru, de, fr)

**Пример:**
```
GET /compare?player1=Player1&player2=Player2&region=en
```

## Конфигурация

Создайте файл `.env` на основе `env.example`:

```bash
cp env.example .env
```

Настройте переменные окружения:

- `API_HOST`: Хост для запуска (по умолчанию: 0.0.0.0)
- `API_PORT`: Порт (по умолчанию: 8000)
- `DEBUG`: Режим отладки (true/false)
- `ALLOWED_ORIGINS`: Разрешенные домены для CORS
- `CACHE_DURATION`: Время кэширования в секундах
- `REDIS_URL`: URL Redis для кэширования

## Структура проекта

```
backend/
├── main.py              # Основной файл FastAPI
├── requirements.txt     # Python зависимости
├── Dockerfile          # Docker конфигурация
├── env.example         # Пример конфигурации
└── README.md           # Документация
```

## Обновление фронтенда

После развертывания бэкенда обновите URL API в фронтенде:

1. Откройте `app.js` в корне проекта
2. Найдите строку с `API_BASE_URL`
3. Замените на URL вашего бэкенда:

```javascript
const API_BASE_URL = 'https://your-backend-url.onrender.com';
```

## Мониторинг

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs` (Swagger UI)
- **ReDoc**: `GET /redoc`

## Логирование

Логи выводятся в stdout/stderr для совместимости с облачными платформами.

## Поддержка

При возникновении проблем:

1. Проверьте логи в консоли развертывания
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию CORS
4. Убедитесь, что порт настроен правильно 