# 🔧 Ручная настройка Render (если Blueprint не работает)

## 🎯 Проблема
Render не может найти `render.yaml` в репозитории `Gree1t/warstats-backend`

## ✅ Решение: Ручная настройка

### Шаг 1: Создайте Web Service
1. **Перейдите:** https://dashboard.render.com/
2. **Нажмите:** "New +" → "Web Service"
3. **Подключите GitHub:** `Gree1t/warstats-mini-app`

### Шаг 2: Настройте сервис
**Основные настройки:**
- **Name**: `warstats-backend`
- **Root Directory**: `backend`
- **Environment**: `Python 3`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Auto-Deploy**: ✅ Включено

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
- **PYTHON_VERSION**: `3.9.16`

### Шаг 3: Создайте сервис
1. **Нажмите:** "Create Web Service"
2. **Подождите** 2-3 минуты для деплоя

## 🔍 Проверка

После деплоя проверьте:
```bash
curl https://warstats-backend.onrender.com/health
```

Должен вернуть: `{"status": "healthy"}`

## 🎉 Результат

- ✅ Backend работает на Render
- ✅ Фронтенд получает реальные данные
- ✅ Ошибка 500 исчезнет
- ✅ Mini App полностью функционален

## 📱 Обновление фронтенда

После успешного деплоя backend, фронтенд автоматически обновится и будет использовать реальные данные вместо ошибок. 