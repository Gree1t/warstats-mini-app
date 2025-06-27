# ⚡ Быстрая настройка Render (3 клика)

## 🎯 Цель
Настроить backend для автоматического деплоя и получения реальных данных вместо ошибки 500.

## 🚀 Быстрая настройка

### Шаг 1: Откройте Render
**Перейдите:** https://dashboard.render.com/

### Шаг 2: Создайте Blueprint
1. **Нажмите:** "New +" → "Blueprint"
2. **Подключите GitHub:** `Gree1t/warstats-mini-app` ⚠️ **ВАЖНО: именно warstats-mini-app**
3. **Нажмите:** "Apply"

### Шаг 3: Готово!
- ✅ Backend автоматически создастся
- ✅ Начнется деплой (2-3 минуты)
- ✅ Ошибка 500 исчезнет

## 🔍 Проверка

После деплоя проверьте:
```bash
curl https://warstats-backend.onrender.com/health
curl https://warstats-backend.onrender.com/player/test
```

## 📱 Результат

- ✅ Фронтенд работает с реальными данными
- ✅ Поиск игроков работает
- ✅ Автоматический деплой при каждом пуше
- ✅ Карточка техники отображается

## 🆘 Если что-то пошло не так

### Проблема: "No render.yaml found"
**Решение:**
1. Убедитесь, что выбрали репозиторий `Gree1t/warstats-mini-app` (не warstats-backend)
2. Проверьте, что файл `render.yaml` есть в корне репозитория
3. Убедитесь, что ветка `main` выбрана

### Проблема: "Repository not found"
**Решение:**
1. Проверьте правильность названия: `Gree1t/warstats-mini-app`
2. Убедитесь, что репозиторий публичный
3. Проверьте права доступа к репозиторию

## 🔧 Альтернативная настройка

Если Blueprint не работает:

1. **"New +" → "Web Service"**
2. **Подключите GitHub:** `Gree1t/warstats-mini-app`
3. **Настройки:**
   - **Name**: `warstats-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy**: ✅ Включено

## 🎉 Готово!

После настройки ваш War Thunder Stats Mini App будет полностью функционален с реальными данными! 