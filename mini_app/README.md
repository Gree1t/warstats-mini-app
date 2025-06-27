# War Thunder Stats Mini App

Современная Telegram Mini App для просмотра статистики игроков War Thunder с красивым дизайном в стиле кофейни.

## 🎨 Особенности дизайна

- **Современный UI** с градиентами и стеклянным эффектом
- **Адаптивный дизайн** для всех устройств
- **Темная/светлая тема** с автоматическим переключением
- **Плавные анимации** и переходы
- **Интуитивная навигация** с табами и кнопками

## 🚀 Функции

### Основные возможности
- 🔍 **Поиск игроков** по никнейму
- 📊 **Детальная статистика** (общая, авиация, танки, флот)
- 🏅 **Система достижений** с прогресс-барами
- 👥 **Информация о кланах**
- 📈 **Сравнение режимов** (Arcade/Realistic/Simulator)
- 🌙 **Переключение темы** (светлая/темная)

### Интеграция с Telegram
- **Telegram Web App API** для нативной интеграции
- **Кнопки навигации** (Назад, Главная)
- **Поделиться статистикой** через Telegram
- **Адаптация под тему** Telegram

## 📱 Установка и настройка

### 1. Подготовка файлов
```bash
# Структура проекта
mini_app/
├── index.html      # Главная страница
├── styles.css      # Стили
├── app.js          # JavaScript логика
└── README.md       # Документация
```

### 2. Настройка бота для Mini App

1. **Создайте бота** через @BotFather
2. **Настройте Mini App**:
   ```
   /newapp
   Выберите бота: @your_bot_name
   Название: War Thunder Stats
   Описание: Статистика игроков War Thunder
   URL: https://your-domain.com/mini_app/
   ```

3. **Добавьте команду**:
   ```
   /setcommands
   Выберите бота: @your_bot_name
   Команды:
   start - Запустить War Thunder Stats
   stats - Открыть статистику
   ```

### 3. Размещение на сервере

```bash
# Загрузите файлы на ваш веб-сервер
# Пример с nginx:
server {
    listen 80;
    server_name your-domain.com;
    
    location /mini_app/ {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /mini_app/index.html;
    }
}
```

### 4. Настройка HTTPS (обязательно для Mini App)

```bash
# Установите SSL сертификат
sudo certbot --nginx -d your-domain.com
```

## 🎯 Использование

### Для пользователей
1. **Найдите бота** в Telegram
2. **Нажмите кнопку "Start"** или команду `/start`
3. **Введите никнейм** игрока для поиска
4. **Просматривайте статистику** по разделам
5. **Поделитесь результатами** с друзьями

### Для разработчиков

#### Добавление новых функций
```javascript
// В app.js добавьте новые обработчики
function newFeature() {
    // Ваша логика
    tg.showAlert('Новая функция!');
}

// Подключите к кнопке
document.getElementById('newBtn').addEventListener('click', newFeature);
```

#### Интеграция с API
```javascript
// Замените demo данные на реальные API вызовы
async function searchPlayer(playerName) {
    try {
        const response = await fetch(`/api/player/${playerName}`);
        const data = await response.json();
        displayPlayerStats(data);
    } catch (error) {
        tg.showAlert('Ошибка при поиске игрока');
    }
}
```

## 🎨 Кастомизация

### Изменение цветов
```css
/* В styles.css измените основные цвета */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ff6b6b;
}
```

### Добавление новых разделов
```html
<!-- В index.html добавьте новую вкладку -->
<button class="tab-btn" data-tab="new-section">
    <span class="tab-icon">🆕</span>
    <span class="tab-text">Новый раздел</span>
</button>

<!-- И соответствующий контент -->
<div class="tab-panel" id="new-section">
    <div class="content-card">
        <h3>Новый раздел</h3>
        <!-- Ваш контент -->
    </div>
</div>
```

## 🔧 Технические требования

- **HTTPS** - обязательно для Mini App
- **Telegram Web App API** - для интеграции
- **Современный браузер** - поддержка ES6+
- **Responsive дизайн** - для мобильных устройств

## 📊 Производительность

- **Быстрая загрузка** - оптимизированные ресурсы
- **Кэширование** - для улучшения скорости
- **Lazy loading** - для больших данных
- **Минификация** - для продакшена

## 🚀 Развертывание

### Docker (рекомендуется)
```dockerfile
FROM nginx:alpine
COPY mini_app/ /usr/share/nginx/html/mini_app/
EXPOSE 80
```

### Статический хостинг
- **Netlify** - простой деплой
- **Vercel** - быстрая загрузка
- **GitHub Pages** - бесплатный хостинг

## 🔒 Безопасность

- **HTTPS только** - для Mini App
- **Валидация входных данных** - защита от XSS
- **CORS настройки** - для API запросов
- **Rate limiting** - защита от спама

## 📈 Мониторинг

### Аналитика
```javascript
// Добавьте Google Analytics или Yandex.Metrica
gtag('event', 'search_player', {
    'player_name': playerName
});
```

### Логирование ошибок
```javascript
// Отправка ошибок в Sentry
Sentry.captureException(error);
```

## 🤝 Вклад в проект

1. **Fork** репозиторий
2. **Создайте ветку** для новой функции
3. **Внесите изменения** и протестируйте
4. **Создайте Pull Request**

## 📞 Поддержка

- **Issues** - для багов и предложений
- **Discussions** - для обсуждений
- **Telegram** - для быстрой связи

## 📄 Лицензия

MIT License - свободное использование и модификация

---

**Создано с ❤️ для сообщества War Thunder** 