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

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    showWelcomeMessage();
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

function displayPlayerStats(playerData) {
    // Update player info
    document.getElementById('playerName').textContent = playerData.username;
    document.getElementById('playerLevel').textContent = `Уровень ${playerData.level}`;
    
    if (playerData.clan) {
        document.getElementById('playerClan').innerHTML = `<span class="clan-tag">[${playerData.clan.tag}]</span>`;
    } else {
        document.getElementById('playerClan').innerHTML = '';
    }
    
    // Update stats
    document.getElementById('battlesCount').textContent = formatNumber(playerData.stats.battles);
    document.getElementById('winRate').textContent = `${playerData.stats.winRate}%`;
    document.getElementById('kdRatio').textContent = playerData.stats.kdRatio;
    document.getElementById('playTime').textContent = `${playerData.stats.playTime}ч`;
    
    // Update detailed stats
    document.getElementById('totalBattles').textContent = formatNumber(playerData.stats.battles);
    document.getElementById('totalWins').textContent = formatNumber(playerData.stats.wins);
    document.getElementById('totalLosses').textContent = formatNumber(playerData.stats.losses);
    document.getElementById('totalKills').textContent = formatNumber(playerData.stats.kills);
    document.getElementById('totalDeaths').textContent = formatNumber(playerData.stats.deaths);
    
    // Show stats overview
    statsOverview.style.display = 'block';
    
    // Scroll to stats
    statsOverview.scrollIntoView({ behavior: 'smooth' });
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

function showLoading(show) {
    if (show) {
        loadingOverlay.style.display = 'flex';
    } else {
        loadingOverlay.style.display = 'none';
    }
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