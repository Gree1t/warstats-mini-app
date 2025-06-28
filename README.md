# GameStats Platform

A universal gaming statistics platform that provides comprehensive player analytics and statistics for various games. The platform consists of a FastAPI backend, Flask scraper API, Telegram bot, and a modern web frontend.

## 🎮 Features

- **Universal Game Support**: Designed to work with multiple gaming platforms
- **Real-time Statistics**: Live player data fetching and analysis
- **Hybrid Data System**: Combines real-time scraping with fallback demo data
- **Telegram Bot Integration**: Easy access to player stats via Telegram
- **Modern Web Interface**: Responsive Mini App frontend
- **RESTful API**: Comprehensive API for third-party integrations
- **Cloudflare Bypass**: Advanced scraping techniques to overcome anti-bot measures

## 🏗️ Architecture

```
GameStats Platform
├── Backend (FastAPI)          # Main API server
├── Scraper (Flask)           # Local data scraping service
├── Telegram Bot              # Bot for Telegram integration
├── Mini App (Frontend)       # Web interface
└── Documentation             # Setup and deployment guides
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Chrome/Chromium browser
- Git
- Node.js (for development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GameStats
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Setup Scraper API**
   ```bash
   cd wt_profile_api
   pip install -r requirements.txt
   python warthunder_profile_api.py
   ```

4. **Setup Telegram Bot**
   ```bash
   pip install -r requirements.txt
   python mini_app_bot.py
   ```

5. **Open Frontend**
   ```bash
   # Open mini_app/index.html in your browser
   # Or serve with a local server
   python -m http.server 3000
   ```

## 🚀 Quick Deployment to Render

### One-Click Deployment
1. **Fork this repository** to your GitHub account
2. **Sign up** at [render.com](https://render.com) (free)
3. **Click "New +"** → **"Blueprint"**
4. **Connect your GitHub** and select this repository
5. **Click "Apply"** - Render will automatically:
   - Create a Redis database for caching
   - Deploy the FastAPI backend
   - Configure all environment variables
   - Set up health monitoring

### Manual Deployment
```bash
# Clone and push to your repository
git clone <your-repo-url>
git add .
git commit -m "Initial deployment"
git push origin main

# Render will auto-deploy on push
```

### Deployment Features
- ✅ **Free Tier**: 750 hours/month
- ✅ **Auto-deploy**: Updates on every git push
- ✅ **Redis Cache**: Automatic database setup
- ✅ **Health Monitoring**: Built-in health checks
- ✅ **SSL/HTTPS**: Automatic certificates
- ✅ **Custom Domains**: Available on paid plans

📖 **Detailed deployment guide**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## 📁 Project Structure

```
GameStats/
├── backend/                  # FastAPI backend
│   ├── main.py              # Main API server
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── wt_profile_api/          # Flask scraper service
│   ├── warthunder_profile_api.py
│   ├── requirements.txt
│   └── Dockerfile
├── mini_app/               # Frontend application
│   ├── index.html          # Main page
│   ├── app.js              # Application logic
│   ├── styles.css          # Styling
│   └── _redirects          # Netlify configuration
├── mini_app_bot.py         # Telegram bot
├── deploy.sh               # Deployment script
├── render.yaml             # Render deployment config
├── .render-buildpacks      # Render buildpack config
├── netlify.toml            # Netlify configuration
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username

# API Configuration
BACKEND_URL=http://localhost:8000
SCRAPER_URL=http://localhost:8080

# Database (if using)
DATABASE_URL=your_database_url
```

### API Endpoints

#### Backend API (FastAPI)

- `GET /` - API information
- `GET /health` - Health check
- `GET /player/{username}` - Get player statistics
- `GET /player/{username}/refresh` - Force refresh player data
- `GET /top` - Get top players
- `GET /compare` - Compare two players

#### Scraper API (Flask)

- `GET /profile?username={username}&region={region}` - Get player profile
- `GET /health` - Health check

## 🚀 Deployment

### Automated Deployment

Run the deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment

1. **Backend (Render)**
   - Connect your GitHub repository to Render
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Frontend (Netlify)**
   - Connect your GitHub repository to Netlify
   - Set build directory: `mini_app`
   - Set publish directory: `mini_app`

3. **Telegram Bot**
   - Deploy to any Python hosting service
   - Set environment variables for bot token

## 🔒 Security Features

- **CORS Configuration**: Properly configured for production
- **Input Validation**: All user inputs are validated
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Comprehensive error handling and logging
- **Cloudflare Bypass**: Advanced techniques to handle anti-bot measures

## 📊 Data Sources

The platform uses a hybrid approach:

1. **Real-time Scraping**: Direct data extraction from game websites
2. **Demo Data**: Fallback data for testing and development
3. **Caching**: Intelligent caching to reduce server load
4. **Background Updates**: Asynchronous data updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the deployment guides

## 🔄 Updates

The platform is actively maintained and updated with:

- New game support
- Improved scraping techniques
- Enhanced UI/UX
- Performance optimizations
- Security updates

---

**GameStats Platform** - Universal gaming statistics for everyone! 🎮📊 