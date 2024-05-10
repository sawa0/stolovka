from flask import *

import html_builder
from BD import db


app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
        
        #######################\   Обработчик страницы purchase   /#######################
        
        elif 'NewIngredientName' in request.form:
            return html_builder.conf('purchase', notification(db.NewIngredient(request.form['NewIngredientName'], request.form['NewIngredientVolume'])))
            
        elif 'DeleteIngredient' in request.form:
            db.DeleteIngredient(int(request.form['DeleteIngredient']))
            
            return html_builder.conf('purchase', "")
            
        elif 'EditIngredientName' in request.form:
            return html_builder.conf('purchase', notification(db.EditIngredientName(request.form['EditIngredientName'], request.form['id'])))
        
        elif 'LastPrice' in request.form:
            return html_builder.conf('purchase', notification(db.LastPrice(request.form['LastPrice'], request.form['id'])))

        #######################\   Обработчик страницы dish_list  /#######################
        
        elif 'IngredientVolumeData' in request.form:
            db.IngredientVolumeEdit(request.form['IngredientVolumeData'], request.form['DishId'])
            
            return html_builder.conf('dish_list', "", request.form['DishId'])

        elif 'DeleteIngredientFromRecipe' in request.form:
            db.DeleteIngredientFromRecipe(request.form['DishId'], request.form['DeleteIngredientFromRecipe'])
            
            return html_builder.conf('dish_list', "", request.form['DishId'])

        elif 'Recipe' in request.form:
            return html_builder.conf('dish_list', "" , request.form['Recipe'])
        
        elif 'AddIngredientToRecipe' in request.form:
            db.AddIngredientToRecipe(request.form['DishId'], request.form['AddIngredientToRecipe'])
            
            return html_builder.conf('dish_list', "", request.form['DishId'])
        
        elif 'NewDish' in request.form:
            return html_builder.conf('dish_list', notification(db.NewDish(request.form['NewDish'])))    #   Добавляет блюдо
        
        elif 'DeleteDish' in request.form:
            db.DeleteDish(request.form['DeleteDish'])

            return html_builder.conf('dish_list', "")   #   Удаляет блюдо

        elif 'ChangeDishStatus' in request.form:
            db.ChangeDishStatus(request.form['ChangeDishStatus'])

            return html_builder.conf('dish_list', "")   #   Включает/выключает отображение блюда
        
        elif 'EditDishName' in request.form:
            return html_builder.conf('dish_list', notification(db.EditDishName(request.form['EditDishName'], request.form['id'])))  #   Меняет имя блюда
        
        #########################\  Обработчик страницы users   /##########################

        elif 'NewUser' in request.form:

            return html_builder.conf('users', notification(db.NewUser(request.form['NewUser'])))    #   Добавляет пользователя
        
        elif 'DeleteUser' in request.form:
            db.DeleteUser(request.form['DeleteUser'])

            return html_builder.conf('users', "")   #   Удаляет пользователя
        
        elif 'ChangeUserStatus' in request.form:
            db.ChangeUserStatus(request.form['ChangeUserStatus'])

            return html_builder.conf('users', "")   #   Включает/выключает отображение пользователя
        
        elif 'EditUserName' in request.form:
            return html_builder.conf('users', notification(db.EditUserName(request.form['EditUserName'], request.form['id'])))  #   Меняет имя пользователя, если всё хорошо

        ######################\   Oбработчик страницы menu   /#############################

        elif 'GetMemu' in request.form:
            return html_builder.conf('menu', "", request.form['GetMemu'])
        
        elif 'Memu' in request.form:
            db.UpdateMenu(request.form['Memu'], request.form['Week'])
            return html_builder.conf('menu', notification(["Успех", "Меню на неделю сохранено!"]), request.form['Week'])
        
        elif 'PriceRecalculate' in request.form:
            return html_builder.conf('menu', notification(db.PriceRecalculate(request.form['PriceRecalculate'])), request.form['PriceRecalculate'])

    if request.method == 'GET':
        return html_builder.conf("menu", "")    #  Редирект на страницу по умолчанию

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="8080")

"""
доделать:

    добавить возможность указывать цену при добавлении ингредиента (не обязательную)
    добавить возможность указать объём при добавлении ингредиента в рецепт (не обязательную)
    
    название удаляемого ингредиента в accept_delete_conteiner
    стили подтверждения удаления ингредиентов
    
    коментарии ко всему
    
    автопрокрутку до измененного элемента
    
"""