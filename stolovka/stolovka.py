print("""#################################
 * http://127.0.0.1:8080/config
 * http://127.0.0.1:8080/povar
#################################""")

import datetime, os, sys, subprocess, requests
from timeit import repeat

from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path

from flask import *
from flask_socketio import SocketIO, send, emit

from BD import db
from config import HOST, PORT, DEBUG, REPORTS_DIR, REPORT_SCHEDULE_DAY, REPORT_SCHEDULE_HOUR, REPORT_SCHEDULE_MINUTE, WEB_RESOURCES_DIR, WEB_LIBS_DIR, GIT_CONFIG
from github_updater import GitHubUpdater

def previous_month_report_autosend():
    if db.GetTGReportAutosend():
        def get_prev_month():
            now = datetime.datetime.now()

            year = now.year
            month = now.month - 1

            if month == 0:
                month = 12
                year -= 1

            return f"{year}-{month:02d}"

        def get_report_path(report_month):
            base_path = Path(__file__).resolve().parent
            report_path = base_path / "reports" / report_month
            return report_path

        def send_report(bot_token, user_id, file_path):
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

            with open(file_path, "rb") as f:
                response = requests.post(
                    url,
                    data={"chat_id": user_id,
                          "caption": "Отчёт за прошедший месяц"},
                    files={"document": f}
                )

            return response.json()

        TGSettings = db.GetTGReportAutosendParametrs()

        from excel import create_excel_report
        repeat_path = get_report_path(create_excel_report(db.GetReports(get_prev_month(), 0)))

        result = send_report(TGSettings['bot_api_key'], TGSettings['tg_user_id'], repeat_path)
        #print(result)

scheduler = BackgroundScheduler()
scheduler.add_job(
    previous_month_report_autosend,
    trigger='cron',
    day=REPORT_SCHEDULE_DAY,
    hour=REPORT_SCHEDULE_HOUR,
    minute=REPORT_SCHEDULE_MINUTE
)
scheduler.start()

app = Flask(__name__)
flask_web_interface = SocketIO(app) #   Flask app

@app.route('/favicon.ico')  #   Иконка на вкладке браузера
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='favicon.ico')

##############################################
#                 page loading               #
##############################################

@app.route('/config')
def SettingsPage():
    with open('./web_recurces/config.html') as f:
        return f.read()

@app.route('/povar')
def povar_page():
    with open('./web_recurces/povar.html') as f:
        return f.read()
    
@app.route('/')
def main_page():
    with open('./web_recurces/main.html') as f:
        return f.read()

##############################################
#                files loading               #
##############################################

web_recurces_directory = WEB_RESOURCES_DIR

@app.route('/<filename>.css')
def css_files(filename):
    try:
        return send_from_directory(web_recurces_directory, f"{filename}.css")
    except FileNotFoundError:
        abort(404)

@app.route('/<filename>.js')
def JS_files(filename):
    try:
        return send_from_directory(web_recurces_directory, f"{filename}.js")
    except FileNotFoundError:
        abort(404)

##############################################
#       Обработка отправки JS библиотек      #
##############################################

web_libs_directory = WEB_LIBS_DIR

@app.route('/libs/<filename>')
def serve_libs(filename):
    try:
        return send_from_directory(web_libs_directory, filename)
    except FileNotFoundError:
        abort(404)


#####################################################
#         обработка событий отправки/приема         #
#   данных о новом закакзе, и о решении по заказу   #
#####################################################
        
@flask_web_interface.on('decision')     #   Отправка решения о принятии/отказе заказа на страницу Заказа
def order_decision(data):
    if data['decision'] == 'accept':
        db.NewTransaction(data['order'])
        emit('today_transactions', db.GetTodayTtransactions())
    emit('decision', data['decision'], broadcast=True)

@flask_web_interface.on('new_order')    #   Отправка нового заказа на страницу Повара
def new_order(data):
    ConfirmationType = db.GetOrderConfirmationType()
    if ConfirmationType[0] == "off":
        db.NewTransaction(data)
        emit('decision', 'accept', broadcast=True)
        emit('today_transactions', db.GetTodayTtransactions(), broadcast=True)
    emit('new_order', [ConfirmationType, data], broadcast=True)
    
##################################################
#            Обработчик GET запросов             #
##################################################    
@flask_web_interface.on('get')
def get_request_handler(data):
#####   запросы страницы повара   #####
    if data == 'transactions':    #   Загрузка списка заказов за сегодня для истории заказов на странице повара
        emit('today_transactions', db.GetTodayTtransactions())

