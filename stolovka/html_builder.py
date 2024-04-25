import datetime
import re

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
                    <td><p class="dish_name" id="dish_name{i}" style="margin-left: 6px; padding-left: 6px; {"background-color: #f1f1f1; border-radius: 15px;" if (i % 2) == 0 else ""}"></p></td>
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
                <p class="total_price" id="total_price">Всего: 0грн</p>
            </div>
            <div class="result">
                {btn_previous_dey()}
                <button class="cancel">Отмена</button>
                <button class="buy" onclick="buy()">Купить</button>
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
           
        answer = """<button onclick="MainPage()" style="text-align: center; background-color: #c9c9c9;" class="key">Назад</button>"""

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
        elif page == 'dish_list':
            return scripts_for_dish    #   Добавляет скрипты на страницу

    def page_style():
        if page == 'menu':
            return define_menu_page_style
        elif page == 'reports':
            return
        elif page == 'users':
            return control_user_page_style
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
                            return "".join(f"""<option>{dish[1]}</option>""" for dish in db.GetDishList())
                    
                        table += f"""
                        <tr>
                            <td class="eda">
                                <select class="dish_name" id="name{pos + 1}" style="width: 300px;">
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
          <button class="add_user" >Сохранить</button>
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
            
                table = """
    <table style="margin-top: 50px;">       
        <tbody>"""
            
                for user in users:
                    table += f"""
            <tr class="user_column">
                <td>
                <input style="border-width: 0px;width: 300px;" type="text" id="UserName{user[0]}" value="{user[1]}" onfocus="showEditButton({user[0]})" onblur="hideEditButtonWithDelay({user[0]})">
                <button id="editButton{user[0]}" style="display: none;" title="Сохранить изменённое имя" style="hiden;" onclick="EditUserName({user[0]})">✏️</button>
                </td>
                <td class="user_status">{'✔️' if user[2] else '❌'}</td>
                <td class="user_actions">
                  <button style="width: 140px;" title="Деактивированный пользователь не будет отображатся в списке пользователей на странице заказов. его всегда можно будет активировать снова" onclick="ChangeUserStatus({user[0]})">{'Деактивировать' if user[2] else 'Активировать'}</button>
                  <button title="Удалить пользователя (не удалит его из отчётов. если пользователь временно не будет пользоватся столовой деактивируйте его.)" class="delete_user" onclick="DeleteUser({user[0]})">Удалить</button>
                </td>
            </tr>"""
                table += "</tbody></table>"
                return table    #   создание таблицы пользователей
            
            header = """
    <div class="header">
        <div class="add-user-conteiner">
            <input class="input_user_name" type="text" id="newUserName" placeholder="Имя пользователя" oninput="FilterUserList()">
            <button class="add_user" onclick="NewUser()">Добавить</button>
        </div>
    </div>
"""

            return header + user_table()
        
        elif page == 'purchase':
            return
            
        elif page == 'dish_list':
            
            def dish_table():
                dishes = db.GetDishList()
            
                table = """
    <table style="margin-top: 50px;">       
        <tbody>"""
            
                for dish in dishes:
                    table += f"""
            <tr class="dish_column">
                <td>
                <input style="border-width: 0px;width: 300px;" type="text" id="DishName{dish[0]}" value="{dish[1]}" onfocus="showEditButton({dish[0]})" onblur="hideEditButtonWithDelay({dish[0]})">
                <button id="editButton{dish[0]}" style="display: none;" title="Сохранить изменённое имя" style="hiden;" onclick="EditDishName({dish[0]})">✏️</button>
                </td>
                <td class="dish_status">{'✔️' if dish[2] else '❌'}</td>
                <td class="dish_actions">
                  <button style="width: 140px;" title="Деактивированное блюдо не будет отображатся в списке блюд. Его всегда можно будет активировать снова" onclick="ChangeDishStatus({dish[0]})">{'Деактивировать' if dish[2] else 'Активировать'}</button>
                  <button title="Удалить блюдо" class="delete_dish" onclick="DeleteDish({dish[0]})">Удалить</button>
                </td>
            </tr>"""
                table += "</tbody></table>"
                return table

            header = """
    <div class="header">
        <div class="add-dish-conteiner">
            <input class="input_dish_name" type="text" id="newDishName" placeholder="Название блюда" oninput="FilterDishList()">
            <button class="add_dish" onclick="NewDish()">Добавить</button>
        </div>
    </div>
"""

            return header + dish_table()

    def sidebar_create():
        
        return f"""
    <h2>Конфигурация Столовой</h2>

    <button class="key" style="{'background-color: #4CAF50;color: white;' if page == 'menu' or page == 'purchase' or page == 'dish_list' else ''}"
            onclick="openpage('menu')">Меню</button>
    <div class="sub_menu" style="{'display: flex;' if page == 'menu' or page == 'purchase' or page == 'dish_list' else 'display: none;'}">
            <button class="sub_menu_btn" {'style="background-color: #c1c1c1;float: right;margin-right: 0px;color: white;"' if page == 'purchase' else ""} onclick="openpage('purchase')">Закупка</button>
            <button class="sub_menu_btn" {'style="background-color: #c1c1c1;float: right;margin-right: 0px;color: white;"' if page == 'dish_list' else ""} onclick="openpage('dish_list')">Список блюд</button>
    </div>

    <button class="key" {'style="background-color: #4CAF50;float: right;margin-right: 0px;color: white;"' if page == 'reports' else ""} onclick="openpage('reports')">Отчет</button>
    <button class="key" {'style="background-color: #4CAF50;float: right;margin-right: 0px;color: white;"' if page == 'users' else ""} onclick="openpage('users')">Пользователи</button>
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

    <div class="sidebar">
    
        {sidebar_create()}
        
    </div>

    <div class="content">
        {filling_main_page()}
    </div>
    
    <div class="notifications"></div>
    
    <script>
    {config_page_scripts}
    {page_scripts()}
    {notification if notification != None else ""}
    </script>
    

</body>
</html>"""
    