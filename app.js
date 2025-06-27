// Initialize Telegram Web App
let tg = window.Telegram.WebApp;

// Initialize the app
tg.ready();
tg.expand();

// Set theme
tg.setHeaderColor('#667eea');
tg.setBackgroundColor('#667eea');

// App state
let currentPlayer = null;
let currentTab = 'general';
let currentMode = 'ab';
let isLoading = false;

// DOM elements
const searchInput = document.getElementById('playerSearch');
const searchBtn = document.getElementById('searchBtn');
const quickSearchBtns = document.querySelectorAll('.quick-search-btn');
const statsOverview = document.getElementById('statsOverview');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');
const modeBtns = document.querySelectorAll('.mode-btn');
const loadingOverlay = document.getElementById('loadingOverlay');
const settingsBtn = document.getElementById('settingsBtn');
const themeBtn = document.getElementById('themeBtn');

// --- Геймерские иконки ---
const icons = {
    general: '🎮',
    aviation: '✈️',
    tanks: '🛡️',
    fleet: '🚢',
    achievements: '🏅',
    level: '⭐',
    accuracy: '🎯',
    winrate: '🏆',
    battles: '⚔️',
    kills: '💥',
    deaths: '💀',
};

// --- Данные для вкладок ---
const demoData = {
    general: [
        { icon: '⭐', label: 'Уровень', value: '100' },
        { icon: '🏆', label: 'Winrate', value: '62%' },
        { icon: '⚔️', label: 'Боев', value: '12 345' },
        { icon: '💥', label: 'Фрагов', value: '8 888' },
        { icon: '💀', label: 'Смертей', value: '2 222' },
    ],
    aviation: [
        { icon: '✈️', label: 'Самолетов сбито', value: '3 210' },
        { icon: '🏆', label: 'Winrate', value: '65%' },
        { icon: '⚔️', label: 'Боев', value: '4 321' },
    ],
    tanks: [
        { icon: '🛡️', label: 'Танков уничтожено', value: '2 100' },
        { icon: '🏆', label: 'Winrate', value: '60%' },
        { icon: '⚔️', label: 'Боев', value: '3 000' },
    ],
    fleet: [
        { icon: '🚢', label: 'Кораблей потоплено', value: '1 234' },
        { icon: '🏆', label: 'Winrate', value: '58%' },
        { icon: '⚔️', label: 'Боев', value: '1 500' },
    ],
    achievements: [
        { icon: '🏅', label: 'Медалей', value: '15' },
        { icon: '🏅', label: 'Достижений', value: '42' },
    ],
};

// --- Вкладки ---
const tabs = [
    { id: 'general', label: 'Общие' },
    { id: 'aviation', label: 'Авиация' },
    { id: 'tanks', label: 'Танки' },
    { id: 'fleet', label: 'Флот' },
    { id: 'achievements', label: 'Достижения' },
];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    showWelcomeMessage();
    renderTabs();
    renderCards();
    setupSearch();
});

function initializeApp() {
    // Set up theme based on Telegram theme
    if (tg.colorScheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
    
    // Initialize with demo data
    showDemoData();
}

function setupEventListeners() {
    // Search functionality
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Quick search buttons
    quickSearchBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const playerName = this.dataset.player;
            searchInput.value = playerName;
            handleSearch();
        });
    });
    
    // Tab navigation
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.dataset.tab;
            switchTab(tab);
        });
    });
    
    // Mode buttons
    modeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const mode = this.dataset.mode;
            switchMode(mode);
        });
    });
    
    // Settings and theme buttons
    settingsBtn.addEventListener('click', showSettings);
    themeBtn.addEventListener('click', toggleTheme);
}

function showWelcomeMessage() {
    // Show welcome message using Telegram Web App
    tg.showAlert('🎮 Добро пожаловать в War Thunder Stats!\n\nНачните с поиска игрока для просмотра статистики.');
}

function handleSearch() {
    const playerName = searchInput.value.trim();
    
    if (!playerName) {
        tg.showAlert('Введите никнейм игрока');
        return;
    }
    
    showLoading(true);
    
    // Simulate API call
    setTimeout(() => {
        searchPlayer(playerName);
        showLoading(false);
    }, 1500);
}

