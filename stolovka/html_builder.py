﻿import datetime

from BD import db
from texsts import *

def menu(id=None):

    def generate_food_list():
        current_week = f"{datetime.date.today().year}-W{datetime.date.today().isocalendar()[1]:02d}"

        if datetime.datetime.now().weekday():
            previous_dey_data = "var previous_dey_data = " + str(db.GetMemu(current_week)[datetime.datetime.now().weekday() - 1])
        today_data = "var today_data = " + str(db.GetMemu(current_week)[datetime.datetime.now().weekday()])
        
        script = f"""<script>
        {previous_dey_data if datetime.datetime.now().weekday() else ""};
        {today_data};
        </script>"""
        

        table_html = '<table class="menu_table">'
        for i in range(1, 9):
            table_html += f'''
                <tr class="dish_column" id="dish_column_{i}" style="display: none;">
                    <td><p class="dish_name" id="dish_name{i}"></p></td>
                    <td class="quantity-control">
                        <span class="price" id="dish_price{i}"></span>
                        <button class="left-qua" onclick="decrement({i})">➖</button>
                        <input class="counter" type="value" id="quantity{i}" oninput="total_price_resume()" value="0">
                        <button class="right-qua" onclick="increment({i})">➕</button>
                    </td>
                </tr>'''
        table_html += '</table>'
    
        return table_html + script

    def btn_previous_dey():
        if datetime.datetime.now().weekday() == 0:
            return ""
        return """<button class="previous_dey" id="previous_dey" onclick="swech_dey() ">Предыдущий день</button>"""
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Form</title>
</head>
<body>
    <style>
        {menu_page_style_advanced}
    </style>
    <div class="wrapper">
        <div class="form">
            <h1 id="user_name" class="name">{db.GetUser(id)[1]}</h1>
            <div class="foods">{generate_food_list()}</div>
            <div class="result">
                {btn_previous_dey()}
                <p class="total_price" id="total_price">Всего: 0грн</p>
                <button class="buy" onclick="buy()">Купить</button>
                <button class="cancel" onclick="PreviousDay()">Отмена</button>
            </div>
        </div>
    </div>

<script>
    {menu_page_scripts}
</script>
    
</body>
</html>
"""


def letter(letter):
    def user_filling():    
        UserList = db.LoadUserList()
        users = []
        for user in UserList:
            if user[1][0] == letter:
                users.append(user)
           
        answer = """<button onclick="PreviousDay()" style="text-align: center; background-color: #c9c9c9;" class="key">Назад</button>"""

        for user in users:
            if user[2]:
                answer += f"""<button class="key" onclick="chose_menu('{user[0]}')">{user[1]}</button>"""

        return answer
    
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Виртуальная клавиатура</title>
    <style>
        {choise_user_page_style}
    </style>
</head>
<body>
    <div class="choise_user">
        {user_filling()}
    </div>
    <script>
        {choise_user_page_scripts}
    </script>
</body>
</html>
"""


def main():
    def get_name_laters():
        UserList = db.LoadUserList()
        
        letters = []
        for user in UserList:
            if user[2]:
                letter = user[1][0]
                if letter not in letters:
                    letters.append(letter)

        answer = ""

        for letter in letters:
            answer += f"""<button onclick="letter('{letter}')" class="key">{letter}</button>"""
            
        return answer

    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Виртуальная клавиатура</title>
    <style>
        {main_page_style}
    </style>
</head>
<body>
    <div class="keyboard">
        {get_name_laters()}
    </div>
    <script>
        {main_page_scripts}
    </script>
