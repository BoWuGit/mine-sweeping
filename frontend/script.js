/**
 * Minesweeper Game Frontend
 * Complete game logic with API integration
 */

class MinesweeperGame {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.currentGame = null;
        this.gameTimer = null;
        this.gameStartTime = null;
        this.isGameActive = false;
        
        this.initializeElements();
        this.bindEvents();
        this.updateStatus('准备开始游戏');
    }

    initializeElements() {
        // Game elements
        this.gameBoard = document.getElementById('game-board');
        this.statusMessage = document.getElementById('status-message');
        this.timerElement = document.getElementById('timer');
        this.flagCountElement = document.getElementById('flag-count');
        this.mineCountElement = document.getElementById('mine-count');
        
        // Controls
        this.difficultySelect = document.getElementById('difficulty');
        this.customSettings = document.getElementById('custom-settings');
        this.customWidth = document.getElementById('custom-width');
        this.customHeight = document.getElementById('custom-height');
        this.customMines = document.getElementById('custom-mines');
        this.newGameBtn = document.getElementById('new-game-btn');
        this.restartBtn = document.getElementById('restart-btn');
        
        // Modal
        this.gameOverModal = document.getElementById('game-over-modal');
        this.modalTitle = document.getElementById('modal-title');
        this.modalMessage = document.getElementById('modal-message');
        this.modalTime = document.getElementById('modal-time');
        this.modalFlags = document.getElementById('modal-flags');
        this.modalNewGame = document.getElementById('modal-new-game');
        this.modalClose = document.getElementById('modal-close');
        
        // Loading
        this.loading = document.getElementById('loading');
        
        // Audio - 使用新的音效系统
        this.soundEnabled = true;
    }

    bindEvents() {
        // Difficulty selection
        this.difficultySelect.addEventListener('change', () => {
            this.toggleCustomSettings();
        });

        // Custom settings validation
        this.customWidth.addEventListener('input', () => this.validateCustomSettings());
        this.customHeight.addEventListener('input', () => this.validateCustomSettings());
        this.customMines.addEventListener('input', () => this.validateCustomSettings());

        // Buttons
        this.newGameBtn.addEventListener('click', () => this.startNewGame());
        this.restartBtn.addEventListener('click', () => this.restartGame());
        
        // Modal
        this.modalNewGame.addEventListener('click', () => {
            this.hideModal();
            this.startNewGame();
        });
        this.modalClose.addEventListener('click', () => this.hideModal());
        
        // Close modal on background click
        this.gameOverModal.addEventListener('click', (e) => {
            if (e.target === this.gameOverModal) {
                this.hideModal();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' || e.key === 'R') {
                if (this.isGameActive) {
                    this.restartGame();
                }
            }
            if (e.key === 'n' || e.key === 'N') {
                this.startNewGame();
            }
        });
    }

    toggleCustomSettings() {
        const isCustom = this.difficultySelect.value === 'custom';
        this.customSettings.style.display = isCustom ? 'flex' : 'none';
        
        if (isCustom) {
            this.validateCustomSettings();
        }
    }

    validateCustomSettings() {
        let width = parseInt(this.customWidth.value) || 10;
        let height = parseInt(this.customHeight.value) || 10;
        let mines = parseInt(this.customMines.value) || 10;
        
        // 强制限制最小值为5
        if (width < 5) {
            width = 5;
            this.customWidth.value = 5;
        }
        
        if (height < 5) {
            height = 5;
            this.customHeight.value = 5;
        }
        
        const maxMines = width * height - 1;
        
        if (mines > maxMines) {
            this.customMines.value = maxMines;
        }
        
        if (mines < 1) {
            this.customMines.value = 1;
        }
    }

    async startNewGame() {
        try {
            this.showLoading();
            
            const difficulty = this.difficultySelect.value;
            let requestData = { difficulty };
            
            if (difficulty === 'custom') {
                // 确保使用验证后的值
                this.validateCustomSettings();
                requestData = {
                    difficulty: 'custom',
                    width: parseInt(this.customWidth.value),
                    height: parseInt(this.customHeight.value),
                    mine_count: parseInt(this.customMines.value)
                };
            }
            
            const response = await fetch(`${this.apiBaseUrl}/game/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.renderGame();
                this.startTimer();
                this.isGameActive = true;
                this.restartBtn.disabled = false;
                this.updateStatus('游戏开始！点击格子开始游戏');
            } else {
                throw new Error(data.error || '创建游戏失败');
            }
            
        } catch (error) {
            console.error('Error starting new game:', error);
            this.updateStatus(`错误: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    async restartGame() {
        if (!this.currentGame) return;
        
        try {
            this.showLoading();
            
            const response = await fetch(`${this.apiBaseUrl}/game/${this.currentGame.game_id}/restart`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.renderGame();
                this.resetTimer();
                this.startTimer();
                this.isGameActive = true;
                this.updateStatus('游戏重新开始！');
            } else {
                throw new Error(data.error || '重启游戏失败');
            }
            
        } catch (error) {
            console.error('Error restarting game:', error);
            this.updateStatus(`错误: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    async revealCell(x, y) {
        if (!this.currentGame || !this.isGameActive) return;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/game/${this.currentGame.game_id}/reveal`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x, y })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.renderGame();
                this.updateGameInfo();
                
                // Play sound
                this.playSound('reveal');
                
                // Check game status
                if (data.game_state.status === 'won') {
                    this.handleGameWin(data.message);
                } else if (data.game_state.status === 'lost') {
                    this.handleGameLoss(data.message);
                }
            } else {
                console.warn('Cell reveal failed:', data.message);
            }
            
        } catch (error) {
            console.error('Error revealing cell:', error);
            this.updateStatus(`错误: ${error.message}`);
        }
    }

    async flagCell(x, y) {
        if (!this.currentGame || !this.isGameActive) return;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/game/${this.currentGame.game_id}/flag`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x, y })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.currentGame = data.game_state;
                this.renderGame();
                this.updateGameInfo();
                
                // Play sound
                this.playSound('flag');
                
                // Check game status
                if (data.game_state.status === 'won') {
                    this.handleGameWin(data.message);
                }
            } else {
                console.warn('Cell flag failed:', data.message);
            }
            
        } catch (error) {
            console.error('Error flagging cell:', error);
            this.updateStatus(`错误: ${error.message}`);
        }
    }

    renderGame() {
        if (!this.currentGame) return;
        
        this.gameBoard.innerHTML = '';
        this.gameBoard.style.gridTemplateColumns = `repeat(${this.currentGame.width}, 1fr)`;
        
        for (let y = 0; y < this.currentGame.height; y++) {
            for (let x = 0; x < this.currentGame.width; x++) {
                const cell = this.currentGame.board[y][x];
                const cellElement = this.createCellElement(cell, x, y);
                this.gameBoard.appendChild(cellElement);
            }
        }
    }

    createCellElement(cell, x, y) {
        const cellElement = document.createElement('div');
        cellElement.className = 'cell';
        cellElement.dataset.x = x;
        cellElement.dataset.y = y;
        cellElement.textContent = ''; // 强制清空内容

        // Set cell state
        if (cell.state === 'revealed') {
            cellElement.classList.add('revealed');
            if (cell.is_mine) {
                cellElement.classList.add('exploded');
            } else if (cell.neighbor_mines > 0) {
                cellElement.textContent = cell.neighbor_mines;
                cellElement.dataset.mines = cell.neighbor_mines;
            }
        } else if (cell.state === 'flagged') {
            cellElement.classList.add('flagged');
            cellElement.textContent = '🚩';
        } else {
            cellElement.classList.add('hidden');
        }

        // Add event listeners
        cellElement.addEventListener('click', (e) => {
            e.preventDefault();
            if (cell.state !== 'flagged') {
                this.revealCell(x, y);
            }
        });

        cellElement.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            if (cell.state !== 'revealed') {
                this.flagCell(x, y);
            }
        });

        return cellElement;
    }

    updateGameInfo() {
        if (!this.currentGame) return;
        
        this.flagCountElement.textContent = this.currentGame.flagged_count;
        this.mineCountElement.textContent = this.currentGame.mine_count;
    }

    updateStatus(message) {
        this.statusMessage.textContent = message;
    }

    startTimer() {
        this.gameStartTime = Date.now();
        this.gameTimer = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.gameStartTime) / 1000);
            this.timerElement.textContent = elapsed.toString().padStart(3, '0');
        }, 1000);
    }

    resetTimer() {
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
            this.gameTimer = null;
        }
        this.timerElement.textContent = '000';
    }

    stopTimer() {
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
            this.gameTimer = null;
        }
    }

    handleGameWin(message) {
        this.isGameActive = false;
        this.stopTimer();
        this.playSound('victory');
        this.updateStatus(message);
        this.showGameOverModal('恭喜获胜！', message, 'victory');
    }

    handleGameLoss(message) {
        this.isGameActive = false;
        this.stopTimer();
        this.playSound('explosion');
        this.updateStatus(message);
        this.showGameOverModal('游戏结束', message, 'defeat');
    }

    showGameOverModal(title, message, type) {
        this.modalTitle.textContent = title;
        this.modalMessage.textContent = message;
        this.modalTime.textContent = this.timerElement.textContent;
        this.modalFlags.textContent = this.currentGame.flagged_count;
        
        // Update modal styling based on game result
        const modalHeader = this.gameOverModal.querySelector('.modal-header');
        if (type === 'victory') {
            modalHeader.style.background = 'linear-gradient(135deg, #38a169 0%, #2f855a 100%)';
        } else {
            modalHeader.style.background = 'linear-gradient(135deg, #e53e3e 0%, #c53030 100%)';
        }
        
        this.gameOverModal.classList.add('show');
    }

    hideModal() {
        this.gameOverModal.classList.remove('show');
    }

    showLoading() {
        this.loading.classList.add('show');
    }

    hideLoading() {
        this.loading.classList.remove('show');
    }

    playSound(soundType) {
        if (!this.soundEnabled) return;
        
        // 映射音效类型到新的音效名称
        const soundMap = {
            'reveal': 'click',
            'flag': 'beep',
            'explosion': 'explosion',
            'victory': 'victory'
        };
        
        const soundName = soundMap[soundType];
        if (soundName && typeof playSound === 'function') {
            playSound(soundName);
        }
    }

    // Utility methods
    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/game/health`);
            if (response.ok) {
                const data = await response.json();
                console.log('API Health:', data);
                return true;
            }
        } catch (error) {
            console.error('API Health check failed:', error);
            this.updateStatus('无法连接到游戏服务器，请检查后端服务是否运行');
            return false;
        }
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const game = new MinesweeperGame();
    
    // Check API health on startup
    game.checkApiHealth();
    
    // Make game instance globally available for debugging
    window.minesweeperGame = game;
});
