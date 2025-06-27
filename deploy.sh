#!/bin/bash

echo "🚀 Starting automatic deployment..."

# Check if we're in the right directory
if [ ! -f "netlify.toml" ]; then
    echo "❌ Error: netlify.toml not found. Make sure you're in the project root."
    exit 1
fi

# Add all changes
echo "📦 Adding all changes to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit."
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Auto-deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push to GitHub
    echo "📤 Pushing to GitHub..."
    git push origin main
    
    echo "✅ Changes pushed to GitHub!"
    echo "🔄 Netlify will automatically deploy the frontend..."
    echo "🔄 Render will automatically deploy the backend..."
fi

echo "🎉 Deployment process completed!"
echo ""
echo "📋 Next steps:"
echo "1. Wait 1-2 minutes for Netlify to deploy frontend"
echo "2. Wait 2-3 minutes for Render to deploy backend"
echo "3. Test the application at your Netlify URL"
echo "4. Test the API at https://warstats-backend.onrender.com/health" 