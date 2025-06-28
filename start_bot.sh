#!/bin/bash

# War Thunder Statistics Telegram Bot Startup Script

echo "🤖 Starting War Thunder Statistics Telegram Bot..."

# Check if TELEGRAM_BOT_TOKEN is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN environment variable is not set!"
    echo "Please set your Telegram bot token:"
    echo "export TELEGRAM_BOT_TOKEN=your_bot_token_here"
    exit 1
fi

# Check if backend URL is set
if [ -z "$BACKEND_URL" ]; then
    echo "⚠️ Warning: BACKEND_URL not set, using default Render URL"
    export BACKEND_URL="https://warstats-backend-f6hw.onrender.com"
fi

echo "✅ Environment variables configured:"
echo "   BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:0:10}..."
echo "   BACKEND_URL: $BACKEND_URL"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r bot_requirements.txt

# Test backend connection
echo "🔍 Testing backend connection..."
python3 -c "
import asyncio
import httpx

async def test_backend():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('$BACKEND_URL/health', timeout=10)
            if response.status_code == 200:
                print('✅ Backend is accessible')
                return True
            else:
                print(f'❌ Backend returned status: {response.status_code}')
                return False
    except Exception as e:
        print(f'❌ Backend connection failed: {e}')
        return False

asyncio.run(test_backend())
"

# Start the bot
echo "🚀 Starting bot..."
python3 mini_app_bot.py 