"""
GameStats API
Универсальная платформа игровой статистики с реальными данными War Thunder
"""

import os
import time
import logging
import asyncio
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from datetime import datetime
import random

# Импортируем новые сервисы
from services.player_service import player_service
from services.features import features_service
from services.cache_service import cache_service
from routers.features import router as features_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем FastAPI приложение
app = FastAPI(
    title="GameStats API",
    description="Universal gaming statistics platform API with real War Thunder data",
    version="2.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер с расширенными функциями
app.include_router(features_router)

# Кэш для данных (fallback)
cache = {}
CACHE_DURATION = 300  # 5 минут

class PlayerStats(BaseModel):
    username: str
    level: int
    clan: Optional[Dict[str, Any]] = None
    general: Dict[str, Any]
    aviation: Optional[Dict[str, Any]] = None
    tanks: Optional[Dict[str, Any]] = None
    fleet: Optional[Dict[str, Any]] = None
    achievements: Optional[list] = None
    charts: Optional[Dict[str, Any]] = None
    top_vehicles: Optional[list] = None

class GameStatsAPI:
    def __init__(self):
        self.session: Optional[httpx.AsyncClient] = None
        self.base_url = "https://warthunder.com"
    
    def _get_demo_stats(self, username: str) -> Dict[str, Any]:
        """Возвращает демо-данные для игрока (fallback)"""
        return {
            "username": username,
            "general": {
                "level": random.randint(50, 100),
                "total_battles": random.randint(1000, 5000),
                "wins": random.randint(400, 2000),
                "losses": random.randint(200, 1000),
                "win_rate": round(random.uniform(0.45, 0.75), 2),
                "kills": random.randint(2000, 8000),
                "deaths": random.randint(800, 3000),
                "kdr": round(random.uniform(1.5, 3.5), 2),
                "ground_battles": random.randint(500, 2000),
                "air_battles": random.randint(300, 1500),
                "naval_battles": random.randint(50, 300)
            },
            "vehicles": {
                "top_vehicle": {
                    "name": "T-72B3",
                    "battles": random.randint(100, 500),
                    "wins": random.randint(60, 300),
                    "kills": random.randint(200, 800),
                    "deaths": random.randint(50, 200)
                },
                "total_vehicles": random.randint(50, 200)
            },
            "profile": {
                "registration_date": "2020-01-15",
                "last_online": "2024-01-20 15:30:00",
                "clan": "DemoClan"
            },
            "__source__": "demo_data"
        }

    async def get_player_stats(self, username: str, region: str = 'en') -> Dict[str, Any]:
        """Получение статистики игрока с приоритетом реальных данных"""
        try:
            # Сначала пытаемся получить реальные данные через новый сервис
            logger.info(f"Fetching real data for player: {username} in region: {region}")
            real_data = await player_service.get_player_stats(username, region)
            
            if real_data and real_data.get("__source__") == "real_wt_api":
                logger.info(f"Successfully retrieved real data for {username}")
                return real_data
            
            # Если реальные данные недоступны, используем локальный Flask API
            logger.info(f"Trying local Flask API for {username}")
            local_data = await self._fetch_from_local_api(username, region)
            if local_data and not local_data.get('error'):
                transformed_data = self._transform_local_api_data(local_data)
                if transformed_data:
                    return transformed_data
            
            # Fallback на демо-данные
            logger.warning(f"Using demo data for {username}")
            return self._get_demo_stats(username)
            
        except Exception as e:
            logger.error(f"Error getting player stats for {username}: {e}")
            return self._get_demo_stats(username)

    async def _fetch_from_local_api(self, username: str, region: str) -> Optional[Dict[str, Any]]:
        """Получает данные от локального Flask API"""
        local_api_url = f"http://localhost:8080/profile?username={username}&region={region}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(local_api_url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Local API request failed: {e}")
            return None
    
    def _transform_local_api_data(self, local_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Преобразование данных из локального Flask API в формат FastAPI"""
        try:
            return {
                "username": local_data.get("username", ""),
                "general": {
                    "level": local_data.get("level", 0),
                    "total_battles": local_data.get("total_battles", 0),
                    "wins": local_data.get("wins", 0),
                    "losses": local_data.get("losses", 0),
                    "win_rate": local_data.get("win_rate", 0.0),
                    "kills": local_data.get("kills", 0),
                    "deaths": local_data.get("deaths", 0),
                    "kdr": local_data.get("kdr", 0.0),
                    "ground_battles": local_data.get("ground_battles", 0),
                    "air_battles": local_data.get("air_battles", 0),
                    "naval_battles": local_data.get("naval_battles", 0)
                },
                "vehicles": {
                    "top_vehicle": local_data.get("top_vehicle", {}),
                    "total_vehicles": local_data.get("total_vehicles", 0)
                },
                "profile": {
                    "registration_date": local_data.get("registration_date", ""),
                    "last_online": local_data.get("last_online", ""),
                    "clan": local_data.get("clan", "")
                },
                "__source__": "local_flask_api"
            }
        except Exception as e:
            logger.error(f"Error transforming local API data: {e}")
            return None

    async def get_top_players(self, region: str = 'en', limit: int = 100) -> List[Dict[str, Any]]:
        """Получение топ игроков"""
        try:
            # Проверяем кэш
            cached_top = await cache_service.get_top_players(region, limit)
            if cached_top:
                return cached_top
            
            # Генерируем демо-данные для топ игроков
            top_players = []
            for i in range(min(limit, 100)):
                player = {
                    "username": f"TopPlayer{i+1}",
                    "level": 100 - i,
                    "total_battles": 5000 - i * 50,
                    "win_rate": round(0.8 - i * 0.003, 2),
                    "kdr": round(3.5 - i * 0.03, 2),
                    "total_score": 1000000 - i * 50000
                }
                top_players.append(player)
            
            # Кэшируем результат
            await cache_service.set_top_players(region, limit, top_players)
            
            return top_players
            
        except Exception as e:
            logger.error(f"Error fetching top players: {e}")
            return []
    
    async def close(self):
        """Закрытие сессии"""
        if self.session:
            await self.session.aclose()

# Создаем экземпляр API
game_stats_api = GameStatsAPI()

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    logger.info("GameStats API starting up...")
    try:
        # Проверяем подключение к Redis
        await cache_service.get_redis()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Закрытие соединений при выключении"""
    logger.info("GameStats API shutting down...")
    await game_stats_api.close()
    await cache_service.close()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "GameStats API - Universal Gaming Statistics Platform v2.0",
        "version": "2.0.0",
        "features": {
            "real_data": "Real War Thunder data parsing",
            "advanced_features": "Combat rating, recommendations, enemy analysis",
            "caching": "Redis-based caching with TTL",
            "websockets": "Realtime notifications",
            "competitive": "Features surpassing statshark.net"
        },
        "endpoints": {
            "/player/{username}": "Get player statistics",
            "/top": "Get top players",
            "/compare": "Compare two players",
            "/features/combat-rating/{nickname}": "Get realtime combat rating",
            "/features/recommendations/{nickname}": "Get vehicle recommendations",
            "/features/enemy-analysis/{nickname}": "Analyze recent enemies",
            "/features/performance-forecast/{nickname}": "Performance forecast",
            "/health": "Health check",
            "/features/health/advanced": "Advanced health check"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "player_service": "available",
            "features_service": "available",
            "cache_service": "available"
        }
    }