function searchPlayer(playerName) {
    // Demo data - in real app this would be API call
    const demoData = {
        username: playerName,
        level: Math.floor(Math.random() * 100) + 1,
        clan: Math.random() > 0.5 ? { name: 'THUNDER', tag: 'THD' } : null,
        stats: {
            battles: Math.floor(Math.random() * 20000) + 1000,
            wins: Math.floor(Math.random() * 15000) + 500,
            losses: Math.floor(Math.random() * 8000) + 200,
            kills: Math.floor(Math.random() * 100000) + 5000,
            deaths: Math.floor(Math.random() * 25000) + 1000,
            winRate: (Math.random() * 30 + 50).toFixed(1),
            kdRatio: (Math.random() * 5 + 1).toFixed(2),
            playTime: Math.floor(Math.random() * 2000) + 100
        }
    };
    
    currentPlayer = demoData;
    displayPlayerStats(demoData);
    
    // Show success message
    tg.showAlert(`✅ Найден игрок: ${playerName}`);
}

function displayPlayerStats(player) {
    const container = document.querySelector('.container');
    // Универсальное имя
    const name = player.username || player.nickname || (player.general && player.general.name) || 'Игрок';
    // Универсальный уровень
    const level = player.level || (player.general && player.general.level) || '-';
    // Универсальный winrate
    const winrate = player.winrate || (player.general && player.general.win_rate) || '-';
    // Универсальные бои
    const battles = player.battles || (player.general && player.general.total_battles) || '-';
    // Универсальный kd
    const kd = player.kd_ratio || (player.general && player.general.kd_ratio) || '-';
    // Ошибка если нет данных
    if (!name || name === 'Игрок' || name === 'undefined') {
        showError('Игрок не найден или нет данных');
        return;
    }
    // Обновляем заголовок
    const header = document.querySelector('.header');
    header.textContent = `${name} - War Thunder Stats`;
    // Показываем основную информацию
    const mainInfo = document.createElement('div');
    mainInfo.className = 'player-info';
    mainInfo.innerHTML = `
        <div class="player-avatar">
            <div class="avatar-placeholder">${name.charAt(0).toUpperCase()}</div>
        </div>
        <div class="player-details">
            <h2>${name}</h2>
            <div class="player-stats-grid">
                <div class="stat-item">
                    <span class="stat-icon">⭐</span>
                    <span class="stat-label">Уровень</span>
                    <span class="stat-value">${level}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">🏆</span>
                    <span class="stat-label">Winrate</span>
                    <span class="stat-value">${winrate}%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">⚔️</span>
                    <span class="stat-label">Боев</span>
                    <span class="stat-value">${battles}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">💥</span>
                    <span class="stat-label">K/D</span>
                    <span class="stat-value">${kd}</span>
                </div>
            </div>
        </div>
    `;
    // Очищаем контейнер и добавляем новую информацию
    const existingInfo = container.querySelector('.player-info');
    if (existingInfo) existingInfo.remove();
    const existingContent = container.querySelector('.content');
    if (existingContent) existingContent.remove();
    container.appendChild(mainInfo);
    // Добавляем контент для вкладок
    const content = document.createElement('div');
    content.className = 'content';
    container.appendChild(content);
    // Показываем вкладки
    showTabs();
    showTab('general');
}

function switchTab(tab) {
    // Update active tab button
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tab) {
            btn.classList.add('active');
        }
    });
    
    // Update active tab panel
    tabPanels.forEach(panel => {
        panel.classList.remove('active');
        if (panel.id === tab) {
            panel.classList.add('active');
        }
    });
    
    currentTab = tab;
    
    // Load tab-specific data
    loadTabData(tab);
}

function switchMode(mode) {
    // Update active mode button
    modeBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.mode === mode) {
            btn.classList.add('active');
        }
    });
    
    currentMode = mode;
    
    // Reload current tab data with new mode
    loadTabData(currentTab);
}

function loadTabData(tab) {
    if (!currentPlayer) return;
    
    switch(tab) {
        case 'air':
            loadAirStats();
            break;
        case 'ground':
            loadGroundStats();
            break;
        case 'fleet':
            loadFleetStats();
            break;
        case 'achievements':
            loadAchievements();
            break;
    }
}

