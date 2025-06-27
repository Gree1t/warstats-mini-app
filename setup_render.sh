#!/bin/bash

echo "🚀 Настройка Render для автоматического деплоя..."

# Проверяем наличие необходимых файлов
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found"
    exit 1
fi

if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: backend/requirements.txt not found"
    exit 1
fi

if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Создаем requirements.txt если его нет
if [ ! -f "backend/requirements.txt" ]; then
    echo "📝 Создаю requirements.txt..."
    cat > backend/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
beautifulsoup4==4.12.2
lxml==4.9.3
python-multipart==0.0.6
pydantic==2.5.0
EOF
fi

# Коммитим изменения
echo "📦 Коммитим изменения..."
git add .
git commit -m "setup: add render.yaml for automatic deployment" || true

# Пушим изменения
echo "📤 Пушим изменения на GitHub..."
git push origin main

echo ""
echo "🎉 Настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Перейдите на https://dashboard.render.com/"
echo "2. Нажмите 'New +' → 'Blueprint'"
echo "3. Подключите GitHub репозиторий: Gree1t/warstats-mini-app"
echo "4. Render автоматически обнаружит render.yaml"
echo "5. Нажмите 'Apply'"
echo ""
echo "🔧 Или создайте сервис вручную:"
echo "1. 'New +' → 'Web Service'"
echo "2. Подключите GitHub: Gree1t/warstats-mini-app"
echo "3. Настройки:"
echo "   - Name: warstats-backend"
echo "   - Root Directory: backend"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Auto-Deploy: ✅ Включено"
echo ""
echo "⏱️  После настройки подождите 2-3 минуты для первого деплоя" 