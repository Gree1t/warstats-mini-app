#!/bin/bash

# War Thunder Statistics Backend - Render Deployment Script
echo "🚀 Starting War Thunder Statistics Backend deployment..."

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Set environment variables for production
export ENVIRONMENT=production
export PYTHON_VERSION=3.11.0
export PORT=8000

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt

# Run health check
echo "🏥 Running health check..."
python -c "
import asyncio
import httpx
import time

async def health_check():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/health', timeout=10)
            if response.status_code == 200:
                print('✅ Health check passed')
                return True
            else:
                print(f'❌ Health check failed: {response.status_code}')
                return False
    except Exception as e:
        print(f'❌ Health check error: {e}')
        return False

# Start server in background
import subprocess
import threading
import time

def start_server():
    subprocess.run(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'])

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(5)

# Run health check
result = asyncio.run(health_check())
if result:
    print('🎉 Deployment successful!')
    print('📊 API Documentation: http://localhost:8000/docs')
    print('🔍 Health Check: http://localhost:8000/health')
    print('📈 Metrics: http://localhost:8000/metrics')
else:
    print('💥 Deployment failed!')
    exit(1)
"

echo "✅ Deployment script completed!" 