function loadAirStats() {
    const vehicleStats = document.querySelector('#air .vehicle-stats');
    const vehicles = [
        { name: 'F-16 Fighting Falcon', battles: 1247, wr: 72.3, kd: 5.2, icon: '✈️' },
        { name: 'MiG-29 Fulcrum', battles: 892, wr: 68.7, kd: 4.8, icon: '🛩️' },
        { name: 'Su-27 Flanker', battles: 654, wr: 71.2, kd: 4.9, icon: '🚁' }
    ];
    
    vehicleStats.innerHTML = vehicles.map(vehicle => `
        <div class="vehicle-card">
            <div class="vehicle-icon">${vehicle.icon}</div>
            <div class="vehicle-info">
                <h4>${vehicle.name}</h4>
                <p>Боев: ${vehicle.battles} | WR: ${vehicle.wr}% | K/D: ${vehicle.kd}</p>
            </div>
        </div>
    `).join('');
}

function loadGroundStats() {
    const vehicleStats = document.querySelector('#ground .vehicle-stats');
    const vehicles = [
        { name: 'M1A2 Abrams', battles: 892, wr: 65.8, kd: 3.7, icon: '🛡️' },
        { name: 'T-90A', battles: 756, wr: 67.3, kd: 3.9, icon: '⚔️' },
        { name: 'Leopard 2A6', battles: 634, wr: 69.1, kd: 4.1, icon: '🛡️' }
    ];
    
    vehicleStats.innerHTML = vehicles.map(vehicle => `
        <div class="vehicle-card">
            <div class="vehicle-icon">${vehicle.icon}</div>
            <div class="vehicle-info">
                <h4>${vehicle.name}</h4>
                <p>Боев: ${vehicle.battles} | WR: ${vehicle.wr}% | K/D: ${vehicle.kd}</p>
            </div>
        </div>
    `).join('');
}

function loadFleetStats() {
    const vehicleStats = document.querySelector('#fleet .vehicle-stats');
    const vehicles = [
        { name: 'USS Iowa', battles: 456, wr: 58.2, kd: 2.9, icon: '🚢' },
        { name: 'Yamato', battles: 389, wr: 61.7, kd: 3.2, icon: '⚓' },
        { name: 'Bismarck', battles: 312, wr: 59.8, kd: 2.8, icon: '🚢' }
    ];
    
    vehicleStats.innerHTML = vehicles.map(vehicle => `
        <div class="vehicle-card">
            <div class="vehicle-icon">${vehicle.icon}</div>
            <div class="vehicle-info">
                <h4>${vehicle.name}</h4>
                <p>Боев: ${vehicle.battles} | WR: ${vehicle.wr}% | K/D: ${vehicle.kd}</p>
            </div>
        </div>
    `).join('');
}

function loadAchievements() {
    const achievementsGrid = document.querySelector('#achievements .achievements-grid');
    const achievements = [
        { name: 'Супер-ас', description: '5 убийств за бой', progress: 80, icon: '🏆' },
        { name: 'Небесный король', description: '10 побед подряд', progress: 100, icon: '👑' },
        { name: 'Танковый ас', description: '1000 убийств на танках', progress: 65, icon: '🛡️' },
        { name: 'Морской волк', description: '500 побед на флоте', progress: 45, icon: '⚓' }
    ];
    
    achievementsGrid.innerHTML = achievements.map(achievement => `
        <div class="achievement-card">
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-info">
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
                <div class="achievement-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${achievement.progress}%"></div>
                    </div>
                    <span>${achievement.progress}%</span>
                </div>
            </div>
        </div>
    `).join('');
}

function showDemoData() {
    // Show demo data for testing
    const demoPlayer = {
        username: 'DemoPlayer',
        level: 85,
        clan: { name: 'DEMO', tag: 'DEMO' },
        stats: {
            battles: 15420,
            wins: 10580,
            losses: 4840,
            kills: 67890,
            deaths: 15420,
            winRate: 68.6,
            kdRatio: 4.41,
            playTime: 1247
        }
    };
    
    currentPlayer = demoPlayer;
    displayPlayerStats(demoPlayer);
}

