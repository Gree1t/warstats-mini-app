# Инструкции по деплою War Thunder Stats

## 🚀 Frontend (Netlify) - Уже работает!

Ваш Mini App уже развернут на Netlify и работает корректно:
- **URL**: https://miniappwar.netlify.app/
- **Статус**: ✅ Работает
- **Тип**: Статический сайт (HTML/CSS/JS)

### Что исправлено:
- ✅ Убраны все Python файлы из деплоя Netlify
- ✅ Удалены requirements.txt и backend.py
- ✅ Настроен правильный .gitignore
- ✅ Обновлена конфигурация netlify.toml
- ✅ Frontend работает в демо режиме

---

## 📱 Telegram Bot (Отдельный проект)

### Создание отдельного репозитория для бота:

1. **Создайте новый репозиторий** для бота
2. **Скопируйте файлы**:
   - `mini_app_bot.py`
   - `config.py`
   - `requirements.txt` (создайте новый)

### Настройка бота:

1. **Откройте** @BotFather в Telegram
2. **Отправьте** `/mybots`
3. **Выберите** ваш бот
4. **Нажмите** "Bot Settings" → "Menu Button"
5. **Установите** URL: `https://miniappwar.netlify.app/`

### Запуск бота локально:

```bash
# В отдельном репозитории бота
pip install -r requirements.txt
python mini_app_bot.py
```

---

## 🔧 Backend (Отдельный проект)

### Вариант 1: Render (Рекомендуется - бесплатно)

1. **Создайте аккаунт** на [render.com](https://render.com)
2. **Создайте новый репозиторий** для backend
3. **Добавьте файлы**:
   - `backend.py`
   - `requirements.txt`
   - `README.md`
4. **Подключите GitHub** репозиторий к Render
5. **Создайте новый Web Service**:
   - **Name**: warstats-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend.py`
   - **Plan**: Free

### Вариант 2: Railway (Альтернатива)

1. **Создайте аккаунт** на [railway.app](https://railway.app)
2. **Создайте новый репозиторий** для backend
3. **Подключите GitHub** репозиторий
4. **Railway автоматически** определит Python
5. **Настройте команду запуска**: `python backend.py`

---

## 🔗 Подключение Frontend к Backend

После развертывания backend получите URL (например: `https://warstats-backend.onrender.com`)

### Обновите API URL в frontend:

1. **Откройте файл** `app.js`
2. **Найдите строку**:
   ```javascript
   const API_BASE = 'demo';
   ```
3. **Замените на** ваш реальный URL:
   ```javascript
   const API_BASE = 'https://warstats-backend.onrender.com';
   ```
4. **Закоммитьте и отправьте** изменения:
   ```bash
   git add app.js
   git commit -m "Update backend URL"
   git push origin main
   ```

---

## ✅ Проверка работы

### 1. Frontend (Mini App)
- ✅ Откройте: https://miniappwar.netlify.app/
- ✅ Введите любой никнейм (демо данные)
- ✅ Проверьте вкладки и функционал

### 2. Backend API (после развертывания)
- ✅ Откройте: `https://your-backend-url.com/docs`
- ✅ Проверьте Swagger документацию
- ✅ Протестируйте эндпоинты

### 3. Telegram Bot (после настройки)
- ✅ Отправьте `/start` боту
- ✅ Нажмите кнопку Mini App
- ✅ Проверьте работу приложения

---

## 🚨 Устранение проблем

### Frontend не обновляется:
```bash
# Принудительный редеплой
git commit --allow-empty -m "Force redeploy"
git push origin main
```

### Backend не запускается:
- Проверьте логи в Render/Railway
- Убедитесь, что requirements.txt корректный
- Проверьте переменные окружения

### Бот не отвечает:
- Проверьте токен в config.py
- Убедитесь, что только один экземпляр запущен
- Проверьте логи бота

---

## 📊 Мониторинг

### Frontend (Netlify):
- **Аналитика**: Netlify Analytics
- **Логи**: Netlify Functions logs
- **Статус**: Netlify Status page

### Backend (Render/Railway):
- **Логи**: Dashboard → Logs
- **Метрики**: Dashboard → Metrics
- **Статус**: Dashboard → Status

---

## 📁 Рекомендуемая структура проектов

### Проект 1: Frontend (текущий репозиторий)
```
warstats-frontend/
├── index.html
├── styles.css
├── app.js
├── _redirects
├── netlify.toml
└── README.md
```

### Проект 2: Backend (новый репозиторий)
```
warstats-backend/
├── backend.py
├── requirements.txt
├── config.py
└── README.md
```

### Проект 3: Telegram Bot (новый репозиторий)
```
warstats-bot/
├── mini_app_bot.py
├── config.py
├── requirements.txt
└── README.md
```

---

**🎮 Ваш War Thunder Stats готов к использованию!** 