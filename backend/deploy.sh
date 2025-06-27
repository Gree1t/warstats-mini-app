#!/bin/bash

# Скрипт для автоматического развертывания бэкенда
echo "🚀 Запуск развертывания бэкенда War Thunder Stats..."

# Проверяем, что мы в правильной папке
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: main.py не найден. Убедитесь, что вы в папке backend/"
    exit 1
fi

# Проверяем git статус
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Все изменения закоммичены"
else
    echo "📝 Обнаружены незакоммиченные изменения"
    echo "Добавляем все файлы..."
    git add .
    
    echo "Введите сообщение коммита (или нажмите Enter для 'Update backend'):"
    read commit_message
    if [ -z "$commit_message" ]; then
        commit_message="Update backend"
    fi
    
    git commit -m "$commit_message"
fi

# Проверяем, есть ли remote origin
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Remote origin не настроен"
    echo "Пожалуйста, выполните следующие команды:"
    echo "1. Создайте репозиторий на GitHub: https://github.com/new"
    echo "2. Назовите его: warstats-backend"
    echo "3. Выполните:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/warstats-backend.git"
    echo "   git branch -M main"
    exit 1
fi

# Пушим изменения
echo "📤 Отправляем изменения на GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Код успешно отправлен на GitHub"
    echo ""
    echo "🎯 Следующие шаги для развертывания:"
    echo ""
    echo "1. Перейдите на Render: https://render.com"
    echo "2. Создайте новый Web Service"
    echo "3. Подключите ваш GitHub репозиторий warstats-backend"
    echo "4. Настройте:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
    echo "   - Environment: Python 3"
    echo ""
    echo "5. После деплоя обновите API_BASE_URL в app.js"
    echo ""
    echo "📚 Подробные инструкции в файле DEPLOYMENT_GUIDE.md"
else
    echo "❌ Ошибка при отправке кода"
    exit 1
fi 