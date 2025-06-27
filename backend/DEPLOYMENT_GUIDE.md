# Руководство по развертыванию бэкенда

## Шаг 1: Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Назовите репозиторий: `warstats-backend`
4. Сделайте его публичным
5. НЕ инициализируйте с README (у нас уже есть файлы)

## Шаг 2: Загрузка кода на GitHub

```bash
# В папке backend выполните:
git remote add origin https://github.com/YOUR_USERNAME/warstats-backend.git
git branch -M main
git push -u origin main
```

## Шаг 3: Развертывание на Render

### Вариант A: Render (Рекомендуется - бесплатно)

1. Перейдите на [Render](https://render.com)
2. Создайте аккаунт (можно через GitHub)
3. Нажмите "New +" → "Web Service"
4. Подключите ваш GitHub репозиторий `warstats-backend`
5. Настройте:
   - **Name**: `warstats-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

6. Нажмите "Create Web Service"
7. Дождитесь завершения деплоя (5-10 минут)

### Вариант B: Railway

1. Перейдите на [Railway](https://railway.app)
2. Создайте аккаунт
3. Нажмите "New Project" → "Deploy from GitHub repo"
4. Выберите репозиторий `warstats-backend`
5. Railway автоматически определит Python проект
6. Дождитесь деплоя

### Вариант C: Heroku

1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Создайте аккаунт на [Heroku](https://heroku.com)
3. Выполните команды:
```bash
heroku login
heroku create warstats-backend
git push heroku main
```

## Шаг 4: Получение URL бэкенда

После успешного деплоя вы получите URL вида:
- Render: `https://warstats-backend.onrender.com`
- Railway: `https://warstats-backend.railway.app`
- Heroku: `https://warstats-backend.herokuapp.com`

## Шаг 5: Обновление фронтенда

1. Откройте файл `app.js` в корне проекта
2. Найдите строку с `API_BASE_URL`
3. Замените на URL вашего бэкенда:

```javascript
// Замените эту строку:
const API_BASE_URL = 'https://miniappwar.netlify.app';

// На URL вашего бэкенда:
const API_BASE_URL = 'https://your-backend-url.onrender.com';
```

4. Сохраните файл и закоммитьте изменения:
```bash
git add app.js
git commit -m "Update API URL to backend"
git push
```

## Шаг 6: Тестирование

1. Откройте ваш бэкенд URL в браузере
2. Вы должны увидеть JSON с информацией об API
3. Добавьте `/docs` к URL для документации Swagger
4. Протестируйте эндпоинты:
   - `GET /health` - проверка здоровья
   - `GET /top?limit=5` - топ игроков
   - `GET /player/TestPlayer` - поиск игрока

## Возможные проблемы

### Ошибка "Build failed"
- Проверьте, что все зависимости в `requirements.txt`
- Убедитесь, что Python версия 3.8+

### Ошибка "Application error"
- Проверьте логи в консоли развертывания
- Убедитесь, что команда запуска правильная

### CORS ошибки
- Проверьте настройки CORS в `main.py`
- Убедитесь, что домен фронтенда добавлен в `ALLOWED_ORIGINS`

## Мониторинг

- **Health Check**: `https://your-backend-url/health`
- **API Docs**: `https://your-backend-url/docs`
- **ReDoc**: `https://your-backend-url/redoc`

## Обновление бэкенда

При изменении кода:
```bash
git add .
git commit -m "Update backend"
git push
```

Render/Railway автоматически передеплоят приложения.

## Поддержка

Если что-то не работает:
1. Проверьте логи в консоли развертывания
2. Убедитесь, что все файлы загружены в репозиторий
3. Проверьте, что порт настроен правильно (`$PORT`)
4. Убедитесь, что команда запуска корректная 