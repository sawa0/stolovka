import os

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'stolovka.db')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
WEB_RESOURCES_DIR = os.path.join(BASE_DIR, 'web_recurces')
WEB_LIBS_DIR = os.path.join(WEB_RESOURCES_DIR, 'JS_Libs')

# Настройки сервера
HOST = '0.0.0.0'
PORT = 8080
DEBUG = False

# Настройки планировщика отчетов
REPORT_SCHEDULE_DAY = 1
REPORT_SCHEDULE_HOUR = 12
REPORT_SCHEDULE_MINUTE = 0

# Настройки цен
PRICE_MARKUP = 1.11  # Наценка 11%
