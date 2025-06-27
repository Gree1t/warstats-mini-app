#!/usr/bin/env python3
"""
GameStats Telegram Bot
Универсальная платформа игровой статистики
"""

import asyncio
import logging
import os
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import httpx

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(s)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'your-bot-token-here')
BACKEND_URL = os.getenv('BACKEND_URL', 'https://gamestats-backend.onrender.com')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://gamestats-mini-app.netlify.app')

class GameStatsBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("find", self.find_command))
        self.application.add_handler(CommandHandler("top", self.top_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        
        # Обработка callback запросов
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработка сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        if not update.effective_user or not update.message:
            return
            
        user = update.effective_user
        
        # Приветственное сообщение с кнопкой открытия Mini App
        welcome_text = f"""
🎮 Добро пожаловать в **GameStats**!

Ваша универсальная платформа игровой статистики.

🚀 **Что умеет приложение:**
• 🔍 Поиск игроков по никнейму
• 📊 Детальная статистика (авиация, танки, флот)
• 🏅 Система достижений
• 📈 Сравнение режимов игры
• 🌙 Современный дизайн

Нажмите кнопку ниже, чтобы открыть приложение:
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "🎮 Открыть GameStats", 
                web_app=WebAppInfo(url=MINI_APP_URL)
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        if not update.message:
            return
            
        help_text = """
📚 **Справка по командам:**

🎮 `/start` - Запустить приложение
🔍 `/find <никнейм>` - Быстрый поиск игрока
📊 `/stats` - Открыть статистику
🏆 `/top` - Топ игроков
⚙️ `/settings` - Настройки

💡 **Советы:**
• Используйте кнопку "Открыть приложение" для полного доступа
• В приложении можно искать игроков, просматривать детальную статистику
• Поддерживается темная и светлая тема
• Можно делиться статистикой с друзьями

🆘 **Нужна помощь?** Обратитесь к @admin
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "🎮 Открыть приложение", 
                web_app=WebAppInfo(url=MINI_APP_URL)
            )],
            [InlineKeyboardButton("📞 Поддержка", url="https://t.me/admin")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stats"""
        if not update.message:
            return
            
        stats_text = """
📊 **Статистика GameStats**

Выберите, что хотите посмотреть:

🔍 **Поиск игрока** - найти конкретного игрока
🏆 **Топ игроков** - лучшие игроки
📈 **Общая статистика** - общая информация
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "🔍 Поиск игрока", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=search")
            )],
            [InlineKeyboardButton(
                "🏆 Топ игроков", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=top")
            )],
            [InlineKeyboardButton(
                "📊 Общая статистика", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=stats")
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def find_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /find"""
        if not update.message:
            return
            
        if not context.args:
            await update.message.reply_text(
                "🔍 **Использование:** `/find <никнейм>`\n\n"
                "Пример: `/find JohnDoe`",
                parse_mode='Markdown'
            )
            return
        
        player_name = " ".join(context.args)
        api_url = f"http://localhost:8080/profile?username={player_name}&region=en"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(api_url, timeout=30)
                data = resp.json()
            msg = f"\n".join([
                f"👤 Игрок: {data.get('username')}",
                f"🏅 Уровень: {data.get('level') if data.get('level') is not None else 'N/A'}",
                # Добавь другие поля по желанию
            ])
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при получении данных: {e}")
    
    async def top_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /top"""
        if not update.message:
            return
            
        top_text = """
🏆 **Топ игроков GameStats**

Выберите категорию:

👑 **Топ по победам** - лучшие по количеству побед
🎯 **Топ по K/D** - лучшие по соотношению убийств/смертей
⏱️ **Топ по времени** - самые активные игроки
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "👑 Топ по победам", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=top&category=wins")
            )],
            [InlineKeyboardButton(
                "🎯 Топ по K/D", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=top&category=kd")
            )],
            [InlineKeyboardButton(
                "⏱️ Топ по времени", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=top&category=time")
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            top_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /settings"""
        if not update.message:
            return
            
        settings_text = """
⚙️ **Настройки**

Выберите, что хотите настроить:

🌙 **Тема** - светлая или темная
🌍 **Язык** - русский, английский, немецкий, французский
🔔 **Уведомления** - включить/выключить
📊 **Автообновление** - частота обновления статистики
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "⚙️ Открыть настройки", 
                web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=settings")
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            settings_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на inline кнопки"""
        if not update.callback_query:
            return
            
        query = update.callback_query
        await query.answer()
        
        # Здесь можно добавить логику для разных кнопок
        if query.data == "open_app":
            await query.edit_message_text(
                "🎮 Открываю приложение...\n\n"
                "Если приложение не открылось, нажмите кнопку еще раз.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        "🎮 Открыть приложение", 
                        web_app=WebAppInfo(url=MINI_APP_URL)
                    )
                ]])
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        if not update.message or not update.message.text:
            return
            
        text = update.message.text
        
        # Если сообщение похоже на никнейм, предлагаем поиск
        if text and len(text) >= 3 and len(text) <= 20 and text.replace('_', '').replace('-', '').isalnum():
            keyboard = [
                [InlineKeyboardButton(
                    f"🔍 Найти {text}", 
                    web_app=WebAppInfo(url=f"{MINI_APP_URL}?action=search&player={text}")
                )]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"🔍 Найдено возможное имя игрока: **{text}**\n\n"
                "Нажмите кнопку ниже, чтобы найти статистику:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            # Общий ответ с предложением открыть приложение
            keyboard = [
                [InlineKeyboardButton(
                    "🎮 Открыть приложение", 
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "💬 Не понимаю ваше сообщение.\n\n"
                "Используйте команды или откройте приложение для поиска игроков:",
                reply_markup=reply_markup
            )
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ошибок"""
        logger.error(f"Exception while handling an update: {context.error}")
        # Просто логируем ошибку без отправки сообщения пользователю
    
    def run(self):
        """Запуск бота"""
        # Добавляем обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        logger.info("Starting GameStats bot...")
        
        # Запускаем бота
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

def main():
    """Главная функция"""
    bot = GameStatsBot()
    bot.run()

if __name__ == "__main__":
    main() 