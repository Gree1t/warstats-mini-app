#!/usr/bin/env python3
"""
War Thunder Statistics Telegram Bot
Интеграция с развернутым на Render backend API
"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL', 'https://warstats-backend-f6hw.onrender.com')
DEFAULT_REGION = 'en'

class WarThunderBot:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = httpx.AsyncClient(timeout=30.0)
    
    async def get_player_stats(self, username: str, region: str = DEFAULT_REGION) -> Optional[Dict[str, Any]]:
        """Получение статистики игрока с backend API"""
        try:
            url = f"{self.backend_url}/player/{username}"
            params = {'region': region}
            
            logger.info(f"Requesting stats for player: {username} in region: {region}")
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully received data for {username}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {username}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error getting stats for {username}: {e}")
            return None
    
    async def format_player_stats(self, data: Dict[str, Any]) -> str:
        """Форматирование статистики игрока для Telegram"""
        if not data:
            return "❌ Не удалось получить данные игрока"
        
        username = data.get('username', 'Unknown')
        general = data.get('general', {})
        vehicles = data.get('vehicles', {})
        profile = data.get('profile', {})
        
        # Основная статистика
        level = general.get('level', 0)
        total_battles = general.get('total_battles', 0)
        wins = general.get('wins', 0)
        losses = general.get('losses', 0)
        win_rate = general.get('win_rate', 0.0)
        kills = general.get('kills', 0)
        deaths = general.get('deaths', 0)
        kdr = general.get('kdr', 0.0)
        
        # Статистика по типам боев
        ground_battles = general.get('ground_battles', 0)
        air_battles = general.get('air_battles', 0)
        naval_battles = general.get('naval_battles', 0)
        
        # Топ техника
        top_vehicle = vehicles.get('top_vehicle', {})
        top_vehicle_name = top_vehicle.get('name', 'N/A')
        top_vehicle_battles = top_vehicle.get('battles', 0)
        
        # Профиль
        clan = profile.get('clan', 'Нет клана')
        last_online = profile.get('last_online', 'N/A')
        
        # Источник данных
        source = data.get('__source__', 'unknown')
        source_emoji = "🟢" if source != "demo_data" else "🟡"
        
        message = f"""
{source_emoji} **Статистика игрока: {username}**

📊 **Общая статистика:**
• Уровень: {level}
• Всего боев: {total_battles:,}
• Победы: {wins:,} | Поражения: {losses:,}
• Винрейт: {win_rate:.1%}
• Убийства: {kills:,} | Смерти: {deaths:,}
• K/D: {kdr:.2f}

🎯 **По типам боев:**
• Наземные: {ground_battles:,}
• Воздушные: {air_battles:,}
• Морские: {naval_battles:,}

🚗 **Топ техника:** {top_vehicle_name} ({top_vehicle_battles} боев)

👥 **Клан:** {clan}
🕐 **Последний онлайн:** {last_online}

📡 **Источник:** {source}
"""
        return message.strip()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        welcome_message = """
🎮 **War Thunder Statistics Bot**

Привет! Я помогу тебе получить статистику игроков War Thunder.

**Команды:**
• `/stats <имя_игрока>` - Получить статистику игрока
• `/compare <игрок1> <игрок2>` - Сравнить двух игроков
• `/top` - Топ игроков
• `/help` - Помощь

**Примеры:**
• `/stats PhlyDaily`
• `/compare PhlyDaily TheRussianBadger`
• `/stats PlayerName ru` (для русских серверов)

