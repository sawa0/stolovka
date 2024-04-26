import sqlite3, json

class DB:
    def __init__(self):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        isactive BOOLEAN NOT NULL 
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        "order" TEXT NOT NULL
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS "menu" (
                        week_number VARCHAR(10) PRIMARY KEY,
                        MenuText TEXT,
                        CONSTRAINT unique_week_number UNIQUE (week_number)
                    );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS "orders" (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT NOT NULL,
                        person_id INTEGER NOT NULL,
                        "order" TEXT NOT NULL
                    );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        isactive BOOLEAN NOT NULL,
                        recipe TEXT
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        volume_unit TEXT NOT NULL,
                        last_price INTEGER
                    )''')
        conn.commit()
        conn.close()    #   Создает структуру базы данных, если таковой нет 
        
    def NewOrder(self, data, user, order):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO orders (data, person_id, order_text) VALUES (?, ?, ?)""", (data, user, order))
        conn.commit()
        conn.close()
        return  #   пока не используется
    
    def GetUserStatus():
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute("""SELECT isactive FROM users WHERE id = ?""", (id,))

        # Получение результата запроса
        status = cursor.fetchone()

        conn.close()
        return status[0]    #   Получает статус пользователя. ((Теоретически бесполезная функция))

    ##################\  Для страницы menu /##################

    def LoadUserList(self):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users""")
        users = cursor.fetchall()
            
        conn.close()
        
        return users    #   Получает список всех пользователей из базы данных

    def GetMemu(self, week):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT MenuText FROM "menu" WHERE week_number = '{week}';""")
        menu = cursor.fetchall()

        if not menu:
            conn.close()
            return [{"name1":"", "price1":"", "name2":"", "price2":"", "name3":"", "price3":"", "name4":"", "price4":"", "name5":"", "price5":"", "name6":"", "price6":"", "name7":"", "price7":"", "name8":"", "price8":""},
                    {"name1":"", "price1":"", "name2":"", "price2":"", "name3":"", "price3":"", "name4":"", "price4":"", "name5":"", "price5":"", "name6":"", "price6":"", "name7":"", "price7":"", "name8":"", "price8":""},
                    {"name1":"", "price1":"", "name2":"", "price2":"", "name3":"", "price3":"", "name4":"", "price4":"", "name5":"", "price5":"", "name6":"", "price6":"", "name7":"", "price7":"", "name8":"", "price8":""},
                    {"name1":"", "price1":"", "name2":"", "price2":"", "name3":"", "price3":"", "name4":"", "price4":"", "name5":"", "price5":"", "name6":"", "price6":"", "name7":"", "price7":"", "name8":"", "price8":""},
                    {"name1":"", "price1":"", "name2":"", "price2":"", "name3":"", "price3":"", "name4":"", "price4":"", "name5":"", "price5":"", "name6":"", "price6":"", "name7":"", "price7":"", "name8":"", "price8":""}]

        conn.close()
        return json.loads(menu[0][0])   #   Возвращает меню по номеру недели
        
    def UpdateMenu(self, menu_text, week):

        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM menu WHERE week_number = ?""", (week,))
        answer = cursor.fetchone()
        if answer:
            cursor.execute(f"""UPDATE menu SET MenuText = '{menu_text}' WHERE week_number = '{week}';""")
            conn.commit()
            conn.close()
            return
        
        cursor.execute(f"""INSERT INTO menu (week_number, MenuText) VALUES ('{week}', '{menu_text}');""")
        conn.commit()
        conn.close()
        return  #   Обновляет меню на выборную неделю

    ################\ Для страницы purchase  /################
    
    def NewIngredient(self, name, volume_unit):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM products WHERE name = ?""", (name,))
        ingredient = cursor.fetchone()
        if ingredient:
            return ["Ошибка", "Такой ингредиент уже существует"]

        cursor.execute("""INSERT INTO products (name, volume_unit) VALUES (?, ?)""", (name, volume_unit))
        conn.commit()
        conn.close()
        
        return ["успех", "Ингредиент добавлен"]  #   Добавляет ингредиент

    def GetIngredientsList(self):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM products""")
        dishes = cursor.fetchall()
        
        conn.close()
        
        return dishes    #   Возвращает список всех ингредиентов

    def EditIngredientName(self, name, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM products WHERE name = ?""", (name,))
        ingredient = cursor.fetchone()

        if ingredient:
            if ingredient[0] == int(id):
                conn.close()
                return ["Ошибка", "Вы не изменили название"]
            conn.close()
            return ["Ошибка", "Такой ингредиент уже существует"]
            

        cursor.execute("""UPDATE products SET name = ? WHERE id = ?""", (name, id))
        conn.commit()
        conn.close()
        return ["Успех", "Название ингредиента изменено"]   #   Меняет название ингредиента
    
    def LastPrice(self, LastPrice, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor() 

        cursor.execute("""UPDATE products SET last_price = ? WHERE id = ?""", (LastPrice, id))
        conn.commit()
        conn.close()
        return ["Успех", "Цена ингредиента изменена"]   #   Меняет цену последней покупки ингредиента
    
    def DeleteIngredient(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""DELETE FROM products WHERE id = ?""", (id,))
        conn.commit()
        conn.close()    #   Удаляет ингредиент

    ################\ Для страницы dish_list /################
    
    def NewDish(self, dishname):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM dishes WHERE name = ?""", (dishname,))
        dish = cursor.fetchone()
        if dish:
            return ["Ошибка", "Такое блюдо уже существует"]

        cursor.execute("""INSERT INTO dishes (name, isactive) VALUES (?, ?)""", (dishname, True))
        conn.commit()
        conn.close()
        
        return ["успех", "Блюдо добавлено"]  #   Добавляет блюдо
    
    def ChangeDishStatus(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT isactive FROM dishes WHERE id = ?""", (id,))
        status = cursor.fetchone()

        if status[0]:
            status = False
        else:
            status = True
            
        cursor.execute("""UPDATE dishes SET isactive = ? WHERE id = ?""", (status, id))
        conn.commit()
        conn.close()    #   Меняет статус блюда
    
    def GetDishList(self):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM dishes""")
        dishes = cursor.fetchall()
        
        conn.close()
        
        return dishes    #   Возвращает список всех блюд

    def EditDishName(self, dishname, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM dishes WHERE name = ?""", (dishname,))
        dish = cursor.fetchone()

        if dish:
            if dish[0] == int(id):
                conn.close()
                return ["Ошибка", "Вы не изменили название"]
            conn.close()
            return ["Ошибка", "Такое блюдо уже существует"]
            

        cursor.execute("""UPDATE dishes SET name = ? WHERE id = ?""", (dishname, id))
        conn.commit()
        conn.close()
        return ["Успех", "Название блюда изменено"]   #   Меняет название блюда
    
    def DeleteDish(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""DELETE FROM dishes WHERE id = ?""", (id,))
        conn.commit()
        conn.close()    #   Удаляет блюдо

    ##################\ Для страницы users /##################
    
    def NewUser(self, username):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        user = cursor.fetchone()
        if user:
            return ["Ошибка", "Такой пользователь уже существует"]

        cursor.execute("""INSERT INTO users (username, isactive) VALUES (?, ?)""", (username, True))
        conn.commit()
        conn.close()
        
        return ["успех", "Пользователь успешно добавлен"]  #   Добавляет пользователя
    
    def ChangeUserStatus(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT isactive FROM users WHERE id = ?""", (id,))
        status = cursor.fetchone()

        if status[0]:
            status = False
        else:
            status = True
            
        cursor.execute("""UPDATE users SET isactive = ? WHERE id = ?""", (status, id))
        conn.commit()
        conn.close()    #   Меняет статус пользователя 
        
    def EditUserName(self, username, id):
        
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
        user = cursor.fetchone()

        if user:
            if user[0] == int(id):
                conn.close()
                return ["Ошибка", "Вы не изменили имя"]
            conn.close()
            return ["Ошибка", "Такой пользователь уже существует"]
            

        cursor.execute("""UPDATE users SET username = ? WHERE id = ?""", (username, id))
        conn.commit()
        conn.close()
        return ["Успех", "Имя пользователя изменено"]   #   Меняет имя пользователя
    
    def DeleteUser(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        cursor.execute("""DELETE FROM users WHERE id = ?""", (id,))
        conn.commit()
        conn.close()    #   Удаляет пользователя

    def GetUser(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))

        # Получение результата запроса
        status = cursor.fetchone()

        conn.close()
        return status   #   Возвращает информацию о пользователе

db = DB()
