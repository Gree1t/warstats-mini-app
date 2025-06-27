#!/bin/bash

echo "🚀 Deploying GameStats Platform..."

# Проверяем наличие необходимых файлов
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found"
    exit 1
fi

if [ ! -f "mini_app/index.html" ]; then
    echo "❌ Error: mini_app/index.html not found"
    exit 1
fi

echo "✅ All required files found"

# Создаем .gitignore если его нет
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Chrome debug files
debug_*.html

# Environment variables
.env
.env.local

# Build artifacts
dist/
build/
*.egg-info/
EOF
fi

# Проверяем статус git
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial GameStats platform commit"
fi

# Проверяем изменения
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "Update GameStats platform - $(date)"
fi

echo "✅ Deployment preparation completed"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Deploy backend to Render: https://render.com"
echo "3. Deploy frontend to Netlify: https://netlify.com"
echo ""
echo "🔗 Backend API: https://gamestats-api.onrender.com"
echo "🔗 Frontend App: https://gamestats-mini-app.netlify.app"
echo ""
echo "🎉 GameStats Platform is ready for deployment!" 