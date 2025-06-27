# 🔧 Настройка Render для автоматического деплоя

## Проблема
Backend на Render не обновляется автоматически при пуше в GitHub, поэтому возвращает ошибку 500.

## Решение

### Шаг 1: Настройка Render Dashboard

1. **Перейдите на [Render Dashboard](https://dashboard.render.com/)**
2. **Найдите ваш сервис `warstats-backend`**
3. **Нажмите на него для перехода к настройкам**

### Шаг 2: Настройка автоматического деплоя

1. **В настройках сервиса найдите раздел "Build & Deploy"**
2. **Убедитесь, что:**
   - **Auto-Deploy**: Включено ✅
   - **Branch**: `main`
   - **Root Directory**: `backend`

### Шаг 3: Проверка конфигурации

Убедитесь, что в настройках указано:
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Шаг 4: Принудительный деплой

1. **В Render Dashboard найдите кнопку "Manual Deploy"**
2. **Нажмите "Deploy latest commit"**
3. **Дождитесь завершения деплоя (2-3 минуты)**

### Шаг 5: Проверка работы

После деплоя проверьте:
```bash
curl https://warstats-backend.onrender.com/health
curl https://warstats-backend.onrender.com/player/test
```

## Альтернативное решение: Создание нового сервиса

Если текущий сервис не обновляется:

1. **Удалите старый сервис в Render**
2. **Создайте новый: "New +" → "Web Service"**
3. **Подключите GitHub репозиторий**: `Gree1t/warstats-mini-app`
4. **Настройки:**
   - **Name**: `warstats-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy**: ✅ Включено

## Проверка после настройки

1. **Сделайте тестовый пуш:**
   ```bash
   echo "# test" >> README.md
   git add README.md
   git commit -m "test deploy"
   git push
   ```

2. **Проверьте логи в Render Dashboard**
3. **Убедитесь, что деплой запустился автоматически**

## Готово! 🎉

После настройки:
- Каждый пуш в GitHub автоматически обновит backend
- Ошибка 500 исчезнет
- Фронтенд будет работать с реальным API

## Если проблемы остаются

1. **Проверьте логи в Render Dashboard**
2. **Убедитесь, что `requirements.txt` существует в папке backend**
3. **Проверьте, что `main.py` не содержит синтаксических ошибок**
4. **Попробуйте создать новый сервис с нуля** 