</body>
</html>
"""


def conf(page=None, notification=None, *args):
    
    def page_scripts():
        if page == 'menu':
            return scripts_for_menu
        elif page == 'reports':
            return
        elif page == 'users':
            return scripts_for_users
        elif page == 'purchase':
            return scripts_for_ingredients_page
        elif page == 'dish_list':
            return scripts_for_dish_page    #   Добавляет скрипты на страницу

    def page_style():
        if page == 'menu':
            return define_menu_page_style
        elif page == 'reports':
            return
        elif page == 'users':
            return control_user_page_style
        elif page == 'purchase':
            return define_ingredients_page_style
        elif page == 'dish_list':
            return define_dish_page_style   #   Добавляет стили на страницу

    def filling_main_page():

        if page == 'menu':
            
            def week():
                if args:
                    return args[0]
                else:
                    current_date = datetime.date.today()
                    current_year = current_date.year
                    current_week = current_date.isocalendar()[1]
                    return f"{current_year}-W{current_week:02d}"    #   подстановка нужной недели
                
            def menu_filling():  
                menu = db.GetMemu(week())
            
                table = ""
                days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
                for day in range(5):

                    table += f"""
                    <table id="dey{day + 1}">
                        <tr>
                            <th colspan="2">{days[day]}</th>
                        </tr>"""
                    for pos in range(8):

                        dish_name = menu[day][f"name{pos + 1}"]
                        dish_price = menu[day][f"price{pos + 1}"]
                        def dish_list():
                            answer = ""
                            for dish in db.GetDishList():
                                if dish[2]:
                                    answer += f"""<option>{dish[1]}</option>"""
                            return answer
                    
                        table += f"""
                        <tr>
                            <td class="eda">
                                <select class="dish_name" id="name{pos + 1}" onchange="UpdateMenu()" style="width: 300px;">
                                    <option>{dish_name}</option>
                                    <option></option>
                                    {dish_list()}
                                </select>
                            </td>
                            <td id="price{pos + 1}" class="price" ><input value="{dish_price}" class="price_input" type="number" max="999"></td>
                        </tr>"""
                    
                    table += "</table>"

                return table    #   создание таблиц для заполнения меню

            return f"""
    <div class="menu_conteiner">
            
        <div style="height: 38px;">
          <input class="week" type="week" id="week" name="week" onchange="WeekChange()">
          <button class="heder_button" onclick="UpdateMenu()">Сохранить</button>
          <button class="heder_button" onclick="PriceRecalculate()">Пересчёт цен</button>
        </div>

        <div class="menu-container">
        {menu_filling()}
        </div>
    </div>
    
    <script>
        var weekInput = document.getElementById('week');
        weekInput.value = '{week()}';
    </script>"""
        
        elif page == 'reports':
            return
        
        elif page == 'users':   #   заполнение вкладки с настройкой пользователей
            
            def user_table():
                users = db.LoadUserList()
                table = ""
            
                for user in users:
                    table += f"""
            <tr class="user_column">
                <td>
                <input class="table_input_user_name" type="text" id="UserName{user[0]}" value="{user[1]}" onfocus="showEditButton({user[0]})" onblur="hideEditButtonWithDelay({user[0]})">
                <button id="editButton{user[0]}" style="display: none;" title="Сохранить изменённое имя" style="hiden;" onclick="EditUserName({user[0]})">✏️</button>
                </td>
                <td class="user_status">{'✔️' if user[2] else '❌'}</td>
                <td class="user_actions">
                  <button style="width: 140px;" title="Деактивированный пользователь не будет отображатся в списке пользователей на странице заказов. его всегда можно будет активировать снова" onclick="ChangeUserStatus({user[0]})">{'Деактивировать' if user[2] else 'Активировать'}</button>
                  <button title="Удалить пользователя (не удалит его из отчётов. если пользователь временно не будет пользоватся столовой деактивируйте его.)" class="delete_user" onclick="DeleteUser({user[0]})">Удалить</button>
                </td>
            </tr>
            """
                
                return table    #   создание таблицы пользователей
            
            return f"""
    <div class="header">
        <div class="add-user-conteiner">
            <input class="input_user_name" type="text" id="newUserName" placeholder="Имя пользователя" oninput="FilterUserList()">
            <button class="add_user" onclick="NewUser()">Добавить</button>
        </div>
    </div>
    
    <div class="users-table-conteiner">
        <table>       
            <tbody>
                {user_table()}
            </tbody>
        </table>
    </div>
    """
        
        elif page == 'purchase':
            
            def dish_table():
                ingredients = db.GetIngredientsList()
                table = ""
            
                for ingredient in ingredients:
                    table += f"""
            <tr class="ingredients_column">
                <td>
                <input class="table_input_ingredient_name" type="text" id="IngredientName{ingredient[0]}" value="{ingredient[1]}" onfocus="showEditButton({ingredient[0]})" onblur="hideEditButtonWithDelay({ingredient[0]})">
                <button id="editButton{ingredient[0]}" style="display: none;" title="Сохранить изменённое название" onclick="EditIngredientName({ingredient[0]})">✏️</button>
                </td>
                <td class="ingredient_volume" style="font-size: 18px;width: 210px;">
                    <input id="newLastPrice{ingredient[0]}" value="{ingredient[3]}" class="price_input" type="number" max="999" onfocus="showEditLastPriceButton({ingredient[0]})" onblur="hideEditLastPriceButtonWithDelay({ingredient[0]})">
                    грн/{ingredient[2]}
                    <button class="edit_last_price" id="editLastPrice{ingredient[0]}" style="display: none;" onclick="editLastPrice({ingredient[0]})">✏️</button>
                </td>
                <td class="ingredients_actions" style="width: 100px;">
                    <button class="delete_ingredient" onclick="DeleteIngredientDiolog({ingredient[0]})">Удалить</button>
                </td>
            </tr>"""
                    
                return table

            return f"""
    <div class="header">
        <div class="add-ingredients-conteiner">
            <input class="input_ingredient_name" type="text" id="newIngredientName" placeholder="Название ингридеента" oninput="FilterIngredientList()">
            <select id="newIngredientVolume" class="volume_input">
                <option></option>
                <option>кг.</option>
                <option>л.</option>
                <option>шт.</option>
            </select>
            <button class="add_ingredient" onclick="NewIngredient()">Добавить</button>
        </div>
    </div>
    
    
    <div class="ingredients-table-conteiner">
        <table>       
            <tbody>
                {dish_table()}
            </tbody>
        </table>
    </div>
    
    <div id="accept_delete_conteiner" class="accept_delete_conteiner" style="display: none;">
        <h1 style="margin: 0px;">Вы действительно хотите удалить ингредиент?</h1>
        <p>Также, удалённый ингредиент будет удалён из всех рецептов</p>
        <div class="delete_action_buttons">
            <button class="cancel_delete_button" onclick="cancelDelete()">Отмена</button>
            <button class="accept_delete_button" onclick="DeleteIngredient()">Удалить</button>
        </div>
    </div>
    
    """
            
        elif page == 'dish_list':

            def dish_table():
                dishes = db.GetDishList()
                table = ""
            
                for dish in dishes:
                    table += f"""
            <tr class="dish_column">
                <td>
                <input class="table_input_dish_name" type="text" id="DishName{dish[0]}" value="{dish[1]}" onfocus="showEditButton({dish[0]})" onblur="hideEditButtonWithDelay({dish[0]})">
                <button id="editButton{dish[0]}" style="display: none;" title="Сохранить изменённое название" style="hiden;" onclick="EditDishName({dish[0]})">✏️</button>
                </td>
                <td class="dish_status">{'✔️' if dish[2] else '❌'}</td>
                <td class="dish_actions">
                  <button style="width: 140px;" title="Деактивированное блюдо не будет отображатся в списке блюд. Его всегда можно будет активировать снова" onclick="ChangeDishStatus({dish[0]})">{'Деактивировать' if dish[2] else 'Активировать'}</button>
                  <button onclick="Recipe({dish[0]})">Рецептура</button>
                  <button title="Удалить блюдо" class="delete_dish" onclick="DeleteDish({dish[0]})">Удалить</button>
                </td>
            </tr>"""
                    
                return table    #   возвращает таблицу с блюдами

            def recipe_window():
                ingredients = db.GetIngredientsList()
                ingredients_dict = {item[0]: item[1:] for item in ingredients}

                def ingredients_choose_list():
                    
                    result = "<option></option>"
                    
                    heven_id = []
                    
                    for i in db.GetRecipe(args[0]):
                        heven_id.append(i[0])

                    for i in ingredients:
                        if i[0] not in heven_id:
                            result += f'<option value="{i[0]}">{i[1]}</option>'
                    return result

                def recipe_table():

                    answer = "<table>"

                    for i in db.GetRecipe(args[0]):
                        answer += f"""
            <tr class="">
                <td class="padding_4">{ingredients_dict[i[0]][0]}</td>
                <td class="input_volume">
                    <input id="set_ingridient_volume{i[0]}" class="input" type="number" value="{i[1]}" onfocus="showIngredientVolumeEditButton({i[0]})" onblur="hideIngredientVolumeEditButtonWithDelay({i[0]})">  {ingredients_dict[i[0]][1]}
                    <button class="set_volume" id="set_volume{i[0]}" style="display: none;" onclick="SaveVolume({args[0]}, {i[0]})">✏️</button>
                </td>
                <td class="ingredients_actions"><button class="delete_ingredient" onclick="DeleteIngredientFromRecipe({args[0]}, {i[0]})">Удалить</button></td>
            </tr>"""
                        
                    answer += "</table>"
                    return answer
                        
                return f"""
    <div id="recipeWindow" class="recipe_conteiner">
        <div class="recipe_conteiner_header">
            <div class="add-ingredients-conteiner">
                <select id="newIngredient" class="add_ingredient_select">
                    {ingredients_choose_list()}
                </select>
                <button class="add_ingredient" onclick="UpdateRecipe({args[0]})">Добавить</button>
            </div>
            
            <div style="width: -webkit-fill-available;"><h1 class="dish_name">{db.GetDishName(args[0])[0]}</h1></div>
            
            <button class="close_recipe" onclick="СloseRecipeWindow()">Закрыть</button>
        </div>
        <div class="recipe_conteiner_body">
            {recipe_table()}
        </div>
    </div>
