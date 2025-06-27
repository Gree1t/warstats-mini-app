# 🎮 GameStats - Универсальная платформа игровой статистики

Современная платформа для отслеживания игровой статистики с Telegram ботом и веб-приложением.

## ✨ Возможности

- 🤖 **Telegram Bot** - быстрый доступ к статистике через чат
- 📱 **Mini App** - полнофункциональное веб-приложение в Telegram
- 🔄 **Real-time данные** - актуальная статистика в реальном времени
- 📊 **Детальная аналитика** - подробная статистика по всем аспектам игры
- 🎯 **Умный поиск** - быстрый поиск игроков по никнейму
- 🌐 **API** - RESTful API для интеграции с другими сервисами

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.8+
- Node.js 16+
- Telegram Bot Token

### Установка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/yourusername/gamestats.git
cd gamestats
```

2. **Настройте переменные окружения**
```bash
cp backend/env.example backend/.env
# Отредактируйте .env файл
```

3. **Запустите бэкенд**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

4. **Запустите Telegram бота**
```bash
python mini_app_bot.py
```

## 📱 Использование

### Telegram Bot
- Отправьте `/start` для начала работы
- Используйте `/stats <username>` для поиска игрока
- Навигация через интерактивные кнопки

### Mini App
- Откройте Mini App в Telegram
- Введите никнейм игрока
- Просматривайте детальную статистику
- Используйте кнопку "Обновить" для актуальных данных

## 🏗️ Архитектура

```
Telegram Bot ←→ FastAPI Backend ←→ Data Sources
     ↓              ↓                    ↓
Mini App ←→ FastAPI Backend ←→ Game APIs
```

### Компоненты

- **Frontend**: HTML5, CSS3, JavaScript (Telegram Web App)
- **Backend**: FastAPI (Python)
- **Bot**: python-telegram-bot
- **Data**: Multiple sources with fallback system
- **Deployment**: Render, Netlify

## 🔧 API Endpoints

- `GET /player/{username}` - получить статистику игрока
- `GET /player/{username}/refresh` - обновить данные игрока
- `GET /health` - проверка состояния сервиса

## 📊 Источники данных

Платформа использует гибридный подход:
1. **Основные источники** - официальные API игр
2. **Резервные источники** - веб-скрапинг с обходом защиты
3. **Fallback система** - демо-данные при недоступности реальных

## 🛡️ Безопасность

- Валидация входных данных
- Rate limiting
- CORS настройки
- Безопасное хранение токенов
- Защита от DDoS атак

## 🚀 Развертывание

### Backend (Render)
```bash
# Автоматическое развертывание через render.yaml
```

### Frontend (Netlify)
```bash
# Автоматическое развертывание через netlify.toml
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

- 📧 Email: support@gamestats.com
- 💬 Telegram: @gamestats_support
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/gamestats/issues)

## 🎯 Roadmap

- [ ] Поддержка новых игр
- [ ] Мобильное приложение
- [ ] Социальные функции
- [ ] Турнирная система
- [ ] Аналитика команды
- [ ] Интеграция с Discord

---

**GameStats** - Ваша универсальная платформа игровой статистики! 🎮 