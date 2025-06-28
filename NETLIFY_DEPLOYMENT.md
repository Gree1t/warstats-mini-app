# GameStats Platform - Netlify Deployment Guide

## 🚀 Deploying GameStats Platform to Netlify

This guide will help you deploy the GameStats Platform frontend to Netlify with proper configuration.

## 📋 Prerequisites

- GitHub repository with GameStats Platform code
- Netlify account (free tier available)
- Backend API deployed (Render, Railway, etc.)

## 🔧 Step-by-Step Deployment

### 1. Connect Repository to Netlify

1. **Login to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign in with GitHub account

2. **New Site from Git**
   - Click "New site from Git"
   - Choose "GitHub" as provider
   - Select your repository: `Gree1t/warstats-mini-app`

### 2. Configure Build Settings

**Build Settings:**
- **Build command**: `echo 'GameStats Platform - Universal Gaming Statistics'`
- **Publish directory**: `mini_app`
- **Base directory**: (leave empty)

**Environment Variables:**
```
NODE_VERSION=18
NPM_VERSION=9
```

### 3. Advanced Settings

**Domain Settings:**
- **Custom domain**: `gamestats-platform.netlify.app` (or your preferred domain)
- **HTTPS**: Automatically enabled

**Build & Deploy:**
- **Auto deploy**: Enabled
- **Branch deploy**: `main`
- **Preview deploy**: Enabled

### 4. Environment Variables (Optional)

Add these environment variables in Netlify dashboard:

```
BACKEND_URL=https://your-backend-api.onrender.com
SCRAPER_URL=https://your-scraper-api.com
TELEGRAM_BOT_URL=https://your-telegram-bot.com
```

## 🔧 Configuration Files

### netlify.toml (Root)
```toml
[build]
  publish = "mini_app"
  command = "echo 'GameStats Platform - Universal Gaming Statistics'"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
  force = true

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Content-Security-Policy = "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:; font-src 'self' https: data:;"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
```

### _redirects (mini_app/)
```
# GameStats Platform - Universal Gaming Statistics
# Redirects for SPA (Single Page Application)

# Main SPA redirect - all routes go to index.html
/*    /index.html   200

# API redirects (if needed)
/api/*    https://gamestats-api.onrender.com/:splat    200

# Health check
/health    /index.html   200

# Static assets (fallback)
/assets/*    /index.html   200
```

## 🎯 Deployment Options

### Option 1: Automatic Deployment (Recommended)

1. **Connect GitHub Repository**
   - Netlify will automatically detect changes
   - Deploys on every push to `main` branch

2. **Preview Deployments**
   - Automatic preview for pull requests
   - Test changes before merging

### Option 2: Manual Deployment

1. **Build Locally**
   ```bash
   cd mini_app
   # Test locally
   python -m http.server 3000
   ```

2. **Drag & Drop**
   - Drag `mini_app` folder to Netlify dashboard
   - Automatic deployment

### Option 3: CLI Deployment

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy**
   ```bash
   cd mini_app
   netlify deploy --prod
   ```

## 🔒 Security Configuration

### Headers Configuration
The platform includes comprehensive security headers:

- **X-Frame-Options**: Prevents clickjacking
- **X-XSS-Protection**: XSS protection
- **Content-Security-Policy**: Resource loading control
- **Strict-Transport-Security**: HTTPS enforcement
- **Permissions-Policy**: Feature policy control

### CORS Configuration
```javascript
// In your frontend app.js
const API_BASE = 'https://your-backend-api.onrender.com';
```

## 📊 Performance Optimization

### Caching Strategy
- **Static assets**: 1 year cache
- **HTML files**: No cache (always fresh)
- **API responses**: Controlled by backend

### Compression
- **Gzip**: Automatically enabled
- **Brotli**: Available for modern browsers
- **Image optimization**: Automatic

### CDN
- **Global CDN**: Automatic worldwide distribution
- **Edge caching**: Fast response times
- **DDoS protection**: Built-in

## 🔍 Monitoring & Analytics

### Netlify Analytics
- **Page views**: Track user engagement
- **Performance**: Monitor load times
- **Errors**: Track deployment issues

### Custom Analytics
```javascript
// Add to your app.js
if (typeof gtag !== 'undefined') {
  gtag('config', 'GA_MEASUREMENT_ID');
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check build command
   - Verify publish directory
   - Check environment variables

2. **404 Errors**
   - Verify `_redirects` file
   - Check SPA configuration
   - Test routes locally

3. **CORS Errors**
   - Update backend CORS settings
   - Check API URLs
   - Verify HTTPS configuration

### Debug Commands
```bash
# Test locally
cd mini_app
python -m http.server 3000

# Check Netlify status
netlify status

# View deployment logs
netlify logs
```

## 🔄 Continuous Deployment

### GitHub Integration
1. **Webhook**: Automatic deployment on push
2. **Branch protection**: Require status checks
3. **Preview deployments**: Test before merge

### Deployment Pipeline
```
GitHub Push → Netlify Build → Deploy → CDN Distribution
```

## 📱 Mobile Optimization

### PWA Features
- **Service Worker**: Offline functionality
- **Manifest**: App-like experience
- **Responsive Design**: Mobile-first approach

### Performance
- **Lazy Loading**: Images and components
- **Code Splitting**: Optimized bundles
- **Critical CSS**: Above-the-fold optimization

## 🎉 Success Checklist

- [ ] Repository connected to Netlify
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled
- [ ] Security headers active
- [ ] CORS configured
- [ ] Analytics tracking
- [ ] Mobile testing completed
- [ ] Performance monitoring active

## 🔗 Useful Links

- [Netlify Documentation](https://docs.netlify.com/)
- [Netlify CLI](https://docs.netlify.com/cli/get-started/)
- [Build Configuration](https://docs.netlify.com/configure-builds/overview/)
- [Redirects & Rewrites](https://docs.netlify.com/routing/redirects/)
- [Headers & Security](https://docs.netlify.com/routing/headers/)

---

**GameStats Platform** - Universal gaming statistics for everyone! 🎮📊

*Deployment guide updated: December 28, 2024* 