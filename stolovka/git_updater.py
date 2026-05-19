import subprocess
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class GitUpdater:
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.path.dirname(os.path.abspath(__file__))

    def _run_git_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """Выполнить git команду и вернуть результат"""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Git command timeout"
        except Exception as e:
            return False, "", str(e)

    def get_current_branch(self) -> Optional[str]:
        """Получить текущую ветку"""
        success, stdout, stderr = self._run_git_command(['branch', '--show-current'])
        if success:
            return stdout
        return None

    def get_current_version(self) -> Optional[Dict]:
        """Получить информацию о текущей версии"""
        success, stdout, stderr = self._run_git_command([
            'log', '-1', '--format=%H|%at|%s|%an'
        ])

        if not success:
            return None

        try:
            commit_hash, timestamp, message, author = stdout.split('|', 3)
            return {
                'commit': commit_hash,
                'short_commit': commit_hash[:7],
                'timestamp': int(timestamp),
                'date': datetime.fromtimestamp(int(timestamp)).isoformat(),
                'message': message,
                'author': author,
                'branch': self.get_current_branch()
            }
        except Exception:
            return None

    def get_remote_version(self, branch: str = None) -> Optional[Dict]:
        """Получить информацию о версии из удаленной ветки"""
        if branch is None:
            branch = self.get_current_branch()

        if not branch:
            return None

        success, stdout, stderr = self._run_git_command([
            'log', f'origin/{branch}', '-1', '--format=%H|%at|%s|%an'
        ])

        if not success:
            return None

        try:
            commit_hash, timestamp, message, author = stdout.split('|', 3)
            return {
                'commit': commit_hash,
                'short_commit': commit_hash[:7],
                'timestamp': int(timestamp),
                'date': datetime.fromtimestamp(int(timestamp)).isoformat(),
                'message': message,
                'author': author,
                'branch': branch
            }
        except Exception:
            return None

    def check_local_changes(self) -> Tuple[bool, List[str]]:
        """Проверить наличие локальных изменений"""
        success, stdout, stderr = self._run_git_command(['status', '--porcelain'])

        if not success:
            return False, []

        changes = [line.strip() for line in stdout.split('\n') if line.strip()]
        return len(changes) > 0, changes

    def fetch_updates(self) -> bool:
        """Получить обновления с удаленного репозитория"""
        success, stdout, stderr = self._run_git_command(['fetch', 'origin'])
        return success

    def check_updates(self) -> Dict:
        """Проверить наличие обновлений для текущей ветки"""
        current_branch = self.get_current_branch()

        if not current_branch:
            return {
                'success': False,
                'error': 'Не удалось определить текущую ветку'
            }

        if not self.fetch_updates():
            return {
                'success': False,
                'error': 'Не удалось получить обновления с сервера'
            }

        current = self.get_current_version()
        remote = self.get_remote_version(current_branch)

        if not current or not remote:
            return {
                'success': False,
                'error': 'Не удалось получить информацию о версиях'
            }

        has_updates = current['commit'] != remote['commit']
        has_local_changes, changes = self.check_local_changes()

        return {
            'success': True,
            'has_updates': has_updates,
            'current': current,
            'remote': remote,
            'has_local_changes': has_local_changes,
            'local_changes': changes
        }

    def get_commit_log(self, from_commit: str, to_commit: str) -> List[Dict]:
        """Получить список коммитов между двумя версиями"""
        success, stdout, stderr = self._run_git_command([
            'log', f'{from_commit}..{to_commit}', '--format=%H|%at|%s|%an'
        ])

        if not success:
            return []

        commits = []
        for line in stdout.split('\n'):
            if not line.strip():
                continue

            try:
                commit_hash, timestamp, message, author = line.split('|', 3)
                commits.append({
                    'commit': commit_hash,
                    'short_commit': commit_hash[:7],
                    'timestamp': int(timestamp),
                    'date': datetime.fromtimestamp(int(timestamp)).isoformat(),
                    'message': message,
                    'author': author
                })
            except Exception:
                continue

        return commits

    def pull_updates(self) -> Dict:
        """Скачать и применить обновления для текущей ветки"""
        current_branch = self.get_current_branch()

        if not current_branch:
            return {
                'success': False,
                'error': 'Не удалось определить текущую ветку'
            }

        has_local_changes, changes = self.check_local_changes()
        if has_local_changes:
            return {
                'success': False,
                'error': 'Есть локальные изменения. Сохраните или отмените их перед обновлением.',
                'local_changes': changes
            }

        success, stdout, stderr = self._run_git_command(['pull', 'origin', current_branch])

        if not success:
            return {
                'success': False,
                'error': f'Ошибка при обновлении: {stderr}'
            }

        return {
            'success': True,
            'message': 'Обновление успешно применено',
            'output': stdout
        }

    def switch_branch(self, branch: str) -> Dict:
        """Переключиться на другую ветку и обновить её"""
        current_branch = self.get_current_branch()

        if current_branch == branch:
            return {
                'success': False,
                'error': f'Уже находитесь на ветке {branch}'
            }

        has_local_changes, changes = self.check_local_changes()
        if has_local_changes:
            return {
                'success': False,
                'error': 'Есть локальные изменения. Сохраните или отмените их перед переключением.',
                'local_changes': changes
            }

        if not self.fetch_updates():
            return {
                'success': False,
                'error': 'Не удалось получить обновления с сервера'
            }

        success, stdout, stderr = self._run_git_command(['checkout', branch])
        if not success:
            return {
                'success': False,
                'error': f'Ошибка при переключении ветки: {stderr}'
            }

        success, stdout, stderr = self._run_git_command(['pull', 'origin', branch])
        if not success:
            return {
                'success': False,
                'error': f'Ошибка при обновлении ветки: {stderr}'
            }

        return {
            'success': True,
            'message': f'Успешно переключено на ветку {branch}',
            'from_branch': current_branch,
            'to_branch': branch
        }

    def restart_application(self):
        """Перезапустить приложение"""
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    updater = GitUpdater()

    print("Текущая ветка:", updater.get_current_branch())
    print("\nТекущая версия:")
    print(json.dumps(updater.get_current_version(), indent=2, ensure_ascii=False))

    print("\nПроверка обновлений:")
    result = updater.check_updates()
    print(json.dumps(result, indent=2, ensure_ascii=False))
