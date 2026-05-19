// Модуль управления обновлениями приложения из Git

class UpdateManager {
    constructor() {
        this.currentStatus = null;
        this.updateInProgress = false;
    }

    async getCurrentStatus() {
        try {
            const response = await fetch('/api/update/status');
            const data = await response.json();

            if (data.success) {
                this.currentStatus = data;
                return data;
            } else {
                throw new Error(data.error || 'Не удалось получить статус');
            }
        } catch (error) {
            console.error('Ошибка получения статуса:', error);
            throw error;
        }
    }

    async checkForUpdates() {
        try {
            const response = await fetch('/api/update/check');
            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Не удалось проверить обновления');
            }

            return data;
        } catch (error) {
            console.error('Ошибка проверки обновлений:', error);
            throw error;
        }
    }

    async executeUpdate() {
        if (this.updateInProgress) {
            throw new Error('Обновление уже выполняется');
        }

        try {
            this.updateInProgress = true;

            const response = await fetch('/api/update/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (!data.success) {
                this.updateInProgress = false;
                throw new Error(data.error || 'Не удалось выполнить обновление');
            }

            return data;
        } catch (error) {
            this.updateInProgress = false;
            console.error('Ошибка выполнения обновления:', error);
            throw error;
        }
    }

    async switchBranch(branch) {
        if (this.updateInProgress) {
            throw new Error('Обновление уже выполняется');
        }

        try {
            this.updateInProgress = true;

            const response = await fetch('/api/update/switch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ branch })
            });

            const data = await response.json();

            if (!data.success) {
                this.updateInProgress = false;
                throw new Error(data.error || 'Не удалось переключить ветку');
            }

            return data;
        } catch (error) {
            this.updateInProgress = false;
            console.error('Ошибка переключения ветки:', error);
            throw error;
        }
    }

    async getChangelog(fromCommit, toCommit) {
        try {
            const response = await fetch(`/api/update/changelog/${fromCommit}/${toCommit}`);
            const data = await response.json();

            if (!data.success) {
                throw new Error('Не удалось получить список изменений');
            }

            return data.commits;
        } catch (error) {
            console.error('Ошибка получения changelog:', error);
            throw error;
        }
    }

    formatDate(isoDate) {
        const date = new Date(isoDate);
        return date.toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    getBranchDisplayName(branch, config) {
        if (branch === config.stable_branch) {
            return 'Стабильная';
        } else if (branch === config.experimental_branch) {
            return 'Экспериментальная';
        }
        return branch;
    }
}

// UI компоненты для управления обновлениями

class UpdateUI {
    constructor(updateManager, socketManager) {
        this.updateManager = updateManager;
        this.socket = socketManager;
        this.container = null;
    }

    createVersionInfo(versionData, config) {
        const branchName = this.updateManager.getBranchDisplayName(versionData.branch, config);

        return `
            <div class="version-info">
                <div class="version-row">
                    <span class="version-label">Текущая версия:</span>
                    <span class="version-value">${branchName}</span>
                </div>
                <div class="version-row">
                    <span class="version-label">Коммит:</span>
                    <span class="version-value">${versionData.short_commit}</span>
                </div>
                <div class="version-row">
                    <span class="version-label">Дата:</span>
                    <span class="version-value">${this.updateManager.formatDate(versionData.date)}</span>
                </div>
                <div class="version-row">
                    <span class="version-label">Сообщение:</span>
                    <span class="version-value">${versionData.message}</span>
                </div>
            </div>
        `;
    }

    createBranchSelector(currentBranch, config) {
        const isStable = currentBranch === config.stable_branch;

        return `
            <div class="branch-selector">
                <h3>Выбор версии</h3>
                <div class="branch-buttons">
                    <button class="branch-btn ${isStable ? 'active' : ''}" data-branch="${config.stable_branch}">
                        Стабильная (${config.stable_branch})
                    </button>
                    <button class="branch-btn ${!isStable ? 'active' : ''}" data-branch="${config.experimental_branch}">
                        Экспериментальная (${config.experimental_branch})
                    </button>
                </div>
            </div>
        `;
    }

    createUpdateControls(hasUpdates, hasLocalChanges) {
        let content = '<div class="update-controls">';

        if (hasLocalChanges) {
            content += `
                <div class="warning-message">
                    ⚠️ Обнаружены локальные изменения. Сохраните или отмените их перед обновлением.
                </div>
            `;
        }

        content += `
            <button id="check-updates-btn" class="update-btn">
                Проверить обновления
            </button>
        `;

        if (hasUpdates && !hasLocalChanges) {
            content += `
                <button id="execute-update-btn" class="update-btn primary">
                    Обновить сейчас
                </button>
            `;
        }

        content += '</div>';
        return content;
    }

