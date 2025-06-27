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
}

function setupEventListeners() {
    // Search functionality
    if (searchBtn) {
        searchBtn.addEventListener('click', handleSearch);
    }
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleSearch();
            }
        });
    }
    
    // Quick search buttons
    quickSearchBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const playerName = this.dataset.player;
            if (searchInput) {
                searchInput.value = playerName;
            }
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
    if (settingsBtn) {
        settingsBtn.addEventListener('click', showSettings);
    }
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
}

function showWelcomeMessage() {
    // Show welcome message using Telegram Web App
    tg.showAlert('🎮 Добро пожаловать в War Thunder Stats!\n\nНачните с поиска игрока для просмотра статистики.');
}

function handleSearch() {
    const playerName = searchInput ? searchInput.value.trim() : '';
    
    if (!playerName) {
        tg.showAlert('Введите никнейм игрока');
        return;
    }
    
    showLoading(true);
    
    // Use real API
    searchPlayer(playerName);
}

function searchPlayer(playerName) {
    // Use real API
    const apiUrl = 'https://warstats-backend.onrender.com';
    
    fetch(`${apiUrl}/player/${encodeURIComponent(playerName)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            currentPlayer = data;
            displayPlayerStats(data);
            showLoading(false);
            tg.showAlert(`✅ Найден игрок: ${playerName}`);
        })
        .catch(error => {
            console.error('Error:', error);
            showLoading(false);
            tg.showAlert(`❌ Ошибка при поиске игрока: ${error.message}`);
        });
}

function displayPlayerStats(playerData) {
    // Update player info
    const playerNameEl = document.getElementById('playerName');
    const playerLevelEl = document.getElementById('playerLevel');
    const playerClanEl = document.getElementById('playerClan');
    
    if (playerNameEl) playerNameEl.textContent = playerData.username || playerData.general?.name || 'Unknown';
    if (playerLevelEl) playerLevelEl.textContent = `Уровень ${playerData.level || playerData.general?.level || 0}`;
    
    if (playerClanEl) {
        if (playerData.clan) {
            playerClanEl.innerHTML = `<span class="clan-tag">[${playerData.clan.tag}]</span>`;
        } else {
            playerClanEl.innerHTML = '';
        }
    }
    
    // Update stats
    const stats = playerData.stats || playerData.general || {};
    const battlesEl = document.getElementById('battlesCount');
    const winRateEl = document.getElementById('winRate');
    const kdRatioEl = document.getElementById('kdRatio');
    const playTimeEl = document.getElementById('playTime');
    
    if (battlesEl) battlesEl.textContent = formatNumber(stats.total_battles || stats.battles || 0);
    if (winRateEl) winRateEl.textContent = `${(stats.winrate || 0).toFixed(1)}%`;
    if (kdRatioEl) kdRatioEl.textContent = (stats.kd_ratio || 0).toFixed(2);
    if (playTimeEl) playTimeEl.textContent = `${stats.play_time || 0}ч`;
    
    // Update detailed stats
    const totalBattlesEl = document.getElementById('totalBattles');
    const totalWinsEl = document.getElementById('totalWins');
    const totalLossesEl = document.getElementById('totalLosses');
    const totalKillsEl = document.getElementById('totalKills');
    const totalDeathsEl = document.getElementById('totalDeaths');
    
    if (totalBattlesEl) totalBattlesEl.textContent = formatNumber(stats.total_battles || stats.battles || 0);
    if (totalWinsEl) totalWinsEl.textContent = formatNumber(stats.wins || 0);
    if (totalLossesEl) totalLossesEl.textContent = formatNumber(stats.losses || 0);
    if (totalKillsEl) totalKillsEl.textContent = formatNumber(stats.kills || 0);
    if (totalDeathsEl) totalDeathsEl.textContent = formatNumber(stats.deaths || 0);
    
    // Show top vehicle card
    const topVehicleCard = document.getElementById('topVehicleCard');
    if (topVehicleCard && playerData.top_vehicles && playerData.top_vehicles.length > 0) {
        const v = playerData.top_vehicles[0];
        topVehicleCard.innerHTML = `
            <img class="top-vehicle-img" src="${v.icon}" alt="${v.name}" onerror="this.style.display='none'">
            <div class="top-vehicle-info">
                <div class="top-vehicle-title">${v.name}</div>
                <div class="top-vehicle-type">${vehicleTypeLabel(v.type)}</div>
                <div class="top-vehicle-battles">Боев: ${formatNumber(v.battles)}</div>
            </div>
        `;
        topVehicleCard.style.display = 'flex';
        topVehicleCard.style.opacity = 0;
        setTimeout(() => { topVehicleCard.style.opacity = 1; }, 100);
    } else if (topVehicleCard) {
        topVehicleCard.style.display = 'none';
    }
    
    // Show stats overview
    if (statsOverview) {
        statsOverview.style.display = 'block';
        statsOverview.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Show back button
    showBackButton();
}

function vehicleTypeLabel(type) {
    switch(type) {
        case 'air': return 'Авиация';
        case 'ground': return 'Танки';
        case 'fleet': return 'Флот';
        default: return '';
    }
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
        if (panel.dataset.tab === tab) {
            panel.classList.add('active');
        }
    });
    
    currentTab = tab;
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
    loadTabData(currentTab);
}

function loadTabData(tab) {
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
    if (!currentPlayer) return;
    
    const stats = currentPlayer.air || {};
    const container = document.querySelector('[data-tab="air"] .vehicle-stats');
    
    if (container) {
        container.innerHTML = `
            <div class="vehicle-card">
                <div class="vehicle-header">
                    <h3>✈️ Авиация</h3>
                </div>
                <div class="vehicle-stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">Боев</span>
                        <span class="stat-value">${formatNumber(stats.battles || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Побед</span>
                        <span class="stat-value">${formatNumber(stats.wins || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Убийств</span>
                        <span class="stat-value">${formatNumber(stats.kills || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Смертей</span>
                        <span class="stat-value">${formatNumber(stats.deaths || 0)}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

function loadGroundStats() {
    if (!currentPlayer) return;
    
    const stats = currentPlayer.ground || {};
    const container = document.querySelector('[data-tab="ground"] .vehicle-stats');
    
    if (container) {
        container.innerHTML = `
            <div class="vehicle-card">
                <div class="vehicle-header">
                    <h3>🛡️ Танки</h3>
                </div>
                <div class="vehicle-stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">Боев</span>
                        <span class="stat-value">${formatNumber(stats.battles || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Побед</span>
                        <span class="stat-value">${formatNumber(stats.wins || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Убийств</span>
                        <span class="stat-value">${formatNumber(stats.kills || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Смертей</span>
                        <span class="stat-value">${formatNumber(stats.deaths || 0)}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

function loadFleetStats() {
    if (!currentPlayer) return;
    
    const stats = currentPlayer.fleet || {};
    const container = document.querySelector('[data-tab="fleet"] .vehicle-stats');
    
    if (container) {
        container.innerHTML = `
            <div class="vehicle-card">
                <div class="vehicle-header">
                    <h3>🚢 Флот</h3>
                </div>
                <div class="vehicle-stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">Боев</span>
                        <span class="stat-value">${formatNumber(stats.battles || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Побед</span>
                        <span class="stat-value">${formatNumber(stats.wins || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Убийств</span>
                        <span class="stat-value">${formatNumber(stats.kills || 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Смертей</span>
                        <span class="stat-value">${formatNumber(stats.deaths || 0)}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

function loadAchievements() {
    if (!currentPlayer) return;
    
    const achievements = currentPlayer.achievements || [];
    const container = document.querySelector('[data-tab="achievements"] .achievements-list');
    
    if (container) {
        if (achievements.length > 0) {
            container.innerHTML = achievements.map(achievement => `
                <div class="achievement-item">
                    <div class="achievement-icon">🏆</div>
                    <div class="achievement-info">
                        <div class="achievement-name">${achievement.name}</div>
                        <div class="achievement-desc">${achievement.description}</div>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="no-achievements">Достижения не найдены</div>';
        }
    }
}

function showLoading(show) {
    if (loadingOverlay) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
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
        if (statsOverview) {
            statsOverview.style.display = 'none';
        }
        if (searchInput) {
            searchInput.value = '';
        }
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
        const shareText = `🎮 ${currentPlayer.username || currentPlayer.general?.name} - War Thunder Stats\n\n` +
                         `Уровень: ${currentPlayer.level || currentPlayer.general?.level}\n` +
                         `Боев: ${formatNumber((currentPlayer.stats || currentPlayer.general || {}).total_battles || 0)}\n` +
                         `Винрейт: ${((currentPlayer.stats || currentPlayer.general || {}).winrate || 0).toFixed(1)}%\n` +
                         `K/D: ${((currentPlayer.stats || currentPlayer.general || {}).kd_ratio || 0).toFixed(2)}`;
        
        tg.sendData(shareText);
    }
}); 