function showLoading(show = true) {
    let overlay = document.getElementById('loadingOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<span>Загрузка...</span>';
        document.body.appendChild(overlay);
    }
    overlay.style.display = show ? 'flex' : 'none';
}

function showSettings() {
    tg.showAlert('⚙️ Настройки\n\n• Язык: Русский\n• Уведомления: Включены\n• Тема: Авто\n\nФункция настроек в разработке');
}

function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    
    if (isDark) {
        tg.setHeaderColor('#1a1a2e');
        tg.setBackgroundColor('#1a1a2e');
    } else {
        tg.setHeaderColor('#667eea');
        tg.setBackgroundColor('#667eea');
    }
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Handle back button
tg.BackButton.onClick(() => {
    if (currentPlayer) {
        // Reset to search view
        currentPlayer = null;
        statsOverview.style.display = 'none';
        searchInput.value = '';
        tg.BackButton.hide();
    }
});

// Show back button when player is found
function showBackButton() {
    tg.BackButton.show();
}

// Handle main button
tg.MainButton.onClick(() => {
    if (currentPlayer) {
        // Share player stats
        const shareText = `🎮 ${currentPlayer.username} - War Thunder Stats\n\n` +
                         `Уровень: ${currentPlayer.level}\n` +
                         `Боев: ${formatNumber(currentPlayer.stats.battles)}\n` +
                         `WR: ${currentPlayer.stats.winRate}%\n` +
                         `K/D: ${currentPlayer.stats.kdRatio}\n\n` +
                         `Проверено через WT Stats Mini App`;
        
        tg.sendData(shareText);
    }
});

// Update main button text
function updateMainButton() {
    if (currentPlayer) {
        tg.MainButton.setText('Поделиться статистикой');
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

// Export functions for external use
window.WTStatsApp = {
    searchPlayer,
    switchTab,
    switchMode,
    showDemoData,
    updateMainButton
};

function renderTabs() {
    const tabsContainer = document.querySelector('.tabs');
    if (!tabsContainer) return;
    tabsContainer.innerHTML = '';
    tabs.forEach(tab => {
        const btn = document.createElement('button');
        btn.className = 'tab' + (tab.id === currentTab ? ' active' : '');
        btn.textContent = tab.label;
        btn.onclick = () => {
            currentTab = tab.id;
            renderTabs();
            renderCards();
        };
        tabsContainer.appendChild(btn);
    });
}

function renderCards() {
    const cardsContainer = document.querySelector('.cards');
    if (!cardsContainer) return;
    cardsContainer.innerHTML = '';
    (demoData[currentTab] || []).forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `<span class="icon">${item.icon}</span> <span>${item.label}</span> <span class="value">${item.value}</span>`;
        cardsContainer.appendChild(card);
    });
}

function setupSearch() {
    const searchInput = document.querySelector('.search-bar input');
    const searchBtn = document.querySelector('.search-bar button');
    if (!searchInput || !searchBtn) return;
    searchBtn.onclick = () => {
        const val = searchInput.value.trim();
        if (val) {
            alert('Демо: поиск игрока ' + val + '\n(Здесь будет реальный поиск)');
        }
    };
    searchInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') searchBtn.onclick();
    });
}

// --- Конфигурация API ---
const API_BASE = 'https://warstats-backend.onrender.com'; // Рабочий URL бэкенда
// const API_BASE = 'http://44.226.145.213'; // IP-адрес Render сервера
// const API_BASE = 'demo'; // Раскомментируйте для демо режима

const API_ENDPOINTS = {
    player: '/player',
    top: '/top',
    compare: '/compare',
    search: '/search',
    clan: '/api/clan'
};

// API функции
async function apiCall(endpoint, params = {}) {
    try {
        // Если API_BASE = 'demo', используем демо данные
        if (API_BASE === 'demo') {
            return getDemoData(endpoint, params);
        }
        
        const url = new URL(API_BASE + endpoint);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        // Fallback на демо данные
        return getDemoData(endpoint, params);
    }
}

