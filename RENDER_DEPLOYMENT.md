# 🚀 War Thunder Statistics - Render Deployment Guide

## Overview
This guide will help you deploy the War Thunder Statistics backend to Render, a modern cloud platform that offers free hosting for web services.

## 📋 Prerequisites
- GitHub account with your Warstats repository
- Render account (free at [render.com](https://render.com))

## 🛠️ Deployment Steps

### 1. Prepare Your Repository
Ensure your repository has the following files:
- `render.yaml` - Render configuration
- `.render-buildpacks` - Python buildpack configuration
- `backend/main.py` - FastAPI application
- `backend/requirements.txt` - Python dependencies
- `backend/Dockerfile` - Docker configuration (optional)

### 2. Connect to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Blueprint"
3. Connect your GitHub account and select the Warstats repository
4. Render will automatically detect the `render.yaml` configuration

### 3. Configure Services
The `render.yaml` file configures:
- **Redis Database**: For caching and session storage
- **Web Service**: FastAPI backend with Python 3.11
- **Environment Variables**: All necessary configuration
- **Health Checks**: Automatic monitoring
- **Auto-deploy**: Automatic updates on git push

### 4. Environment Variables
The following environment variables are automatically configured:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection string | Auto-generated |
| `WT_API_BASE_URL` | War Thunder API base URL | `https://warthunder.com/en/api` |
| `STATSHARK_API_URL` | Statshark API URL | `https://api.statshark.net` |
| `WT_LIVE_API_URL` | WT Live API URL | `https://warthunder.live/api` |
| `CACHE_TTL` | Cache time-to-live (seconds) | `21600` (6 hours) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENABLE_METRICS` | Enable Prometheus metrics | `true` |
| `CLOUDFLARE_BYPASS_ENABLED` | Enable Cloudflare bypass | `true` |

### 5. Manual Deployment (Alternative)
If you prefer manual setup:

1. **Create Web Service**:
   - Type: Web Service
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Create Redis Database**:
   - Type: Redis
   - Plan: Free
   - Name: `warstats-redis`

3. **Link Services**:
   - Connect the web service to the Redis database
   - Set the `REDIS_URL` environment variable

## 🔧 Configuration Details

### render.yaml Structure
```yaml
databases:
  - name: warstats-redis          # Redis database for caching
    plan: free

services:
  - type: web                     # Web service
    name: warstats-backend        # Service name
    env: python                   # Python environment
    plan: free                    # Free tier
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health      # Health check endpoint
    autoDeploy: true              # Auto-deploy on git push
```

### Health Check Endpoint
The application includes a health check at `/health`:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T15:30:00Z",
  "version": "3.0.0",
  "services": {
    "redis": "connected",
    "api": "operational"
  }
}
```

## 📊 Monitoring & Logs

### View Logs
1. Go to your service dashboard on Render
2. Click "Logs" tab
3. Monitor real-time application logs

### Health Monitoring
- Render automatically monitors the `/health` endpoint
- Service will restart if health checks fail
- Email notifications for service issues

### Metrics
Access Prometheus metrics at `/metrics`:
- Request counts
- Response times
- Error rates
- Cache hit/miss ratios

## 🔄 Auto-Deployment
- Every push to the main branch triggers automatic deployment
- Build process takes 2-5 minutes
- Zero-downtime deployments
- Automatic rollback on failure

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Runtime Errors**:
   - Monitor application logs
   - Check environment variables
   - Verify Redis connection

3. **Health Check Failures**:
   - Ensure `/health` endpoint is accessible
   - Check service dependencies
   - Verify port configuration

### Debug Commands
```bash
# Check service status
curl https://your-service.onrender.com/health

# View metrics
curl https://your-service.onrender.com/metrics

# Test API endpoints
curl https://your-service.onrender.com/docs
```

## 📈 Scaling
- **Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: Always-on, custom domains, SSL certificates
- **Auto-scaling**: Available on paid plans

## 🔐 Security
- Automatic HTTPS/SSL certificates
- Environment variable encryption
- Database connection security
- Rate limiting enabled

## 📞 Support
- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Community Forum**: [community.render.com](https://community.render.com)
- **Email Support**: Available on paid plans

## 🎉 Success Indicators
Your deployment is successful when:
- ✅ Service shows "Live" status
- ✅ Health check returns 200 OK
- ✅ API documentation is accessible at `/docs`
- ✅ Redis connection is established
- ✅ All environment variables are set

## 🔗 Useful Links
- **API Documentation**: `https://your-service.onrender.com/docs`
- **Health Check**: `https://your-service.onrender.com/health`
- **Metrics**: `https://your-service.onrender.com/metrics`
- **ReDoc**: `https://your-service.onrender.com/redoc`

---

**Happy Deploying! 🚀** 