#####   запросы страницы заказа   #####

    elif data == 'users':       #   Загрузка списка пользователей на странице заказа  
        answer = []
        for user in db.GetUserList():  #   Очистка списка от не активных пользователей
            if user[2]:
                answer.append([user[0], user[1]])
        emit('users', answer)   #   Отправка списка пользователей в браузер
        
    elif data == 'menu':
        today = datetime.date.today()
        weekday_idx = today.weekday()  # 0=понедельник, 6=воскресенье

        # ISO-неделя
        iso_year, iso_week, _ = today.isocalendar()
        current_week = f"{iso_year}-W{iso_week:02d}"

        data = {}
        week_menu = db.GetMemu(current_week)  # список меню на неделю (0=Пн, 1=Вт ...)

        # Загрузка меню только для будних дней
        if weekday_idx < 5:
            # предыдущий день (если не понедельник)
            if weekday_idx > 0:
                data['previous_day_data'] = week_menu[weekday_idx - 1]
            # сегодня
            data['today_data'] = week_menu[weekday_idx]

        # Остальные данные
        data['dishes'] = db.GetDishDict()
        data['regular'] = db.GetRegularMenu()

        emit('menu', data)

        
#####   запросы страницы настроек   #####
        
@flask_web_interface.on('get_week_menu')
def get_week_menu(data):    #   передаёт в браузер [номер недели, меню на неделю, список названий активных блюд]
    emit('week_menu', [data, db.GetMemu(data), db.GetDishDict(), db.GetRegularMenu(), db.GetPrintFlag()])
    
@flask_web_interface.on('menu_update')
def menu_update(data):
    db.UpdateMenu(data[0], data[1])
    get_week_menu(data[0])    #   Отправляем событие с обновленным недельным меню в браузер
    
@flask_web_interface.on('regular_menu_update')
def regular_menu_update(data):
    db.UpdateRegularMenu(data[1])
    get_week_menu(data[0])
    

@flask_web_interface.on('getUsers')
def getUsers():
    emit('users', db.GetUserList())
    
@flask_web_interface.on('newUserName')
def newUserName(data):
    db.NewUser(data)
    emit('users', db.GetUserList())
    
@flask_web_interface.on('EditUserName')
def EditUserName(data):
    db.EditUserName(data[0], data[1])
    emit('users', db.GetUserList())
    
@flask_web_interface.on('DeleteUser')
def DeleteUser(data):
    db.DeleteUser(data)
    emit('users', db.GetUserList())
    
@flask_web_interface.on('ChangeUserStatus')
def ChangeUserStatus(data):
    db.ChangeUserStatus(data)
    emit('users', db.GetUserList())

@flask_web_interface.on('getPurchase')
def getPurchase():
    emit('Purchase', db.GetIngredientsList())
    
@flask_web_interface.on('newPrice')
def newPrice(data):
    db.NewPrice(data[0], data[1])
    emit('Purchase', db.GetIngredientsList())
    
@flask_web_interface.on('NewIngredient')
def NewIngredient(data):
    db.NewIngredient(data[0], data[1], data[2])
    emit('Purchase', db.GetIngredientsList())
    
@flask_web_interface.on('UpdateIngredientName')
def UpdateIngredientName(data):
    db.EditIngredientName(data[0], data[1])
    emit('Purchase', db.GetIngredientsList())

@flask_web_interface.on('DeleteIngredient')
def DeleteIngredient(data):
    db.DeleteIngredient(data)
    emit('Purchase', db.GetIngredientsList())
    
@flask_web_interface.on('getDishList')
def getDishList():
    emit("Dishes", db.GetDishList())
    
@flask_web_interface.on('ChangeDishStatus')
def ChangeDishStatus(data):
    db.ChangeDishStatus(data)
    emit("Dishes", db.GetDishList())
    
@flask_web_interface.on('NewDish')
def ChangeDishStatus(data):
    db.NewDish(data)
    emit("Dishes", db.GetDishList())
    
@flask_web_interface.on('EditDishName')
def EditDishName(data):
    db.EditDishName(data[0], data[1])
    emit("Dishes", db.GetDishList())
    
@flask_web_interface.on('DeleteDish')
def DeleteDish(data):
    db.DeleteDish(data)
    emit("Dishes", db.GetDishList())
    
@flask_web_interface.on('GetRecipe')
def GetRecipe(data):
    dish_info = db.GetDishInfo(data)
    dish_info['ingredients'] = db.GetIngredientsDict()

    emit("Recipe", dish_info)
    
