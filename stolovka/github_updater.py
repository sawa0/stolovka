import requests
import zipfile
import os
import sys
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class GitHubUpdater:
    def __init__(self, repo_owner: str, repo_name: str, current_branch: str, config_file: str = 'version.json'):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_branch = current_branch
        self.base_path = Path(__file__).resolve().parent
        self.config_file = self.base_path / config_file
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    def _load_version_info(self) -> Dict:
        """Загрузить информацию о текущей версии из файла"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            'branch': self.current_branch,
            'commit': 'unknown',
            'date': datetime.now().isoformat(),
            'message': 'Initial version'
        }

    def _save_version_info(self, version_info: Dict):
        """Сохранить информацию о версии в файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения версии: {e}")

    def get_current_version(self) -> Dict:
        """Получить текущую версию из конфига"""
        version = self._load_version_info()
        return {
            'commit': version.get('commit', 'unknown'),
            'short_commit': version.get('commit', 'unknown')[:7],
            'date': version.get('date', ''),
            'message': version.get('message', ''),
            'branch': version.get('branch', self.current_branch)
        }

    def get_remote_version(self, branch: str = None) -> Optional[Dict]:
        """Получить последнюю версию из GitHub"""
        if branch is None:
            branch = self.current_branch

        try:
            url = f"{self.api_base}/commits/{branch}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()
            commit = data['sha']
            commit_data = data['commit']

            return {
                'commit': commit,
                'short_commit': commit[:7],
                'date': commit_data['author']['date'],
                'message': commit_data['message'],
                'author': commit_data['author']['name'],
                'branch': branch
            }
        except Exception as e:
            print(f"Ошибка получения версии: {e}")
            return None

    def check_updates(self, branch: str = None) -> Dict:
        """Проверить наличие обновлений"""
        if branch is None:
            branch = self.current_branch

        current = self.get_current_version()
        remote = self.get_remote_version(branch)

        if not remote:
            return {
                'success': False,
                'error': 'Не удалось получить информацию о версии с GitHub'
            }

        has_updates = current['commit'] != remote['commit']

        return {
            'success': True,
            'has_updates': has_updates,
            'current': current,
            'remote': remote
        }

    def get_commit_log(self, from_commit: str, to_commit: str) -> List[Dict]:
        """Получить список коммитов между версиями"""
        try:
            url = f"{self.api_base}/compare/{from_commit}...{to_commit}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return []

            data = response.json()
            commits = []

            for commit in data.get('commits', []):
                commits.append({
                    'commit': commit['sha'],
                    'short_commit': commit['sha'][:7],
                    'date': commit['commit']['author']['date'],
                    'message': commit['commit']['message'],
                    'author': commit['commit']['author']['name']
                })

            return commits
        except Exception as e:
            print(f"Ошибка получения changelog: {e}")
            return []

    def download_and_extract(self, branch: str) -> Dict:
        """Скачать и распаковать архив с GitHub"""
        try:
            # Скачиваем архив
            url = f"{self.api_base}/zipball/{branch}"
            response = requests.get(url, timeout=60, stream=True)

            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Ошибка скачивания: HTTP {response.status_code}'
                }

            # Сохраняем во временный файл
            temp_zip = self.base_path / 'temp_update.zip'
            with open(temp_zip, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Распаковываем
            temp_dir = self.base_path / 'temp_update'
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Находим корневую папку (GitHub добавляет префикс)
            extracted_folders = list(temp_dir.iterdir())
            if not extracted_folders:
                return {
                    'success': False,
                    'error': 'Архив пуст'
                }

            source_dir = extracted_folders[0]

            # Получаем информацию о новой версии
            remote_version = self.get_remote_version(branch)

            return {
                'success': True,
                'source_dir': source_dir,
                'temp_zip': temp_zip,
                'temp_dir': temp_dir,
                'version': remote_version
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка при скачивании: {str(e)}'
            }

    def apply_update(self, source_dir: Path, exclude_files: List[str] = None) -> Dict:
        """Применить обновление (скопировать файлы)"""
        if exclude_files is None:
            exclude_files = ['stolovka.db', 'version.json', 'reports', '__pycache__']

        try:
            # Копируем файлы
            for item in source_dir.iterdir():
                if item.name in exclude_files:
                    continue

                dest = self.base_path / item.name

                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)

            return {'success': True}

        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка при копировании файлов: {str(e)}'
            }

    def cleanup_temp_files(self, temp_zip: Path, temp_dir: Path):
        """Удалить временные файлы"""
        try:
            if temp_zip.exists():
                temp_zip.unlink()
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Ошибка очистки: {e}")

    def update(self, branch: str = None) -> Dict:
        """Выполнить полное обновление"""
        if branch is None:
            branch = self.current_branch

        # Скачиваем
        download_result = self.download_and_extract(branch)
        if not download_result['success']:
            return download_result

        # Применяем обновление
        apply_result = self.apply_update(download_result['source_dir'])

        # Очищаем временные файлы
        self.cleanup_temp_files(
            download_result['temp_zip'],
            download_result['temp_dir']
        )

        if not apply_result['success']:
            return apply_result

        # Сохраняем новую версию
        if download_result['version']:
            self._save_version_info({
                'branch': branch,
                'commit': download_result['version']['commit'],
                'date': download_result['version']['date'],
                'message': download_result['version']['message']
            })

        return {
            'success': True,
            'message': 'Обновление успешно установлено',
            'version': download_result['version']
        }

    def switch_branch(self, branch: str) -> Dict:
        """Переключиться на другую ветку"""
        current_branch = self.get_current_version()['branch']

        if current_branch == branch:
            return {
                'success': False,
                'error': f'Уже используется ветка {branch}'
            }

        # Обновляемся на новую ветку
        result = self.update(branch)

        if result['success']:
            result['from_branch'] = current_branch
            result['to_branch'] = branch

        return result

    def restart_application(self):
        """Перезапустить приложение"""
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    updater = GitHubUpdater('sawa0', 'stolovka', 'AI_Master')

    print("Текущая версия:")
    print(json.dumps(updater.get_current_version(), indent=2, ensure_ascii=False))

    print("\nПроверка обновлений:")
    result = updater.check_updates()
    print(json.dumps(result, indent=2, ensure_ascii=False))