    createChangelogView(commits) {
        if (!commits || commits.length === 0) {
            return '<div class="changelog-empty">Нет изменений</div>';
        }

        let html = '<div class="changelog"><h3>Список изменений:</h3><ul class="changelog-list">';

        commits.forEach(commit => {
            html += `
                <li class="changelog-item">
                    <span class="commit-hash">${commit.short_commit}</span>
                    <span class="commit-date">${this.updateManager.formatDate(commit.date)}</span>
                    <span class="commit-message">${commit.message}</span>
                    <span class="commit-author">${commit.author}</span>
                </li>
            `;
        });

        html += '</ul></div>';
        return html;
    }

    createProgressIndicator(message) {
        return `
            <div class="update-progress">
                <div class="spinner"></div>
                <div class="progress-message">${message}</div>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    async render(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error('Container not found:', containerId);
            return;
        }

        try {
            const status = await this.updateManager.getCurrentStatus();
            const checkResult = await this.updateManager.checkForUpdates();

            let html = '<div class="update-panel">';
            html += '<h2>Управление обновлениями</h2>';
            html += this.createVersionInfo(status.current, status.config);
            html += this.createBranchSelector(status.current.branch, status.config);

            if (checkResult.has_updates) {
                html += '<div class="update-available">✓ Доступны обновления</div>';

                const changelog = await this.updateManager.getChangelog(
                    checkResult.current.commit,
                    checkResult.remote.commit
                );
                html += this.createChangelogView(changelog);
            } else {
                html += '<div class="update-none">✓ Установлена последняя версия</div>';
            }

            html += this.createUpdateControls(
                checkResult.has_updates,
                checkResult.has_local_changes
            );
            html += '</div>';

            this.container.innerHTML = html;
            this.attachEventListeners(status.config);
            this.setupWebSocketListeners();

        } catch (error) {
            this.container.innerHTML = `
                <div class="error-message">
                    Ошибка загрузки информации об обновлениях: ${error.message}
                </div>
            `;
        }
    }

    attachEventListeners(config) {
        const checkBtn = document.getElementById('check-updates-btn');
        if (checkBtn) {
            checkBtn.addEventListener('click', () => this.handleCheckUpdates());
        }

        const updateBtn = document.getElementById('execute-update-btn');
        if (updateBtn) {
            updateBtn.addEventListener('click', () => this.handleExecuteUpdate());
        }

        const branchBtns = document.querySelectorAll('.branch-btn');
        branchBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const branch = e.target.dataset.branch;
                const currentBranch = document.querySelector('.branch-btn.active').dataset.branch;

                if (branch !== currentBranch) {
                    this.handleSwitchBranch(branch);
                }
            });
        });
    }

    setupWebSocketListeners() {
        if (!this.socket) return;

        this.socket.on('update_status', (data) => {
            if (data.status === 'restarting') {
                this.showNotification('Приложение перезапускается...', 'info');
            } else if (data.status === 'error') {
                this.showNotification(data.message, 'error');
            }
        });
    }

    async handleCheckUpdates() {
        try {
            this.showNotification('Проверка обновлений...', 'info');
            await this.render(this.container.id);
        } catch (error) {
            this.showNotification('Ошибка проверки обновлений: ' + error.message, 'error');
        }
    }

    async handleExecuteUpdate() {
        if (!confirm('Начать обновление? Приложение будет перезапущено.')) {
            return;
        }

        try {
            this.container.innerHTML = this.createProgressIndicator('Выполняется обновление...');
            await this.updateManager.executeUpdate();
            this.showNotification('Обновление запущено. Ожидайте перезапуска...', 'success');
        } catch (error) {
            this.showNotification('Ошибка обновления: ' + error.message, 'error');
            await this.render(this.container.id);
        }
    }

    async handleSwitchBranch(branch) {
        if (!confirm(`Переключиться на другую версию? Приложение будет перезапущено.`)) {
            return;
        }

        try {
            this.container.innerHTML = this.createProgressIndicator('Переключение версии...');
            await this.updateManager.switchBranch(branch);
            this.showNotification('Переключение выполнено. Ожидайте перезапуска...', 'success');
        } catch (error) {
            this.showNotification('Ошибка переключения: ' + error.message, 'error');
            await this.render(this.container.id);
        }
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { UpdateManager, UpdateUI };
}