// Демо данные для fallback
function getDemoData(endpoint, params) {
    const demoData = {
        player: {
            nickname: params.nickname || 'DemoPlayer',
            level: 85,
            winrate: 68.5,
            battles: 12500,
            kills: 8900,
            deaths: 3200,
            kd_ratio: 2.78,
            vehicles: [
                { name: 'Т-34-85', type: 'tank', battles: 450, winrate: 72.0, kills: 380, deaths: 120 },
                { name: 'Yak-3', type: 'aircraft', battles: 320, winrate: 65.0, kills: 280, deaths: 95 },
                { name: 'IS-2', type: 'tank', battles: 280, winrate: 70.0, kills: 220, deaths: 80 }
            ],
            achievements: [
                { name: 'Ас', description: 'Сбил 5 самолетов за бой', icon: '🏅' },
                { name: 'Герой', description: '100 побед', icon: '⭐' },
                { name: 'Ветеран', description: '1000 боев', icon: '🎖️' }
            ],
            clan: { name: 'Elite Warriors', tag: 'EW', members: 50, position: 'Командир' },
            avatar_url: null,
            last_updated: new Date().toLocaleString()
        },
        top: [
            { rank: 1, nickname: 'AcePilot', level: 100, winrate: 75.5, battles: 15000, kills: 12000 },
            { rank: 2, nickname: 'TankMaster', level: 98, winrate: 72.3, battles: 12000, kills: 9500 },
            { rank: 3, nickname: 'SeaWolf', level: 95, winrate: 70.1, battles: 10000, kills: 8000 }
        ],
        search: [
            { nickname: 'Demo_Ace', level: 85, winrate: 65.0 },
            { nickname: 'Demo_Pro', level: 78, winrate: 62.0 },
            { nickname: 'Demo_Elite', level: 72, winrate: 58.0 }
        ]
    };
    
    return demoData[endpoint.split('/').pop()] || demoData.player;
}

// UI функции
function showLoading() {
    isLoading = true;
    document.body.classList.add('loading');
}

function hideLoading() {
    isLoading = false;
    document.body.classList.remove('loading');
}

function showError(message) {
    let errorDiv = document.getElementById('errorMessage');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'errorMessage';
        errorDiv.className = 'loading-overlay';
        errorDiv.style.background = 'rgba(24,28,36,0.95)';
        errorDiv.style.color = '#ff3c00';
        errorDiv.style.fontSize = '1.3rem';
        errorDiv.style.fontWeight = 'bold';
        errorDiv.style.zIndex = 2000;
        document.body.appendChild(errorDiv);
    }
    errorDiv.innerHTML = message;
    errorDiv.style.display = 'flex';
    setTimeout(() => { errorDiv.style.display = 'none'; }, 2500);
}

// Поиск игрока
async function searchPlayer() {
    const input = document.querySelector('.search-bar input');
    const nickname = input.value.trim();
    if (!nickname) {
        showError('Введите никнейм игрока');
        return;
    }
    showLoading();
    try {
        const playerData = await apiCall(API_ENDPOINTS.player, { username: nickname, nickname });
        if (!playerData || (!playerData.username && !playerData.nickname && !(playerData.general && playerData.general.level))) {
            showError('Игрок не найден или нет данных');
            hideLoading();
            return;
        }
        currentPlayer = playerData;
        displayPlayerStats(playerData);
        showTab('general');
    } catch (error) {
        showError('Ошибка при поиске игрока');
        console.error(error);
    } finally {
        hideLoading();
    }
}