""" #   генерирует окно рецета

            return f"""
    <div class="header">
        <div class="add-dish-conteiner">
            <input class="input_dish_name" type="text" id="newDishName" placeholder="Название блюда" oninput="FilterDishList()">
            <button class="add_dish" onclick="NewDish()">Добавить</button>
        </div>
    </div>
    
    <div class="dish_table_conteiner">
        <table>       
            <tbody>
                {dish_table()}
            </tbody>
        </table>
    </div>
    
    {recipe_window() if args != () else ""}
    
    """

    def sidebar_create():

        # <div class="sub_menu" style="{'display: flex;' if page == 'menu' or page == 'purchase' or page == 'dish_list' else 'display: none;'}">
        #         <button class="sub_menu_btn" {'style="background-color: #c1c1c1;float: right;margin-right: 0px;color: white;"' if page == 'purchase' else ""} onclick="openpage('purchase')">Закупка</button>
        #         <button class="sub_menu_btn" {'style="background-color: #c1c1c1;float: right;margin-right: 0px;color: white;"' if page == 'dish_list' else ""} onclick="openpage('dish_list')">Список блюд</button>
        # </div>

        return f"""
    <h2>Конфигурация Столовой</h2>

    <button class="key" {'style="background-color: #4CAF50;color: white;"' if page == 'menu' else ''} onclick="openpage('menu')">Меню</button>
    <button class="key" {'style="background-color: #4CAF50;color: white;"' if page == 'purchase' else ""} onclick="openpage('purchase')">Закупка</button>
    <button class="key" {'style="background-color: #4CAF50;color: white;"' if page == 'dish_list' else ""} onclick="openpage('dish_list')">Список блюд</button>
    <button class="key" {'style="background-color: #4CAF50;color: white;"' if page == 'reports' else ""} onclick="openpage('reports')">Отчет</button>
    <button class="key" {'style="background-color: #4CAF50;color: white;"' if page == 'users' else ""} onclick="openpage('users')">Пользователи</button>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Страница конфигурации</title>
    <style>
        {config_page_style}
        {page_style()}
    </style>
</head>
<body style="margin: 0px;">
    <div class="sidebar">{sidebar_create()}</div>
    <div class="content">{filling_main_page()}</div>
    <div class="notifications"></div>
    
    <script>
    {config_page_scripts}
    {page_scripts()}
    {notification if notification != None else ""}
    </script>
    
</body>
</html>"""
    