**Регионы:** en, ru, de, fr
"""
        
        keyboard = [
            [InlineKeyboardButton("📊 Получить статистику", callback_data="get_stats")],
            [InlineKeyboardButton("🏆 Топ игроков", callback_data="top_players")],
            [InlineKeyboardButton("🔍 Сравнить игроков", callback_data="compare_players")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stats"""
        if not context.args:
            await update.message.reply_text(
                "❌ Укажите имя игрока!\n"
                "Пример: `/stats PhlyDaily` или `/stats PlayerName ru`",
                parse_mode='Markdown'
            )
            return
        
        username = context.args[0].strip()
        region = context.args[1] if len(context.args) > 1 else DEFAULT_REGION
        
        if not username:
            await update.message.reply_text("❌ Имя игрока не может быть пустым!")
            return
        
        # Отправляем сообщение о загрузке
        loading_msg = await update.message.reply_text(f"🔍 Загружаю статистику для {username}...")
        
        try:
            # Получаем данные
            data = await self.get_player_stats(username, region)
            
            if data:
                # Форматируем и отправляем статистику
                stats_message = await self.format_player_stats(data)
                await loading_msg.edit_text(stats_message, parse_mode='Markdown')
            else:
                await loading_msg.edit_text(
                    f"❌ Не удалось получить статистику для {username}\n"
                    "Проверьте правильность имени игрока и попробуйте снова."
                )
                
        except Exception as e:
            logger.error(f"Error in stats command: {e}")
            await loading_msg.edit_text(
                f"❌ Ошибка при получении статистики для {username}\n"
                "Попробуйте позже или обратитесь к администратору."
            )
    
    async def compare_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /compare"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ Укажите двух игроков для сравнения!\n"
                "Пример: `/compare Player1 Player2`",
                parse_mode='Markdown'
            )
            return
        
        player1 = context.args[0].strip()
        player2 = context.args[1].strip()
        region = context.args[2] if len(context.args) > 2 else DEFAULT_REGION
        
        if not player1 or not player2:
            await update.message.reply_text("❌ Имена игроков не могут быть пустыми!")
            return
        
        # Отправляем сообщение о загрузке
        loading_msg = await update.message.reply_text(f"🔍 Сравниваю {player1} и {player2}...")
        
        try:
            # Получаем данные для обоих игроков
            data1 = await self.get_player_stats(player1, region)
            data2 = await self.get_player_stats(player2, region)
            
            if data1 and data2:
                # Форматируем сравнение
                comparison = await self.format_comparison(data1, data2)
                await loading_msg.edit_text(comparison, parse_mode='Markdown')
            else:
                await loading_msg.edit_text(
                    f"❌ Не удалось получить данные для сравнения\n"
                    f"Проверьте правильность имен игроков."
                )
                
        except Exception as e:
            logger.error(f"Error in compare command: {e}")
            await loading_msg.edit_text(
                f"❌ Ошибка при сравнении игроков\n"
                "Попробуйте позже или обратитесь к администратору."
            )
    
    async def format_comparison(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
        """Форматирование сравнения двух игроков"""
        p1_name = data1.get('username', 'Player1')
        p2_name = data2.get('username', 'Player2')
        
        p1_general = data1.get('general', {})
        p2_general = data2.get('general', {})
        
        # Извлекаем данные для сравнения
        p1_level = p1_general.get('level', 0)
        p2_level = p2_general.get('level', 0)
        
        p1_winrate = p1_general.get('win_rate', 0.0)
        p2_winrate = p2_general.get('win_rate', 0.0)
        
        p1_kdr = p1_general.get('kdr', 0.0)
        p2_kdr = p2_general.get('kdr', 0.0)
        
        p1_battles = p1_general.get('total_battles', 0)
        p2_battles = p2_general.get('total_battles', 0)
        
        p1_kills = p1_general.get('kills', 0)
        p2_kills = p2_general.get('kills', 0)
        
        # Определяем победителей
        level_winner = "🟢" if p1_level > p2_level else "🔴" if p1_level < p2_level else "🟡"
        winrate_winner = "🟢" if p1_winrate > p2_winrate else "🔴" if p1_winrate < p2_winrate else "🟡"
        kdr_winner = "🟢" if p1_kdr > p2_kdr else "🔴" if p1_kdr < p2_kdr else "🟡"
        battles_winner = "🟢" if p1_battles > p2_battles else "🔴" if p1_battles < p2_battles else "🟡"
        kills_winner = "🟢" if p1_kills > p2_kills else "🔴" if p1_kills < p2_kills else "🟡"
        
        comparison = f"""
⚔️ **Сравнение игроков**

👤 **{p1_name}** vs 👤 **{p2_name}**

📊 **Уровень:** {level_winner} {p1_level} vs {p2_level}
🏆 **Винрейт:** {winrate_winner} {p1_winrate:.1%} vs {p2_winrate:.1%}
🎯 **K/D:** {kdr_winner} {p1_kdr:.2f} vs {p2_kdr:.2f}
⚔️ **Бои:** {battles_winner} {p1_battles:,} vs {p2_battles:,}
💀 **Убийства:** {kills_winner} {p1_kills:,} vs {p2_kills:,}

🟢 = Лучше | 🔴 = Хуже | 🟡 = Равно
"""
        return comparison.strip()
    
    async def top_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /top"""
        region = context.args[0] if context.args else DEFAULT_REGION
        limit = min(int(context.args[1]) if len(context.args) > 1 else 10, 50)
        
        loading_msg = await update.message.reply_text(f"🏆 Загружаю топ {limit} игроков...")
        
        try:
            url = f"{self.backend_url}/top"
            params = {'region': region, 'limit': limit}
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data and isinstance(data, list):
                top_message = f"🏆 **Топ {len(data)} игроков** (регион: {region})\n\n"
                
                for i, player in enumerate(data[:10], 1):  # Показываем только топ 10
                    username = player.get('username', 'Unknown')
                    level = player.get('level', 0)
                    winrate = player.get('win_rate', 0.0)
                    kdr = player.get('kdr', 0.0)
                    
                    top_message += f"{i}. **{username}**\n"
                    top_message += f"   Уровень: {level} | Винрейт: {winrate:.1%} | K/D: {kdr:.2f}\n\n"
                
                await loading_msg.edit_text(top_message, parse_mode='Markdown')
            else:
                await loading_msg.edit_text("❌ Не удалось получить топ игроков")
                
        except Exception as e:
            logger.error(f"Error in top command: {e}")
            await loading_msg.edit_text("❌ Ошибка при получении топ игроков")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
❓ **Помощь по командам**

📊 **Получить статистику:**
`/stats <имя_игрока> [регион]`
Пример: `/stats PhlyDaily` или `/stats PlayerName ru`

⚔️ **Сравнить игроков:**
`/compare <игрок1> <игрок2> [регион]`
Пример: `/compare Player1 Player2`

🏆 **Топ игроков:**
`/top [регион] [количество]`
Пример: `/top en 20`

🌍 **Доступные регионы:**
• `en` - Международный (по умолчанию)
• `ru` - Русский
• `de` - Немецкий
• `fr` - Французский

📡 **Источники данных:**
• 🟢 Реальные данные с серверов WT
• 🟡 Демо-данные (если реальные недоступны)

💡 **Советы:**
• Используйте точное имя игрока
• Проверьте регион сервера
• При ошибках попробуйте позже
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "get_stats":
            await query.edit_message_text(
                "📊 **Получить статистику**\n\n"
                "Отправьте команду:\n"
                "`/stats <имя_игрока>`\n\n"
                "Пример: `/stats PhlyDaily`",
                parse_mode='Markdown'
            )
        elif query.data == "top_players":
            await query.edit_message_text(
                "🏆 **Топ игроков**\n\n"
                "Отправьте команду:\n"
                "`/top [регион] [количество]`\n\n"
                "Пример: `/top en 20`",
                parse_mode='Markdown'
            )
        elif query.data == "compare_players":
            await query.edit_message_text(
                "⚔️ **Сравнить игроков**\n\n"
                "Отправьте команду:\n"
                "`/compare <игрок1> <игрок2>`\n\n"
                "Пример: `/compare Player1 Player2`",
                parse_mode='Markdown'
            )
        elif query.data == "help":
            await self.help_command(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ошибок"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка при обработке запроса.\n"
                "Попробуйте позже или обратитесь к администратору."
            )

async def main():
    """Основная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    bot = WarThunderBot()
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CommandHandler("compare", bot.compare_command))
    application.add_handler(CommandHandler("top", bot.top_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    
    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(bot.error_handler)
    
    # Запускаем бота
    logger.info("Starting War Thunder Statistics Bot...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main()) 