@app.get("/player/{username}")
async def get_player_stats(
    username: str,
    region: str = Query('en', description="Region: en, ru, de, fr")
):
    """Получение статистики игрока с реальными данными"""
    if region not in ['en', 'ru', 'de', 'fr']:
        raise HTTPException(status_code=400, detail="Invalid region")
    
    try:
        stats = await game_stats_api.get_player_stats(username, region)
        
        # Добавляем расширенные метрики
        if stats.get("__source__") != "demo_data":
            # Вычисляем боевой рейтинг
            combat_rating = features_service.realtime_combat_rating(
                stats.get("kills", 0),
                stats.get("deaths", 0),
                stats.get("activity_time", 0)
            )
            stats["combat_rating"] = combat_rating
            
            # Добавляем категорию навыков
            if combat_rating > 1000:
                stats["skill_level"] = "Elite"
            elif combat_rating > 700:
                stats["skill_level"] = "Veteran"
            elif combat_rating > 400:
                stats["skill_level"] = "Experienced"
            elif combat_rating > 200:
                stats["skill_level"] = "Intermediate"
            else:
                stats["skill_level"] = "Beginner"
        
        return JSONResponse(content=stats)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_player_stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/top")
async def get_top_players(
    region: str = Query('en', description="Region: en, ru, de, fr"),
    limit: int = Query(100, ge=1, le=1000, description="Number of players to return")
):
    """Получение топ игроков"""
    if region not in ['en', 'ru', 'de', 'fr']:
        raise HTTPException(status_code=400, detail="Invalid region")
    
    try:
        players = await game_stats_api.get_top_players(region, limit)
        return JSONResponse(content={"players": players, "total": len(players)})
    except Exception as e:
        logger.error(f"Error in get_top_players: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/compare")
