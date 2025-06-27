"""
GameStats API
Универсальная платформа игровой статистики
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

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем FastAPI приложение
app = FastAPI(
    title="GameStats API",
    description="Universal gaming statistics platform API",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Кэш для данных
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
        """Возвращает демо-данные для игрока"""
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
        """Получение статистики игрока с кэшированием"""
        cache_key = f"{username}_{region}"
        
        # Проверяем кэш
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < 300:  # 5 минут кэш
                logger.info(f"Returning cached data for {username}")
                return cached_data
        
        logger.info(f"Fetching stats for player: {username} in region: {region} [Local Flask API]")
        
        try:
            # Пытаемся получить данные от локального Flask API
            real_data = await self._fetch_from_local_api(username, region)
            if real_data and not real_data.get('error'):
                transformed_data = self._transform_local_api_data(real_data)
                if transformed_data:
                    cache[cache_key] = (transformed_data, time.time())
                    return transformed_data
            
            logger.warning(f"No valid data found for player {username}, using demo data")
            demo_data = self._get_demo_stats(username)
            cache[cache_key] = (demo_data, time.time())
            return demo_data
            
        except Exception as e:
            logger.warning(f"Background fetch failed for {username}: {e}")
            demo_data = self._get_demo_stats(username)
            cache[cache_key] = (demo_data, time.time())
            return demo_data

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
            raise
    
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
        """Получение топ игроков (демо-данные)"""
        cache_key = f"top_{region}_{limit}"
        
        # Проверяем кэш
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < 600:  # 10 минут кэш
                return cached_data
        
        try:
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
            cache[cache_key] = (top_players, time.time())
            
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

@app.on_event("shutdown")
async def shutdown_event():
    """Закрытие соединений при выключении"""
    await game_stats_api.close()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "GameStats API - Universal Gaming Statistics Platform",
        "version": "1.0.0",
        "endpoints": {
            "/player/{username}": "Get player statistics",
            "/top": "Get top players",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/player/{username}")
async def get_player_stats(
    username: str,
    region: str = Query('en', description="Region: en, ru, de, fr")
):
    """Получение статистики игрока"""
    if region not in ['en', 'ru', 'de', 'fr']:
        raise HTTPException(status_code=400, detail="Invalid region")
    
    try:
        stats = await game_stats_api.get_player_stats(username, region)
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
    """Сравнение двух игроков"""
    if region not in ['en', 'ru', 'de', 'fr']:
        raise HTTPException(status_code=400, detail="Invalid region")
    
    try:
        stats1 = await game_stats_api.get_player_stats(player1, region)
        stats2 = await game_stats_api.get_player_stats(player2, region)
        
        comparison = {
            "player1": stats1,
            "player2": stats2,
            "comparison": {
                "level_diff": stats1["general"]["level"] - stats2["general"]["level"],
                "battles_diff": stats1["general"]["total_battles"] - stats2["general"]["total_battles"],
                "win_rate_diff": stats1["general"]["win_rate"] - stats2["general"]["win_rate"],
                "kd_ratio_diff": stats1["general"]["kdr"] - stats2["general"]["kdr"]
            }
        }
        
        return JSONResponse(content=comparison)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in compare_players: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/player/{username}/refresh")
async def refresh_player_stats(username: str, region: str = 'en'):
    """Принудительное обновление данных игрока через локальный API"""
    try:
        logger.info(f"Manual refresh requested for player: {username}")
        
        # Очищаем кэш для этого игрока
        cache_key = f"{username}_{region}"
        if cache_key in cache:
            del cache[cache_key]
        
        # Пытаемся получить реальные данные
        real_data = await game_stats_api._fetch_from_local_api(username, region)
        if real_data and not real_data.get('error'):
            transformed_data = game_stats_api._transform_local_api_data(real_data)
            if transformed_data:
                cache[cache_key] = (transformed_data, time.time())
                return {
                    "success": True,
                    "message": "Real data updated successfully",
                    "data": transformed_data,
                    "source": "local_flask_api"
                }
        
        # Если не удалось, возвращаем демо-данные
        demo_data = game_stats_api._get_demo_stats(username)
        cache[cache_key] = (demo_data, time.time())
        return {
            "success": False,
            "message": "Using demo data (local API unavailable)",
            "data": demo_data,
            "source": "demo_data"
        }
        
    except Exception as e:
        logger.error(f"Error refreshing player data: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": game_stats_api._get_demo_stats(username),
            "source": "demo_data"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 