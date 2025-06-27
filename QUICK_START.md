# 🚀 Быстрый старт - War Thunder Stats

## ✅ Что готово

1. **Фронтенд**: https://miniappwar.netlify.app ✅
2. **Telegram Bot**: Работает локально ✅
3. **Бэкенд**: Готов к развертыванию ✅

## 🎯 Следующие шаги

### 1. Разверните бэкенд (5 минут)

```bash
cd backend
./deploy.sh
```

Следуйте инструкциям скрипта для создания репозитория и развертывания на Render.

### 2. Обновите URL в фронтенде

После получения URL бэкенда (например, `https://warstats-backend-xxxx.onrender.com`):

1. Откройте `app.js`
2. Замените строку:
```javascript
const API_BASE = 'https://your-backend-url.onrender.com';
```
3. На ваш реальный URL:
```javascript
const API_BASE = 'https://warstats-backend-xxxx.onrender.com';
```

### 3. Запустите Telegram Bot

```bash
python3 mini_app_bot.py
```

## 🎉 Результат

После этого у вас будет полностью работающее приложение:
- Telegram Mini App с реальными данными
- Бэкенд API для обработки запросов
- Telegram Bot для открытия Mini App

## 📚 Подробные инструкции

- `FINAL_BACKEND_DEPLOYMENT.md` - полное руководство по развертыванию
- `backend/DEPLOYMENT_GUIDE.md` - инструкции для бэкенда
- `backend/README.md` - документация API

## 🆘 Если что-то не работает

1. Проверьте логи в Render
2. Убедитесь, что все URL правильные
3. Проверьте, что бот запущен
4. Убедитесь, что фронтенд обновлен

## 📞 Поддержка

Все файлы готовы к использованию. Просто следуйте инструкциям выше! 