@flask_web_interface.on('DeleteIngredientFromRecipe')
def DeleteIngredientFromRecipe(data):
    db.DeleteIngredientFromRecipe(data['DishID'], data['IngredientID'])
    GetRecipe(data['DishID'])
    
@flask_web_interface.on('AddIngredientToRecipe')
def AddIngredientToRecipe(data):
    db.AddIngredientToRecipe(data['DishID'], data['IngredientID'], data['IngredientName'], data['volume'])
    GetRecipe(data['DishID'])

@flask_web_interface.on('EditVolume')
def EditVolume(data):
    db.IngredientVolumeEdit(data['DishID'], data['IngredientID'], data['Volume'])
    GetRecipe(data['DishID'])

@flask_web_interface.on('DownloadRecipe')
def DownloadRecipe(data):
    dish_info = db.GetDishInfo(data['DishID'])
    dish_info['ingredients'] = db.GetIngredientsDict()

    from excel import create_excel_recipe
    emit("DownloadReport", create_excel_recipe(dish_info))

@flask_web_interface.on('getReports')
def GetReports(data):
    emit("Reports", [data, db.GetUserList(), db.GetReports(data)])
    
@flask_web_interface.on('DownloadReport')
def DownloadMonthlyReport(data):
    data = db.GetReports(data[0], data[1])

    from excel import create_excel_report
    emit("DownloadReport", create_excel_report(data))

@app.route('/reports/<filename>')
def download_file(filename):
    file_path = os.path.join(REPORTS_DIR, filename)

    if not os.path.isfile(file_path):
        return 'File not found', 404

    return send_file(file_path, mimetype=filename)

@flask_web_interface.on('DayReportDetails')
def DayReportDetails(data):
    emit("DayReportDetails", db.GetReports(data[0], data[1]))
    
@flask_web_interface.on('DeleteOrder')
def DeleteOrder(data):
    db.DeleteOrder(data[0])
    emit("DayReportDetails", db.GetReports(data[1][0], data[1][1]))
    
@flask_web_interface.on('DayReportDelete')
def DayReportDelete(data):
    db.DeleteDayReport(data)
    emit("Reports", [data[0][:7], db.GetUserList(), db.GetReports(data[0][:7])])
    
@flask_web_interface.on('getSettings')
def getSettings():
    data = {
            'OrderConfirmation':db.GetOrderConfirmationType(),
            'TGReportAutosendParametrs':db.GetTGReportAutosendParametrs(),
            'TGReportAutosend':db.GetTGReportAutosend(),
        }

    emit("Settings", data)
    
@flask_web_interface.on('updateSettings')
def updateSettings(data):
    db.UpdateSettings(data[0], data[1])
    getSettings()
    
@flask_web_interface.on('IngredientPriceEditFromRecipe')
def IngredientPriceEditFromRecipe(data):
    db.NewPrice(data['ingredientID'], data['newPrice'])
    GetRecipe(data['DishID'])

@flask_web_interface.on('print_flag_change')
def print_flag_change(data):
    db.PrintFlagChange(data)

@flask_web_interface.on('app_update')
def app_update():
    print("update")

    # update()
    # emit('reboot', broadcast=True)
    
    # python = sys.executable
    # script = os.path.abspath(sys.argv[0])

    # subprocess.Popen([python, script], creationflags=subprocess.CREATE_NEW_CONSOLE)
    # sys.exit()


# def update():

#     import requests
#     import zipfile
#     import os
#     import shutil
#     from io import BytesIO

#     # Настройки
#     INSTALL_PATH = "C:\\Users\\sawa\\desktop\\stolovka"  # Куда копировать файлы
#     BRANCH = "main"  # Ветка, откуда скачивать, если нет релизов

#     # Получение последнего релиза
#     url = "https://api.github.com/repos/sawa0/stolovka/releases/latest"
#     response = requests.get(url)
#     release_data = response.json()

#     # Скачивание архива
#     response = requests.get(release_data["zipball_url"])
#     if response.status_code == 200:
#         zip_file = zipfile.ZipFile(BytesIO(response.content))
#         extract_path = "temp_repo"
#         zip_file.extractall(extract_path)
#         zip_file.close()

#         # Поиск корневой папки (GitHub добавляет префикс в названии)
#         repo_folder = next(os.scandir(extract_path)).path
    
#         # Удаляем старые файлы, кроме определённых (если надо)
#         for item in os.listdir(INSTALL_PATH):
#             item_path = os.path.join(INSTALL_PATH, item)
#             if os.path.isdir(item_path):
#                 shutil.rmtree(item_path)
#             else:
#                 os.remove(item_path)
    
