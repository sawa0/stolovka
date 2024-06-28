import datetime

from flask import *
from flask_socketio import SocketIO, send, emit

from BD import db

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

web_recurces_directory = app.root_path + "/web_recurces"

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

@app.route('/libs/<filename>')
def serve_libs(filename):
    try:
        with open('./web_recurces/JS_WEB_Libs/' + filename) as f:
            return f.read()
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
    emit('new_order', data, broadcast=True)
    
##################################################
#            Обработчик GET запросов             #
##################################################
@flask_web_interface.on('get')
def get_request_handler(data):
#####  запросы страницы настроек  #####
    if data == '':
        ...
    
#####   запросы страницы повара   #####
    elif data == 'transactions':    #   Загрузка списка заказов за сегодня для истории заказов на странице повара
        emit('today_transactions', db.GetTodayTtransactions())

#####   запросы страницы заказа   #####

    elif data == 'users':   #   Загрузка списка пользователей на странице заказа  
        answer = []
        for user in db.LoadUserList():  #   Очистка списка от не активных пользователей
            if user[2]:
                answer.append([user[0], user[1]])
        emit('users', answer)   #   Отправка списка пользователей в браузер
        
    elif data == 'menu':    #   Загрузка меню за сегодя, и вчера, на страницу заказа  
        current_date = datetime.datetime.now().weekday()
        current_week = f"{datetime.date.today().year}-W{datetime.date.today().isocalendar()[1]:02d}"
        data = {}
        if current_date < 5:    #   если сегодня будний день
            if current_date:    #   если сегодня не понедельник (истина - всё что отличается от нуля)
                data['previous_dey_data'] = db.GetMemu(current_week)[current_date - 1]  #   загрузить меню на предыдущий день 
            data['today_data'] = db.GetMemu(current_week)[current_date] #   загрузить меню на сегодня
        data['dishes'] = db.GetDishDict()
        emit('menu', data)  #   отправить данные в браузер
        
@flask_web_interface.on('get_week_menu')
def get_week_menu(data):    #   передаёт в браузер [номер недели, меню на неделю, список названий активных блюд]
    emit('week_menu', [data, db.GetMemu(data), db.GetDishDict()])
    
@flask_web_interface.on('menu_update')
def menu_update(data):
    db.UpdateMenu(data[0], data[1])
    emit('week_menu', [data[0], db.GetMemu(data[0]), db.GetDishDict()])    #   Отправляем событие с обновленным недельным меню в браузер

@flask_web_interface.on('getUsers')
def getUsers():
    emit('users', db.LoadUserList())
    
@flask_web_interface.on('newUserName')
def newUserName(data):
    db.NewUser(data)
    emit('users', db.LoadUserList())
    
@flask_web_interface.on('EditUserName')
def EditUserName(data):
    db.EditUserName(data[0], data[1])
    emit('users', db.LoadUserList())
    
@flask_web_interface.on('DeleteUser')
def DeleteUser(data):
    db.DeleteUser(data)
    emit('users', db.LoadUserList())
    
@flask_web_interface.on('ChangeUserStatus')
def ChangeUserStatus(data):
    db.ChangeUserStatus(data)
    emit('users', db.LoadUserList())

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
    dish_info['ingridients'] = db.GetIngredientsDict()

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


##################################################
#                 запуск сервера                 #        
##################################################        
if __name__ == '__main__':
    flask_web_interface.run(app, debug=False, port="8080", host="0.0.0.0")
##################################################

