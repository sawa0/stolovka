from flask import *

import html_builder
from BD import db


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        if 'letter' in request.form:
            return html_builder.letter(request.form['letter'])
        if 'user' in request.form:
            return html_builder.menu(request.form['user'])
        if 'order' in request.form:
            print(request.form['order'])
            return request.form['order']
        
    if request.method == 'GET':
        return html_builder.main()

# @app.route('/povar')
# def povar_page():
#     return render_template('povar.html')

@app.route('/config', methods=['GET', 'POST'])
def SettingsPage():
    
    def notification(data):
        return f"""const notification = new NotificationCustom('{data[0]}','{data[1]}');
                   notification.show();"""

    if request.method == 'POST':
        
        if 'Page' in request.form:
            return html_builder.conf(request.form['Page'])  #   Редирект на выбранную страницу
        
        #######################\   Обработчик страницы dish_list  /#######################
        
        elif 'NewDish' in request.form:

            return html_builder.conf('dish_list', notification(db.NewDish(request.form['NewDish'])))
        
        elif 'DeleteDish' in request.form:
            db.DeleteDish(request.form['DeleteDish'])

            return html_builder.conf('dish_list', "")

        elif 'ChangeDishStatus' in request.form:
            db.ChangeDishStatus(request.form['ChangeDishStatus'])

            return html_builder.conf('dish_list', "")
        
        elif 'EditDishName' in request.form:
            return html_builder.conf('dish_list', notification(db.EditDishName(request.form['EditDishName'], request.form['id'])))
        
        #########################\  Обработчик страницы users   /##########################

        elif 'NewUser' in request.form:

            return html_builder.conf('users', notification(db.NewUser(request.form['NewUser'])))
        
        elif 'DeleteUser' in request.form:
            db.DeleteUser(request.form['DeleteUser'])

            return html_builder.conf('users', "")
        
        elif 'ChangeUserStatus' in request.form:
            db.ChangeStatus(request.form['ChangeUserStatus'])

            return html_builder.conf('users', "")
        
        elif 'EditUserName' in request.form:
            return html_builder.conf('users', notification(db.EditUserName(request.form['EditUserName'], request.form['id'])))

        ######################\   Oбработчик страницы menu   /#############################

        elif 'GetMemu' in request.form:
            return html_builder.conf('menu', "", request.form['GetMemu'])
        
        elif 'Memu' in request.form:
            db.UpdateMenu(request.form['Memu'], request.form['Week'])
            return html_builder.conf('menu', notification(["Успех", "Меню на неделю сохранено!"]), request.form['Week'])
        
    if request.method == 'GET':
        print("get")
        return html_builder.conf("menu", "")    #  Редирект на страницу по умолчанию

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="8080")
