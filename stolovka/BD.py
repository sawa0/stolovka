import sqlite3, json
from datetime import datetime

class DB:
    def __init__(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            isactive BOOLEAN NOT NULL )''')   #   таблица пользователей
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT NOT NULL,
                            time TEXT NOT NULL,
                            person TEXT NOT NULL,
                            person_id INTEGER NOT NULL,
                            "order" TEXT NOT NULL,
                            price TEXT NOT NULL)''')   #   таблица заказов
            cursor.execute('''CREATE TABLE IF NOT EXISTS "menu" (
                            week_number VARCHAR(10) PRIMARY KEY,
                            MenuText TEXT,
                            CONSTRAINT unique_week_number UNIQUE (week_number));''')  #   таблица меню
            cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            isactive BOOLEAN NOT NULL,
                            recipe TEXT NOT NULL,
                            price FLOAT NOT NULL DEFAULT 0)''')   #   таблица блюд
            cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            volume TEXT NOT NULL,
                            price INTEGER NOT NULL)''')   #   таблица ингредиентов
            cursor.execute('''CREATE TABLE IF NOT EXISTS "settings" (
                            parameter TEXT PRIMARY KEY,
                            Value TEXT);''')  #   таблица меню
            
            #############################################################################
            #     создаёт в таблице "settings" параметр "RegularMenu", если его нет
            #############################################################################
            cursor.execute("""SELECT * FROM "settings" WHERE parameter = 'RegularMenu' """)
            if not cursor.fetchone():
                cursor.execute("""INSERT INTO "settings" (parameter, Value) VALUES (?, ?)""",
                              ('RegularMenu', json.dumps({'1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': ''})))
            #############################################################################
            #     создаёт в таблице "settings" параметр "OrderConfirmationType", если его нет
            #############################################################################
            cursor.execute("""SELECT * FROM "settings" WHERE parameter = 'OrderConfirmationType' """)
            data = cursor.fetchone()
            self.OrderConfirmationType = None
            if not data:
                cursor.execute("""INSERT INTO "settings" (parameter, Value) VALUES (?, ?)""",
                              ('OrderConfirmationType', json.dumps(["auto", 10])))  #   auto/on/off

            conn.commit()   #   Создает структуру базы данных, если таковой нет 
        
    def NewTransaction(self, data):

        order_total = sum(float(item[1][0]) * int(item[1][1]) for item in data['order'])
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')
        serialized_order = json.dumps(data['order'])

        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO transactions (data, time, person, person_id, "order", price) VALUES (?, ?, ?, ?, ?, ?)""",
                           (current_date, current_time, data['userName'], data['userID'], serialized_order, order_total))
            conn.commit()
            
    def GetTodayTtransactions(swlf):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM transactions WHERE data = ?""", (datetime.now().strftime('%Y-%m-%d'),))
            return cursor.fetchall()
        
    def GetThisMonthsTransactions(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM transactions WHERE data LIKE ?""", (datetime.now().strftime('%Y-%m'),))
            return cursor.fetchall()

    ##################\  Для страницы menu /##################

    def GetMemu(self, week):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT MenuText FROM "menu" WHERE week_number = ?;""", (week,))
            menu = cursor.fetchone()

            if not menu:
                menu = [{'1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': ''} for _ in range(7)]
                cursor.execute(f"""INSERT INTO "menu" (week_number, MenuText) VALUES (?, ?);""", (week, json.dumps(menu)))
                conn.commit()
            else:
                menu = json.loads(menu[0])
            return menu   #   Возвращает меню по номеру недели
        
    def UpdateMenu(self, week, data):   #   "2024-W26", [dey, pos, DishID]
        menu = self.GetMemu(week)
        menu[data[0]][str(data[1])] = data[2]

        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"""UPDATE "menu" SET MenuText = ? WHERE week_number = ?;""", (json.dumps(menu), week))
            conn.commit()   #   Обновляет меню
    
    def GetRegularMenu(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT Value FROM "settings" WHERE parameter = 'RegularMenu' """)
            return json.loads(cursor.fetchone()[0])


    def UpdateRegularMenu(self, data):
        RegMenu = self.GetRegularMenu()
        RegMenu[str(data[0])] = data[1]

        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE "settings" SET Value = ? WHERE parameter = 'RegularMenu'""", (json.dumps(RegMenu),) )
            conn.commit()


    ################\ Для страницы purchase  /################

    def FindDishWhereIngredient(self, IngredientID):
        dishes_to_update = []
        for dish in self.GetDishList():
            recipe = json.loads(dish[3])
            if str(IngredientID) in recipe:
                dishes_to_update.append(dish[0])

        return dishes_to_update #   Возвращает список ID блюд, в которых есть ингредиент
    
    def NewIngredient(self, name, volume, price):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM products WHERE name = ?""", (name,))
            if cursor.fetchone():
                return ["Ошибка", "Такой ингредиент уже существует"]

            cursor.execute("""INSERT INTO products (name, volume, price) VALUES (?, ?, ?)""", (name, volume, price))
            conn.commit()
        
        return ["успех", "Ингредиент добавлен"]  #   Добавляет ингредиент

    def GetIngredientsList(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM products""")
            return cursor.fetchall()    #   Возвращает список всех ингредиентов

    def GetIngredientsDict(self):
        return {ingredient[0]: {"name": ingredient[1], "volume": ingredient[2], "price": ingredient[3]} for ingredient in self.GetIngredientsList()}    # Возвращает словарь всех ингредиентов

    def EditIngredientName(self, id, name):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
        
            cursor.execute("""SELECT * FROM products WHERE name = ?""", (name,))
            if cursor.fetchone():
                return ["Ошибка", "Такой ингредиент уже существует"]    #   Проверка на уникальность
            
            cursor.execute("""UPDATE products SET name = ? WHERE id = ?""", (name, id))
            conn.commit()
        return ["Успех", "Название ингредиента изменено"]   #   Меняет название ингредиента
    
    def NewPrice(self, IngredientID, NewPrice):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE products SET price = ? WHERE id = ?""", (NewPrice, IngredientID))
            conn.commit()
        
        for DishID in self.FindDishWhereIngredient(IngredientID):
            self.DishPriceRecalculate(DishID)   #   Обновляет цену блюд, в рецепте которых есть ингредиент
        
        return  #   Меняет цену последней закупки ингредиента

    def DeleteIngredient(self, IngredientID):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM products WHERE id = ?""", (IngredientID, ))
            conn.commit()

        for DishID in self.FindDishWhereIngredient(IngredientID):
            self.DeleteIngredientFromRecipe(int(DishID), IngredientID)  #   Удаляет ингредиент из рецептов блюд. Также удаление пересчитывает цену блюда

        return  #   Удаляет ингредиент из списка ингредиентов, и из рецептов блюд

    ################\ Для страницы dish_list /################
    
    def NewDish(self, dishname):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM dishes WHERE name = ?""", (dishname,))

            if cursor.fetchone():
                return ["Ошибка", "Такое блюдо уже существует"] #   Проверка на уникальность

            cursor.execute("""INSERT INTO dishes (name, isactive, recipe, price) VALUES (?, ?, ?, ?)""", (dishname, True, "{}", 0))
            conn.commit()
        
        return ["успех", "Блюдо добавлено"]  #   Добавляет блюдо
    
    def ChangeDishStatus(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE dishes SET isactive = NOT isactive WHERE id = ?""", (id,)) #   Изменяет статус блюда на протевоположный
            conn.commit()   #   Меняет статус блюда на протевоположный
    
    def GetDishList(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM dishes""")
            return cursor.fetchall()    #   Возвращает список всех блюд

    def GetDishDict(self):
        return {dish[0]: {"name": dish[1], "isactive": dish[2], "recipe": json.loads(dish[3]), "price": dish[4]} for dish in self.GetDishList()}    #   Возвращает словарь всех блюд
        
    def EditDishName(self, id, dishname):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM dishes WHERE name = ?""", (dishname,))

            if cursor.fetchone():
                return ["Ошибка", "Такое блюдо уже существует"] #   Проверка на уникальность

            cursor.execute("""UPDATE dishes SET name = ? WHERE id = ?""", (dishname, id))
            conn.commit()
        return ["Успех", "Название блюда изменено"]   #   Меняет название блюда

    def DeleteDish(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM dishes WHERE id = ?""", (id,))
            conn.commit()   #   Удаляет блюдо
    
    def GetIngredientName(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT name FROM products WHERE id = ?""", (id,))
            return cursor.fetchone()    #   Возвращает название ингредиента

    def GetRecipe(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT recipe FROM dishes WHERE id = ?""", (id,))
            return json.loads(cursor.fetchone()[0])    #   Возвращает рецепт блюда
    
    def AddIngredientToRecipe(self, DishID, IngredientID, IngredientName, Volume):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT recipe FROM dishes WHERE id = ?""", (DishID,))
            recipe = json.loads(cursor.fetchone()[0])

            if IngredientID in recipe:
                return ["Ошибка", "Ингредиент уже в рецепте"]
        
            recipe[IngredientID] = float(Volume)
            cursor.execute("""UPDATE dishes SET recipe = ? WHERE id = ?""", (json.dumps(recipe), DishID))
            conn.commit()
        
        self.DishPriceRecalculate(DishID)   #   Добавляет ингридиент в рецепт
        
    def DeleteIngredientFromRecipe(self, DishID, IngredientID):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            recipe = self.GetRecipe(DishID)
            recipe.pop(str(IngredientID))
            cursor.execute("""UPDATE dishes SET recipe = ? WHERE id = ?""", (json.dumps(recipe), DishID))
            conn.commit()
        
        self.DishPriceRecalculate(DishID)   #   Удаляет ингредиент из рецепта
        
    def IngredientVolumeEdit(self, DishID, IngredientID, Volume):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            recipe = self.GetRecipe(DishID)
            recipe[str(IngredientID)] = float(Volume)
            cursor.execute("""UPDATE dishes SET recipe = ? WHERE id = ?""", (json.dumps(recipe), DishID))
            conn.commit()

        self.DishPriceRecalculate(DishID)   #   Изменяет объем ингредиента в рецепте

    def DishPriceRecalculate(self, DishID):
        recipe = self.GetRecipe(DishID)
        ingredients = self.GetIngredientsDict()

        total_price = sum(recipe[ingr] * ingredients[int(ingr)]['price'] for ingr in recipe)

        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE dishes SET price = ? WHERE id = ?""", (round((total_price * 1.11), 2), DishID))
            conn.commit()   #   Пересчитывает и обновляет цену блюда

    def GetDishName(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT name FROM dishes WHERE id = ?""", (id,))
            return cursor.fetchone()
        
    def GetDishInfo(self, id):
        return {'id': id, 'Name': self.GetDishName(id), 'Recipe': self.GetRecipe(id)} #   Возвращает информацию о блюде по id {'id': int(id), 'Name': '', 'Recipe': []}
    
    ##################\ Для страницы users /##################
    
    def GetUserList(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users""")
            return cursor.fetchall()    #   Получает список всех пользователей из базы данных
    
    def NewUser(self, username):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
            user = cursor.fetchone()
            if user:
                return ["Ошибка", "Такой пользователь уже существует"]

            cursor.execute("""INSERT INTO users (username, isactive) VALUES (?, ?)""", (username, True))
            conn.commit()
        
        return ["успех", "Пользователь успешно добавлен"]  #   Добавляет пользователя
    
    def ChangeUserStatus(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE users SET isactive = NOT isactive WHERE id = ?""", (id,))
            conn.commit()   # Меняет статус пользователя
        
    def EditUserName(self, id, username):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))

            if cursor.fetchone():
                return ["Ошибка", "Такой пользователь уже существует"]
            
            cursor.execute("""UPDATE users SET username = ? WHERE id = ?""", (username, id))
            conn.commit()
        return ["Успех", "Имя пользователя изменено"]   #   Меняет имя пользователя
    
    def DeleteUser(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM users WHERE id = ?""", (id,))
            conn.commit()   #   Удаляет пользователя

    def GetUser(self, id):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))
            return cursor.fetchone()    #   Возвращает информацию о пользователе
        
    ##################\ Для страницы reports /##################
    
    def GetReports(self, month, user=0):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM transactions WHERE data LIKE ?{'' if int(user) == 0 else f' AND person_id = {user}'}""", (str(month) + "%",))
            return cursor.fetchall()
        
    def DeleteOrder(self, OrderID):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM transactions WHERE order_id = ?""", (OrderID,))
            
    ##################\ Для страницы settings /##################
    def UpdateSettings(self, parametr, value):
        
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
        
            if parametr == "OrderConfirmationType":
                old_value = self.GetOrderConfirmationType()
                cursor.execute(f"""UPDATE 'settings' SET Value = ? WHERE parameter = 'OrderConfirmationType'""", (json.dumps([value, old_value[1]]),))
            
            elif parametr == "OrderAutoConfirmationTime":
                old_value = self.GetOrderConfirmationType()
                cursor.execute(f"""UPDATE 'settings' SET Value = ? WHERE parameter = 'OrderConfirmationType'""", (json.dumps([old_value[0], value]),))

        
    def GetOrderConfirmationType(self):
        with sqlite3.connect('stolovka.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT Value FROM 'settings' WHERE parameter = 'OrderConfirmationType'""")
            return json.loads(cursor.fetchall()[0][0])


db = DB()
