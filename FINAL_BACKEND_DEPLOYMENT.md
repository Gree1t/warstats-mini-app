# 🚀 Финальное развертывание бэкенда War Thunder Stats

## ✅ Что у нас есть

1. **Фронтенд**: Работает на Netlify (https://miniappwar.netlify.app)
2. **Бэкенд**: Готов к развертыванию в папке `backend/`
3. **Telegram Bot**: Работает локально

## 🎯 План действий

### Шаг 1: Создание репозитория для бэкенда

1. Перейдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Назовите: `warstats-backend`
4. Сделайте публичным
5. НЕ инициализируйте с README

### Шаг 2: Загрузка бэкенда на GitHub

```bash
cd backend
git remote add origin https://github.com/YOUR_USERNAME/warstats-backend.git
git branch -M main
git push -u origin main
```

### Шаг 3: Развертывание на Render (Бесплатно)

1. Перейдите на [Render](https://render.com)
2. Создайте аккаунт (через GitHub)
3. Нажмите "New +" → "Web Service"
4. Подключите репозиторий `warstats-backend`
5. Настройте:
   - **Name**: `warstats-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

6. Нажмите "Create Web Service"
7. Дождитесь деплоя (5-10 минут)

### Шаг 4: Получение URL бэкенда

После деплоя вы получите URL вида:
`https://warstats-backend-xxxx.onrender.com`

### Шаг 5: Обновление фронтенда

1. Откройте файл `app.js` в корне проекта
2. Найдите строку:
```javascript
const API_BASE = 'https://your-backend-url.onrender.com';
```
3. Замените на ваш реальный URL:
```javascript
const API_BASE = 'https://warstats-backend-xxxx.onrender.com';
```

4. Сохраните и закоммитьте:
```bash
git add app.js
git commit -m "Update API URL to backend"
git push
```

### Шаг 6: Тестирование

1. Откройте ваш бэкенд URL в браузере
2. Вы должны увидеть JSON с информацией об API
3. Добавьте `/docs` для документации Swagger
4. Протестируйте:
   - `GET /health` - проверка здоровья
   - `GET /top?limit=5` - топ игроков

### Шаг 7: Обновление Telegram Bot

1. Откройте `mini_app_bot.py`
2. Убедитесь, что URL Mini App правильный:
```python
MINI_APP_URL = "https://miniappwar.netlify.app"
```

## 🔧 Альтернативные платформы

### Railway
1. Перейдите на [Railway](https://railway.app)
2. Создайте проект
3. Подключите GitHub репозиторий
4. Railway автоматически определит Python проект

### Heroku
1. Установите Heroku CLI
2. Выполните:
```bash
heroku create warstats-backend
git push heroku main
```

## 📊 Мониторинг

- **Health Check**: `https://your-backend-url/health`
- **API Docs**: `https://your-backend-url/docs`
- **ReDoc**: `https://your-backend-url/redoc`

## 🐛 Возможные проблемы

### Build failed
- Проверьте `requirements.txt`
- Убедитесь, что Python 3.8+

### Application error
- Проверьте логи в Render
- Убедитесь, что команда запуска правильная

### CORS ошибки
- Проверьте настройки CORS в `main.py`
- Убедитесь, что домен фронтенда добавлен

## 🎉 Результат

После успешного развертывания у вас будет:

1. **Фронтенд**: https://miniappwar.netlify.app
2. **Бэкенд**: https://your-backend-url.onrender.com
3. **Telegram Bot**: Работает локально
4. **Полная интеграция**: Фронтенд + Бэкенд + Telegram

## 📞 Поддержка

Если что-то не работает:
1. Проверьте логи в Render
2. Убедитесь, что все URL правильные
3. Проверьте, что порт настроен (`$PORT`)
4. Убедитесь, что команда запуска корректная

## 🚀 Автоматическое развертывание

В папке `backend/` есть скрипт `deploy.sh`:
```bash
cd backend
./deploy.sh
```

Этот скрипт автоматически:
- Проверит изменения
- Закоммитит их
- Отправит на GitHub
- Покажет инструкции для Render 