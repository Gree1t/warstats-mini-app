# 🚀 Автоматический деплой - Настройка

## Что уже настроено

✅ **Frontend (Netlify)**
- Автоматический деплой при пуше в GitHub
- Конфигурация в `netlify.toml`
- Публикация из папки `mini_app`

✅ **Backend (Render)**
- Конфигурация в `backend/render.yaml`
- Автоматический деплой при пуше в GitHub
- Health check endpoint: `/health`

✅ **Скрипт автоматического деплоя**
- `deploy.sh` - автоматически коммитит и пушит изменения

## Настройка Render (Backend)

1. **Перейдите на [Render Dashboard](https://dashboard.render.com/)**
2. **Нажмите "New +" → "Blueprint"**
3. **Подключите GitHub репозиторий**: `Gree1t/warstats-mini-app`
4. **Render автоматически обнаружит `render.yaml`**
5. **Нажмите "Apply"**

**Или вручную:**
1. **New +" → "Web Service"**
2. **Подключите GitHub репозиторий**
3. **Настройки:**
   - **Name**: `warstats-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

## Настройка Netlify (Frontend)

1. **Перейдите на [Netlify Dashboard](https://app.netlify.com/)**
2. **Нажмите "Add new site" → "Import an existing project"**
3. **Подключите GitHub репозиторий**: `Gree1t/warstats-mini-app`
4. **Настройки:**
   - **Base directory**: `mini_app`
   - **Build command**: (оставьте пустым)
   - **Publish directory**: `.` (точка)

## Автоматический деплой

### Для быстрого деплоя:
```bash
./deploy.sh
```

### Вручную:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## Проверка работы

### Frontend:
- URL: Ваш Netlify URL
- Статус: Автоматически обновляется при пуше

### Backend:
- URL: `https://warstats-backend.onrender.com`
- Health check: `https://warstats-backend.onrender.com/health`
- API: `https://warstats-backend.onrender.com/player/{username}`

## Мониторинг

### Netlify:
- Dashboard → Ваш сайт → Deploys
- Автоматические деплои при каждом пуше

### Render:
- Dashboard → warstats-backend → Logs
- Автоматические деплои при каждом пуше

## Troubleshooting

### Если backend не обновляется:
1. Проверьте логи в Render Dashboard
2. Убедитесь, что `render.yaml` в корне репозитория
3. Проверьте `requirements.txt` в папке backend

### Если frontend не обновляется:
1. Проверьте логи в Netlify Dashboard
2. Убедитесь, что `netlify.toml` настроен правильно
3. Проверьте, что файлы в папке `mini_app`

## Структура проекта

```
Warstats/
├── mini_app/           # Frontend (Netlify)
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── netlify.toml
├── backend/            # Backend (Render)
│   ├── main.py
│   ├── requirements.txt
│   └── render.yaml
├── netlify.toml        # Основная конфигурация Netlify
└── deploy.sh           # Скрипт автоматического деплоя
```

## Готово! 🎉

После настройки:
1. Каждый пуш в GitHub автоматически запустит деплой
2. Frontend обновится через 1-2 минуты
3. Backend обновится через 2-3 минуты
4. Используйте `./deploy.sh` для быстрого деплоя 