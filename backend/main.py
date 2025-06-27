"""
GameStats API
Универсальная платформа игровой статистики
"""

import os
import time
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем FastAPI приложение
app = FastAPI(
    title="GameStats API",
    description="Универсальная платформа игровой статистики",
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
        self.base_urls = {
            'en': 'https://gamestats.com/en/community/userinfo',
            'ru': 'https://gamestats.com/ru/community/userinfo'
        }
    
    def _get_demo_stats(self, username: str) -> Dict[str, Any]:
        """Генерирует демо-данные для игрока"""
        return {
            "username": username,
            "level": 85,
            "clan": {
                "name": "THUNDER",
                "tag": "THD",
                "role": "Member",
                "member_since": "2021-01-15",
                "clan_level": 25
            },
            "general": {
                "level": 85,
                "total_battles": 15420,
                "win_rate": 68.6,
                "total_kills": 67890,
                "total_deaths": 15420,
                "kd_ratio": 4.41,
                "total_score": 1250000,
                "premium": True,
                "registration_date": "2020-03-15",
                "last_online": "2024-06-27"
            },
            "aviation": {
                "battles": 8920,
                "wins": 6120,
                "losses": 2800,
                "win_rate": 68.6,
                "kills": 45670,
                "deaths": 8920,
                "kd_ratio": 5.12,
                "air_kills": 34560,
                "ground_kills": 11110,
                "bombing_kills": 2340,
                "accuracy": 78.5
            },
            "tanks": {
                "battles": 4560,
                "wins": 3120,
                "losses": 1440,
                "win_rate": 68.4,
                "kills": 15670,
                "deaths": 4560,
                "kd_ratio": 3.44,
                "ground_kills": 12340,
                "air_kills": 3330,
                "capture_points": 890,
                "accuracy": 72.3
            },
            "fleet": {
                "battles": 1940,
                "wins": 1340,
                "losses": 600,
                "win_rate": 69.1,
                "kills": 6550,
                "deaths": 1940,
                "kd_ratio": 3.38,
                "ship_kills": 5230,
                "air_kills": 1320,
                "torpedo_kills": 890,
                "accuracy": 65.8
            },
            "achievements": [
                {
                    "name": "Ace",
                    "description": "Destroy 5 enemy aircraft in one battle",
                    "icon": "🏆",
                    "unlocked": True
                },
                {
                    "name": "Tank Ace",
                    "description": "Destroy 5 enemy tanks in one battle",
                    "icon": "🛡️",
                    "unlocked": True
                },
                {
                    "name": "Victory",
                    "description": "Win 100 battles",
                    "icon": "🎖️",
                    "unlocked": True
                }
            ],
            "charts": {
                "performance_over_time": [],
                "vehicle_usage": [],
                "nation_stats": []
            },
            "top_vehicles": [
                {
                    "name": "F-16 Fighting Falcon",
                    "type": "air",
                    "battles": 1247,
                    "icon": "https://static.gamestats.com/upload/image/aircraft/f16.png"
                },
                {
                    "name": "M1A2 Abrams",
                    "type": "ground",
                    "battles": 892,
                    "icon": "https://static.gamestats.com/upload/image/tanks/m1a2.png"
                },
                {
                    "name": "USS Iowa",
                    "type": "fleet",
                    "battles": 456,
                    "icon": "https://static.gamestats.com/upload/image/ships/iowa.png"
                }
            ]
        }
    
    async def get_player_stats(self, username: str, region: str = 'en') -> Dict[str, Any]:
        """Получение статистики игрока"""
        cache_key = f"{username}_{region}"
        
        # Проверяем кэш
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < CACHE_DURATION:
                return cached_data
        
        # Сначала возвращаем демо-данные для быстрого ответа
        demo_data = self._get_demo_stats(username)
        
        # В фоне пытаемся получить реальные данные
        try:
            logger.info(f"Background fetch for player: {username} in region: {region}")
            real_data = await self._fetch_from_local_api(username, region)
            if real_data and not real_data.get('error'):
                # Преобразуем формат данных для совместимости
                transformed_data = self._transform_local_api_data(real_data)
                if transformed_data:
                    cache[cache_key] = (transformed_data, time.time())
                    return transformed_data
        except Exception as e:
            logger.warning(f"Background fetch failed for {username}: {e}")
        
        # Возвращаем демо-данные
        cache[cache_key] = (demo_data, time.time())
        return demo_data
    
    async def _fetch_from_local_api(self, username: str, region: str) -> Optional[Dict[str, Any]]:
        """Получение данных от локального Flask API"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"http://localhost:8080/profile", params={
                    "username": username,
                    "region": region
                })
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Local API request failed: {response.status_code}")
                    return None
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

# Создаем экземпляр API
wt_api = GameStatsAPI()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "GameStats API",
        "version": "1.0.0",
        "description": "Универсальная платформа игровой статистики"
    }

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/player/{username}")
async def get_player_stats(username: str, region: str = Query('en', description="Регион игрока")):
    """Получить статистику игрока"""
    try:
        stats = await wt_api.get_player_stats(username, region)
        return stats
    except Exception as e:
        logger.error(f"Error fetching player data for {username}: {str(e)}")
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
        real_data = await wt_api._fetch_from_local_api(username, region)
        if real_data and not real_data.get('error'):
            transformed_data = wt_api._transform_local_api_data(real_data)
            if transformed_data:
                cache[cache_key] = (transformed_data, time.time())
                return {
                    "success": True,
                    "message": "Real data updated successfully",
                    "data": transformed_data,
                    "source": "local_flask_api"
                }
        
        # Если не удалось, возвращаем демо-данные
        demo_data = wt_api._get_demo_stats(username)
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
            "data": wt_api._get_demo_stats(username),
            "source": "demo_data"
        }

if __name__ == "__main__":
    import uvicorn
    def _parse_player_page(self, soup: BeautifulSoup, username: str) -> Dict[str, Any]:
        """Парсинг страницы игрока"""
        stats = {
            "username": username,
            "general": {},
            "aviation": {},
            "tanks": {},
            "fleet": {},
            "achievements": [],
            "clan": {},
            "charts": {},
            "top_vehicles": []
        }
        
        try:
            # Общая информация
            stats["general"] = self._parse_general_stats(soup)
            
            # Статистика авиации
            stats["aviation"] = self._parse_aviation_stats(soup)
            
            # Статистика танков
            stats["tanks"] = self._parse_tank_stats(soup)
            
            # Статистика флота
            stats["fleet"] = self._parse_fleet_stats(soup)
            
            # Достижения
            stats["achievements"] = self._parse_achievements(soup)
            
            # Клан
            stats["clan"] = self._parse_clan_info(soup)
            
            # Графики
            stats["charts"] = self._parse_charts(soup)
            
            # Топовая техника
            stats["top_vehicles"] = self._parse_top_vehicles(soup)
            
        except Exception as e:
            logger.error(f"Error parsing player page: {e}")
        
        return stats
    
    def _parse_general_stats(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг общей статистики"""
        general = {
            "level": 0,
            "total_battles": 0,
            "win_rate": 0.0,
            "total_kills": 0,
            "total_deaths": 0,
            "kd_ratio": 0.0,
            "total_score": 0,
            "premium": False,
            "registration_date": "",
            "last_online": ""
        }
        
        try:
            # Уровень
            level_elem = soup.find('span', class_='level')
            if level_elem and level_elem.text:
                general["level"] = int(level_elem.text.strip())
            
            # Общие бои
            battles_elem = soup.find('div', string=re.compile(r'Total battles', re.I))
            if battles_elem:
                battles_text_elem = battles_elem.find_next('div')
                if battles_text_elem and battles_text_elem.text:
                    general["total_battles"] = int(re.sub(r'[^\d]', '', battles_text_elem.text.strip()) or 0)
            
            # Винрейт
            winrate_elem = soup.find('div', string=re.compile(r'Victories', re.I))
            if winrate_elem:
                winrate_text_elem = winrate_elem.find_next('div')
                if winrate_text_elem and winrate_text_elem.text:
                    general["win_rate"] = float(re.sub(r'[^\d.]', '', winrate_text_elem.text.strip()) or 0)
            
            # K/D
            kd_elem = soup.find('div', string=re.compile(r'K/D', re.I))
            if kd_elem:
                kd_text_elem = kd_elem.find_next('div')
                if kd_text_elem and kd_text_elem.text:
                    general["kd_ratio"] = float(re.sub(r'[^\d.]', '', kd_text_elem.text.strip()) or 0)
            
        except Exception as e:
            logger.error(f"Error parsing general stats: {e}")
        
        return general
    
    def _parse_aviation_stats(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг статистики авиации"""
        aviation = {
            "battles": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "kills": 0,
            "deaths": 0,
            "kd_ratio": 0.0,
            "air_kills": 0,
            "ground_kills": 0,
            "bombing_kills": 0,
            "accuracy": 0.0
        }
        
        try:
            # Ищем секцию авиации
            aviation_section = soup.find('div', string=re.compile(r'Aviation', re.I))
            if aviation_section:
                section = aviation_section.find_parent('div')
                if section:
                    # Бои
                    battles_elem = section.find('div', string=re.compile(r'Battles', re.I))
                    if battles_elem:
                        battles_text_elem = battles_elem.find_next('div')
                        if battles_text_elem and battles_text_elem.text:
                            aviation["battles"] = int(re.sub(r'[^\d]', '', battles_text_elem.text.strip()) or 0)
                    
                    # Убийства
                    kills_elem = section.find('div', string=re.compile(r'Kills', re.I))
                    if kills_elem:
                        kills_text_elem = kills_elem.find_next('div')
                        if kills_text_elem and kills_text_elem.text:
                            aviation["kills"] = int(re.sub(r'[^\d]', '', kills_text_elem.text.strip()) or 0)
                    
                    # Смерти
                    deaths_elem = section.find('div', string=re.compile(r'Deaths', re.I))
                    if deaths_elem:
                        deaths_text_elem = deaths_elem.find_next('div')
                        if deaths_text_elem and deaths_text_elem.text:
                            aviation["deaths"] = int(re.sub(r'[^\d]', '', deaths_text_elem.text.strip()) or 0)
                    
                    if aviation["deaths"] > 0:
                        aviation["kd_ratio"] = round(aviation["kills"] / aviation["deaths"], 2)
                    
                    if aviation["battles"] > 0:
                        aviation["win_rate"] = round((aviation["wins"] / aviation["battles"]) * 100, 1)
        
        except Exception as e:
            logger.error(f"Error parsing aviation stats: {e}")
        
        return aviation
    
    def _parse_tank_stats(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг статистики танков"""
        tanks = {
            "battles": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "kills": 0,
            "deaths": 0,
            "kd_ratio": 0.0,
            "ground_kills": 0,
            "air_kills": 0,
            "capture_points": 0,
            "accuracy": 0.0
        }
        
        try:
            # Ищем секцию танков
            tanks_section = soup.find('div', string=re.compile(r'Ground Forces', re.I))
            if tanks_section:
                section = tanks_section.find_parent('div')
                if section:
                    # Бои
                    battles_elem = section.find('div', string=re.compile(r'Battles', re.I))
                    if battles_elem:
                        battles_text_elem = battles_elem.find_next('div')
                        if battles_text_elem and battles_text_elem.text:
                            tanks["battles"] = int(re.sub(r'[^\d]', '', battles_text_elem.text.strip()) or 0)
                    
                    # Убийства
                    kills_elem = section.find('div', string=re.compile(r'Kills', re.I))
                    if kills_elem:
                        kills_text_elem = kills_elem.find_next('div')
                        if kills_text_elem and kills_text_elem.text:
                            tanks["kills"] = int(re.sub(r'[^\d]', '', kills_text_elem.text.strip()) or 0)
                    
                    # Смерти
                    deaths_elem = section.find('div', string=re.compile(r'Deaths', re.I))
                    if deaths_elem:
                        deaths_text_elem = deaths_elem.find_next('div')
                        if deaths_text_elem and deaths_text_elem.text:
                            tanks["deaths"] = int(re.sub(r'[^\d]', '', deaths_text_elem.text.strip()) or 0)
                    
                    if tanks["deaths"] > 0:
                        tanks["kd_ratio"] = round(tanks["kills"] / tanks["deaths"], 2)
                    
                    if tanks["battles"] > 0:
                        tanks["win_rate"] = round((tanks["wins"] / tanks["battles"]) * 100, 1)
        
        except Exception as e:
            logger.error(f"Error parsing tank stats: {e}")
        
        return tanks
    
    def _parse_fleet_stats(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг статистики флота"""
        fleet = {
            "battles": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "kills": 0,
            "deaths": 0,
            "kd_ratio": 0.0,
            "ship_kills": 0,
            "air_kills": 0,
            "torpedo_kills": 0,
            "accuracy": 0.0
        }
        
        try:
            # Ищем секцию флота
            fleet_section = soup.find('div', string=re.compile(r'Fleet', re.I))
            if fleet_section:
                section = fleet_section.find_parent('div')
                if section:
                    # Бои
                    battles_elem = section.find('div', string=re.compile(r'Battles', re.I))
                    if battles_elem:
                        battles_text_elem = battles_elem.find_next('div')
                        if battles_text_elem and battles_text_elem.text:
                            fleet["battles"] = int(re.sub(r'[^\d]', '', battles_text_elem.text.strip()) or 0)
                    
                    # Убийства
                    kills_elem = section.find('div', string=re.compile(r'Kills', re.I))
                    if kills_elem:
                        kills_text_elem = kills_elem.find_next('div')
                        if kills_text_elem and kills_text_elem.text:
                            fleet["kills"] = int(re.sub(r'[^\d]', '', kills_text_elem.text.strip()) or 0)
                    
                    # Смерти
                    deaths_elem = section.find('div', string=re.compile(r'Deaths', re.I))
                    if deaths_elem:
                        deaths_text_elem = deaths_elem.find_next('div')
                        if deaths_text_elem and deaths_text_elem.text:
                            fleet["deaths"] = int(re.sub(r'[^\d]', '', deaths_text_elem.text.strip()) or 0)
                    
                    if fleet["deaths"] > 0:
                        fleet["kd_ratio"] = round(fleet["kills"] / fleet["deaths"], 2)
                    
                    if fleet["battles"] > 0:
                        fleet["win_rate"] = round((fleet["wins"] / fleet["battles"]) * 100, 1)
        
        except Exception as e:
            logger.error(f"Error parsing fleet stats: {e}")
        
        return fleet
    
    def _parse_achievements(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Парсинг достижений"""
        achievements = []
        
        try:
            # Ищем секцию достижений
            achievements_section = soup.find('div', string=re.compile(r'Achievements', re.I))
            if achievements_section and hasattr(achievements_section, 'find_all'):
                achievement_items = achievements_section.find_all('div', attrs={'class': 'achievement'})
                for item in achievement_items[:10]:  # Ограничиваем 10 достижениями
                    achievement = {
                        "name": item.get('title', ''),
                        "description": item.get('data-description', ''),
                        "icon": item.find('img')['src'] if item.find('img') else '',
                        "unlocked": True
                    }
                    achievements.append(achievement)
        
        except Exception as e:
            logger.error(f"Error parsing achievements: {e}")
        
        return achievements
    
    def _parse_clan_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг информации о клане"""
        clan = {
            "name": "",
            "tag": "",
            "role": "",
            "member_since": "",
            "clan_level": 0
        }
        
        try:
            # Ищем информацию о клане
            clan_elem = soup.find('div', class_='clan-info')
            if clan_elem:
                clan_name = clan_elem.find('div', class_='clan-name')
                if clan_name:
                    clan["name"] = clan_name.text.strip()
                
                clan_tag = clan_elem.find('div', class_='clan-tag')
                if clan_tag:
                    clan["tag"] = clan_tag.text.strip()
        
        except Exception as e:
            logger.error(f"Error parsing clan info: {e}")
        
        return clan
    
    def _parse_charts(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Парсинг графиков"""
        charts = {
            "performance_over_time": [],
            "vehicle_usage": [],
            "nation_stats": []
        }
        
        try:
            # Здесь можно добавить парсинг графиков, если они есть на странице
            # Пока возвращаем пустые данные
            pass
        
        except Exception as e:
            logger.error(f"Error parsing charts: {e}")
        
        return charts
    
    def _parse_top_vehicles(self, soup: BeautifulSoup) -> list:
        """Парсинг топовой техники игрока (заглушка, если нет данных)"""
        # TODO: Реализовать реальный парсинг, если появится список техники на странице
        # Сейчас возвращаем примерные данные для фронта
        return [
            {"name": "F-16 Fighting Falcon", "type": "air", "battles": 1247, "icon": "https://static.warthunder.com/upload/image/aircraft/f16.png"},
            {"name": "M1A2 Abrams", "type": "ground", "battles": 892, "icon": "https://static.warthunder.com/upload/image/tanks/m1a2.png"},
            {"name": "USS Iowa", "type": "fleet", "battles": 456, "icon": "https://static.warthunder.com/upload/image/ships/iowa.png"}
        ]
    
    async def get_top_players(self, region: str = 'en', limit: int = 100) -> List[Dict[str, Any]]:
        """Получение топ игроков"""
        cache_key = f"top_players_{region}_{limit}"
        
        # Проверяем кэш
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < CACHE_DURATION:
                return cached_data
        
        try:
            # Здесь можно добавить парсинг топ игроков
            # Пока возвращаем демо данные
            top_players = []
            for i in range(min(limit, 10)):
                player = {
                    "rank": i + 1,
                    "username": f"TopPlayer{i+1}",
                    "level": 100 - i * 5,
                    "total_battles": 10000 - i * 500,
                    "win_rate": 65.0 - i * 2,
                    "kd_ratio": 3.5 - i * 0.2,
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
        await self.session.aclose()

    async def _fetch_from_local_api(self, username: str, region: str) -> Dict[str, Any]:
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

# Создаем экземпляр API
wt_api = WarThunderAPI()

@app.on_event("shutdown")
async def shutdown_event():
    """Закрытие соединений при выключении"""
    await wt_api.close()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "War Thunder Stats API",
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
        stats = await wt_api.get_player_stats(username, region)
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
        players = await wt_api.get_top_players(region, limit)
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
        stats1 = await wt_api.get_player_stats(player1, region)
        stats2 = await wt_api.get_player_stats(player2, region)
        
        comparison = {
            "player1": stats1,
            "player2": stats2,
            "comparison": {
                "level_diff": stats1["general"]["level"] - stats2["general"]["level"],
                "battles_diff": stats1["general"]["total_battles"] - stats2["general"]["total_battles"],
                "win_rate_diff": stats1["general"]["win_rate"] - stats2["general"]["win_rate"],
                "kd_ratio_diff": stats1["general"]["kd_ratio"] - stats2["general"]["kd_ratio"]
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
        real_data = await wt_api._fetch_from_local_api(username, region)
        if real_data and not real_data.get('error'):
            transformed_data = wt_api._transform_local_api_data(real_data)
            if transformed_data:
                cache[cache_key] = (transformed_data, time.time())
                return {
                    "success": True,
                    "message": "Real data updated successfully",
                    "data": transformed_data,
                    "source": "local_flask_api"
                }
        
        # Если не удалось, возвращаем демо-данные
        demo_data = wt_api._get_demo_stats(username)
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
            "data": wt_api._get_demo_stats(username),
            "source": "demo_data"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 