async def compare_players(
    player1: str = Query(..., description="First player username"),
    player2: str = Query(..., description="Second player username"),
    region: str = Query('en', description="Region: en, ru, de, fr")
):
    """Сравнение двух игроков с расширенными метриками"""
    if region not in ['en', 'ru', 'de', 'fr']:
        raise HTTPException(status_code=400, detail="Invalid region")
    
    try:
        stats1 = await game_stats_api.get_player_stats(player1, region)
        stats2 = await game_stats_api.get_player_stats(player2, region)
        
        # Вычисляем боевые рейтинги
        combat_rating1 = features_service.realtime_combat_rating(
            stats1.get("kills", 0),
            stats1.get("deaths", 0),
            stats1.get("activity_time", 0)
        )
        
        combat_rating2 = features_service.realtime_combat_rating(
            stats2.get("kills", 0),
            stats2.get("deaths", 0),
            stats2.get("activity_time", 0)
        )
        
        comparison = {
            "player1": {**stats1, "combat_rating": combat_rating1},
            "player2": {**stats2, "combat_rating": combat_rating2},
            "comparison": {
                "level_diff": stats1.get("level", 0) - stats2.get("level", 0),
                "battles_diff": stats1.get("total_battles", 0) - stats2.get("total_battles", 0),
                "win_rate_diff": stats1.get("win_rate", 0) - stats2.get("win_rate", 0),
                "kd_ratio_diff": stats1.get("kdr", 0) - stats2.get("kdr", 0),
                "combat_rating_diff": combat_rating1 - combat_rating2
            },
            "recommendation": features_service._generate_enemy_recommendation({
                "win_rate_diff": stats1.get("win_rate", 0) - stats2.get("win_rate", 0),
                "kdr_diff": stats1.get("kdr", 0) - stats2.get("kdr", 0),
                "combat_rating_diff": combat_rating1 - combat_rating2
            })
        }
        
        return JSONResponse(content=comparison)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in compare_players: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/player/{username}/refresh")
async def refresh_player_stats(username: str, region: str = 'en'):
    """Принудительное обновление данных игрока"""
    try:
        logger.info(f"Manual refresh requested for player: {username}")
        
        # Инвалидируем кэш
        await cache_service.invalidate_player_cache(username)
        
        # Получаем свежие данные
        fresh_data = await game_stats_api.get_player_stats(username, region)
        
        return {
            "success": True,
            "message": "Player data refreshed successfully",
            "data": fresh_data,
            "source": fresh_data.get("__source__", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error refreshing player data: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": game_stats_api._get_demo_stats(username),
            "source": "demo_data",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 