#         # Копируем новые файлы
#         for item in os.listdir(repo_folder):
#             shutil.move(os.path.join(repo_folder, item), INSTALL_PATH)
    
#         # Чистим временные файлы
#         shutil.rmtree(extract_path)
#         print("Обновление завершено!")
#     else:
#         print("Ошибка загрузки архива!")

##################################################
#            Git Update API endpoints            #
##################################################

# Инициализация GitHub updater
github_updater = GitHubUpdater(
    repo_owner='sawa0',
    repo_name='stolovka',
    current_branch=GIT_CONFIG['experimental_branch']  # По умолчанию AI_Master
)

@app.route('/api/update/status', methods=['GET'])
def update_status():
    """Получить текущую ветку и версию"""
    current = github_updater.get_current_version()
    if not current:
        return jsonify({'success': False, 'error': 'Не удалось получить информацию о версии'}), 500

    return jsonify({
        'success': True,
        'current': current,
        'config': {
            'stable_branch': GIT_CONFIG['stable_branch'],
            'experimental_branch': GIT_CONFIG['experimental_branch']
        }
    })

@app.route('/api/update/check', methods=['GET'])
def check_updates():
    """Проверить наличие обновлений для текущей ветки"""
    current_branch = github_updater.get_current_version()['branch']
    result = github_updater.check_updates(current_branch)
    return jsonify(result)

@app.route('/api/update/execute', methods=['POST'])
def execute_update():
    """Выполнить обновление текущей ветки"""
    current_branch = github_updater.get_current_version()['branch']
    result = github_updater.update(current_branch)

    if result['success']:
        # Отправляем уведомление через WebSocket
        flask_web_interface.emit('update_status', {
            'status': 'completed',
            'message': 'Обновление успешно завершено. Перезапуск приложения...'
        })

        # Перезапуск приложения через 2 секунды
        import threading
        def delayed_restart():
            import time
            time.sleep(2)
            github_updater.restart_application()

        threading.Thread(target=delayed_restart, daemon=True).start()

    return jsonify(result)

@app.route('/api/update/switch', methods=['POST'])
def switch_branch():
    """Переключиться на другую ветку"""
    data = request.get_json()
    branch = data.get('branch')

    if not branch:
        return jsonify({'success': False, 'error': 'Не указана ветка'}), 400

    if branch not in [GIT_CONFIG['stable_branch'], GIT_CONFIG['experimental_branch']]:
        return jsonify({'success': False, 'error': 'Недопустимая ветка'}), 400

    result = github_updater.switch_branch(branch)

    if result['success']:
        # Отправляем уведомление через WebSocket
        flask_web_interface.emit('update_status', {
            'status': 'completed',
            'message': f'Переключено на ветку {branch}. Перезапуск приложения...'
        })

        # Перезапуск приложения через 2 секунды
        import threading
        def delayed_restart():
            import time
            time.sleep(2)
            github_updater.restart_application()

        threading.Thread(target=delayed_restart, daemon=True).start()

    return jsonify(result)

@app.route('/api/update/changelog/<from_commit>/<to_commit>', methods=['GET'])
def get_changelog(from_commit, to_commit):
    """Получить список изменений между коммитами"""
    commits = github_updater.get_commit_log(from_commit, to_commit)
    return jsonify({
        'success': True,
        'commits': commits
    })

##################################################
#         WebSocket события для обновлений       #
##################################################

@flask_web_interface.on('update_check')
def handle_update_check():
    """Обработка запроса проверки обновлений через WebSocket"""
    emit('update_status', {'status': 'checking', 'message': 'Проверка обновлений...'})
    current_branch = github_updater.get_current_version()['branch']
    result = github_updater.check_updates(current_branch)
    emit('update_check_result', result)

@flask_web_interface.on('update_execute')
def handle_update_execute():
    """Обработка запроса выполнения обновления через WebSocket"""
    emit('update_status', {'status': 'downloading', 'message': 'Скачивание обновлений...'})
    current_branch = github_updater.get_current_version()['branch']
    result = github_updater.update(current_branch)

    if result['success']:
        emit('update_status', {'status': 'restarting', 'message': 'Перезапуск приложения...'})

        import threading
        def delayed_restart():
            import time
            time.sleep(2)
            github_updater.restart_application()

        threading.Thread(target=delayed_restart, daemon=True).start()
    else:
        emit('update_status', {'status': 'error', 'message': result.get('error', 'Неизвестная ошибка')})


##################################################
#                 запуск сервера                 #
##################################################
if __name__ == '__main__':
    flask_web_interface.run(app, debug=DEBUG, port=PORT, host=HOST)
##################################################