// Отображение статистики игрока
function displayPlayerStats(player) {
    const container = document.querySelector('.container');
    // Универсальное имя
    const name = player.username || player.nickname || (player.general && player.general.name) || 'Игрок';
    // Универсальный уровень
    const level = player.level || (player.general && player.general.level) || '-';
    // Универсальный winrate
    const winrate = player.winrate || (player.general && player.general.win_rate) || '-';
    // Универсальные бои
    const battles = player.battles || (player.general && player.general.total_battles) || '-';
    // Универсальный kd
    const kd = player.kd_ratio || (player.general && player.general.kd_ratio) || '-';
    // Ошибка если нет данных
    if (!name || name === 'Игрок' || name === 'undefined') {
        showError('Игрок не найден или нет данных');
        return;
    }
    // Обновляем заголовок
    const header = document.querySelector('.header');
    header.textContent = `${name} - War Thunder Stats`;
    // Показываем основную информацию
    const mainInfo = document.createElement('div');
    mainInfo.className = 'player-info';
    mainInfo.innerHTML = `
        <div class="player-avatar">
            <div class="avatar-placeholder">${name.charAt(0).toUpperCase()}</div>
        </div>
        <div class="player-details">
            <h2>${name}</h2>
            <div class="player-stats-grid">
                <div class="stat-item">
                    <span class="stat-icon">⭐</span>
                    <span class="stat-label">Уровень</span>
                    <span class="stat-value">${level}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">🏆</span>
                    <span class="stat-label">Winrate</span>
                    <span class="stat-value">${winrate}%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">⚔️</span>
                    <span class="stat-label">Боев</span>
                    <span class="stat-value">${battles}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">💥</span>
                    <span class="stat-label">K/D</span>
                    <span class="stat-value">${kd}</span>
                </div>
            </div>
        </div>
    `;
    // Очищаем контейнер и добавляем новую информацию
    const existingInfo = container.querySelector('.player-info');
    if (existingInfo) existingInfo.remove();
    const existingContent = container.querySelector('.content');
    if (existingContent) existingContent.remove();
    container.appendChild(mainInfo);
    // Добавляем контент для вкладок
    const content = document.createElement('div');
    content.className = 'content';
    container.appendChild(content);
    // Показываем вкладки
    showTabs();
    showTab('general');
}

// Показ вкладок
function showTabs() {
    const container = document.querySelector('.container');
    let tabs = container.querySelector('.tabs');
    if (tabs) tabs.remove();
    tabs = document.createElement('div');
    tabs.className = 'tabs';
    const tabList = [
        { id: 'general', label: 'Общие', icon: '🎮' },
        { id: 'aviation', label: 'Авиация', icon: '✈️' },
        { id: 'tanks', label: 'Танки', icon: '🛡️' },
        { id: 'fleet', label: 'Флот', icon: '🚢' },
        { id: 'achievements', label: 'Достижения', icon: '🏅' },
        { id: 'clan', label: 'Клан', icon: '👑' },
        { id: 'charts', label: 'Графики', icon: '📊' }
    ];
    tabList.forEach(tab => {
        const btn = document.createElement('button');
        btn.className = 'tab-btn';
        btn.innerHTML = `${tab.icon} <span>${tab.label}</span>`;
        btn.onclick = () => { switchTab(tab.id); };
        tabs.appendChild(btn);
    });
    container.appendChild(tabs);
}

// Показ содержимого вкладки
function showTab(tabName) {
    if (!currentPlayer) return;
    
    currentTab = tabName;
    const content = document.querySelector('.content');
    
    switch (tabName) {
        case 'general':
            showGeneralTab(content);
            break;
        case 'aviation':
            showAviationTab(content);
            break;
        case 'tanks':
            showTanksTab(content);
            break;
        case 'fleet':
            showFleetTab(content);
            break;
        case 'achievements':
            showAchievementsTab(content);
            break;
        case 'clan':
            showClanTab(content);
            break;
        case 'charts':
            showChartsTab(content);
            break;
    }
}

// Вкладка "Общие"
function showGeneralTab(content) {
    content.innerHTML = `
        <div class="tab-content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-icon">💥</span>
                        <span class="stat-title">Убийства</span>
                    </div>
                    <div class="stat-value">${currentPlayer.kills.toLocaleString()}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-icon">💀</span>
                        <span class="stat-title">Смерти</span>
                    </div>
                    <div class="stat-value">${currentPlayer.deaths.toLocaleString()}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-icon">🎯</span>
                        <span class="stat-title">Точность</span>
                    </div>
                    <div class="stat-value">${(currentPlayer.kills / currentPlayer.battles * 100).toFixed(1)}%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-icon">⚡</span>
                        <span class="stat-title">Активность</span>
                    </div>
                    <div class="stat-value">${Math.floor(currentPlayer.battles / 30)}/день</div>
                </div>
            </div>
            
            <div class="section-title">Топ техника</div>
            <div class="vehicles-list">
                ${currentPlayer.vehicles.slice(0, 5).map(vehicle => `
                    <div class="vehicle-item">
                        <div class="vehicle-icon">${getVehicleIcon(vehicle.type)}</div>
                        <div class="vehicle-info">
                            <div class="vehicle-name">${vehicle.name}</div>
                            <div class="vehicle-stats">
                                <span>${vehicle.battles} боев</span>
                                <span>${vehicle.winrate}%</span>
                                <span>K/D: ${(vehicle.kills / vehicle.deaths).toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Вкладка "Авиация"
function showAviationTab(content) {
    const aviationVehicles = currentPlayer.vehicles.filter(v => v.type === 'aircraft');
    content.innerHTML = `
        <div class="tab-content">
            <div class="section-title">Авиационная статистика</div>
            <div class="aviation-stats">
                <div class="stat-card large">
                    <div class="stat-header">
                        <span class="stat-icon">✈️</span>
                        <span class="stat-title">Самолетов сбито</span>
                    </div>
                    <div class="stat-value">${aviationVehicles.reduce((sum, v) => sum + v.kills, 0).toLocaleString()}</div>
                </div>
            </div>
            
            <div class="vehicles-list">
                ${aviationVehicles.map(vehicle => `
                    <div class="vehicle-item">
                        <div class="vehicle-icon">✈️</div>
                        <div class="vehicle-info">
                            <div class="vehicle-name">${vehicle.name}</div>
                            <div class="vehicle-stats">
                                <span>${vehicle.battles} боев</span>
                                <span>${vehicle.winrate}%</span>
                                <span>K/D: ${(vehicle.kills / vehicle.deaths).toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Вкладка "Танки"
function showTanksTab(content) {
    const tankVehicles = currentPlayer.vehicles.filter(v => v.type === 'tank');
    content.innerHTML = `
        <div class="tab-content">
            <div class="section-title">Танковая статистика</div>
            <div class="tank-stats">
                <div class="stat-card large">
                    <div class="stat-header">
                        <span class="stat-icon">🛡️</span>
                        <span class="stat-title">Танков уничтожено</span>
                    </div>
                    <div class="stat-value">${tankVehicles.reduce((sum, v) => sum + v.kills, 0).toLocaleString()}</div>
                </div>
            </div>
            
            <div class="vehicles-list">
                ${tankVehicles.map(vehicle => `
                    <div class="vehicle-item">
                        <div class="vehicle-icon">🛡️</div>
                        <div class="vehicle-info">
                            <div class="vehicle-name">${vehicle.name}</div>
                            <div class="vehicle-stats">
                                <span>${vehicle.battles} боев</span>
                                <span>${vehicle.winrate}%</span>
                                <span>K/D: ${(vehicle.kills / vehicle.deaths).toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Вкладка "Флот"
function showFleetTab(content) {
    const fleetVehicles = currentPlayer.vehicles.filter(v => v.type === 'ship');
    content.innerHTML = `
        <div class="tab-content">
            <div class="section-title">Флотская статистика</div>
            <div class="fleet-stats">
                <div class="stat-card large">
                    <div class="stat-header">
                        <span class="stat-icon">🚢</span>
                        <span class="stat-title">Кораблей потоплено</span>
                    </div>
                    <div class="stat-value">${fleetVehicles.reduce((sum, v) => sum + v.kills, 0).toLocaleString()}</div>
                </div>
            </div>
            
            <div class="vehicles-list">
                ${fleetVehicles.length > 0 ? fleetVehicles.map(vehicle => `
                    <div class="vehicle-item">
                        <div class="vehicle-icon">🚢</div>
                        <div class="vehicle-info">
                            <div class="vehicle-name">${vehicle.name}</div>
                            <div class="vehicle-stats">
                                <span>${vehicle.battles} боев</span>
                                <span>${vehicle.winrate}%</span>
                                <span>K/D: ${(vehicle.kills / vehicle.deaths).toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                `).join('') : '<div class="no-data">Нет данных о флотской технике</div>'}
            </div>
        </div>
    `;
}

// Вкладка "Достижения"
function showAchievementsTab(content) {
    content.innerHTML = `
        <div class="tab-content">
            <div class="section-title">Достижения</div>
            <div class="achievements-grid">
                ${currentPlayer.achievements.map(achievement => `
                    <div class="achievement-card">
                        <div class="achievement-icon">${achievement.icon}</div>
                        <div class="achievement-info">
                            <div class="achievement-name">${achievement.name}</div>
                            <div class="achievement-description">${achievement.description}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Вкладка "Клан"
function showClanTab(content) {
    if (currentPlayer.clan) {
        content.innerHTML = `
            <div class="tab-content">
                <div class="section-title">Клановая информация</div>
                <div class="clan-card">
                    <div class="clan-header">
                        <div class="clan-tag">[${currentPlayer.clan.tag}]</div>
                        <div class="clan-name">${currentPlayer.clan.name}</div>
                    </div>
                    <div class="clan-stats">
                        <div class="clan-stat">
                            <span class="stat-label">Участников:</span>
                            <span class="stat-value">${currentPlayer.clan.members}</span>
                        </div>
                        <div class="clan-stat">
                            <span class="stat-label">Позиция:</span>
                            <span class="stat-value">${currentPlayer.clan.position}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        content.innerHTML = `
            <div class="tab-content">
                <div class="section-title">Клановая информация</div>
                <div class="no-data">Игрок не состоит в клане</div>
            </div>
        `;
    }
}

// Вкладка "Графики"
function showChartsTab(content) {
    content.innerHTML = `
        <div class="tab-content">
            <div class="section-title">Графики статистики</div>
            <div class="charts-container">
                <div class="chart-card">
                    <h3>Распределение техники</h3>
                    <canvas id="vehiclesChart" width="300" height="200"></canvas>
                </div>
                <div class="chart-card">
                    <h3>Winrate по типам</h3>
                    <canvas id="winrateChart" width="300" height="200"></canvas>
                </div>
            </div>
        </div>
    `;
    
    // Создаем графики
    setTimeout(() => {
        createVehiclesChart();
        createWinrateChart();
    }, 100);
}

// Создание графика техники
function createVehiclesChart() {
    const canvas = document.getElementById('vehiclesChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const vehicleTypes = ['tank', 'aircraft', 'ship'];
    const counts = vehicleTypes.map(type => 
        currentPlayer.vehicles.filter(v => v.type === type).length
    );
    
    // Простой график
    const maxCount = Math.max(...counts);
    const barWidth = 60;
    const barSpacing = 20;
    const startX = 30;
    const startY = 150;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    vehicleTypes.forEach((type, index) => {
        const x = startX + index * (barWidth + barSpacing);
        const height = (counts[index] / maxCount) * 100;
        const y = startY - height;
        
        ctx.fillStyle = getVehicleColor(type);
        ctx.fillRect(x, y, barWidth, height);
        
        ctx.fillStyle = '#e0e0e0';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(type, x + barWidth/2, startY + 15);
        ctx.fillText(counts[index], x + barWidth/2, y - 5);
    });
}

// Создание графика winrate
function createWinrateChart() {
    const canvas = document.getElementById('winrateChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const vehicleTypes = ['tank', 'aircraft', 'ship'];
    const winrates = vehicleTypes.map(type => {
        const vehicles = currentPlayer.vehicles.filter(v => v.type === type);
        return vehicles.length > 0 ? 
            vehicles.reduce((sum, v) => sum + v.winrate, 0) / vehicles.length : 0;
    });
    
    // Простой график
    const maxWinrate = Math.max(...winrates);
    const barWidth = 60;
    const barSpacing = 20;
    const startX = 30;
    const startY = 150;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    vehicleTypes.forEach((type, index) => {
        const x = startX + index * (barWidth + barSpacing);
        const height = (winrates[index] / maxWinrate) * 100;
        const y = startY - height;
        
        ctx.fillStyle = getVehicleColor(type);
        ctx.fillRect(x, y, barWidth, height);
        
        ctx.fillStyle = '#e0e0e0';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(type, x + barWidth/2, startY + 15);
        ctx.fillText(winrates[index].toFixed(1) + '%', x + barWidth/2, y - 5);
    });
}

// Вспомогательные функции
function getVehicleIcon(type) {
    const icons = {
        'tank': '🛡️',
        'aircraft': '✈️',
        'ship': '🚢'
    };
    return icons[type] || '⚔️';
}

function getVehicleColor(type) {
    const colors = {
        'tank': '#ff6b6b',
        'aircraft': '#4ecdc4',
        'ship': '#45b7d1'
    };
    return colors[type] || '#95a5a6';
} 