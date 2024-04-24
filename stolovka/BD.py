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
        conn.commit()
        conn.close()    #   Создает структуру базы данных, если таковой нет 
        
    def NewOrder(self, data, user, order):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO orders (data, person_id, order_text) VALUES (?, ?, ?)""", (data, user, order))
        conn.commit()
        conn.close()
        return

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
        
    def LoadUserList(self):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users""")
        users = cursor.fetchall()
            
        conn.close()
        
        return users    #   Получает список всех пользователей из базы данных 
    
    def DeleteUser(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()
        
        # Запрос на удаление пользователя по его id
        cursor.execute("""DELETE FROM users WHERE id = ?""", (id,))
        conn.commit()
        conn.close()    #   Удаляет пользователя
        
    def GetUserStatus():
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute("""SELECT isactive FROM users WHERE id = ?""", (id,))

        # Получение результата запроса
        status = cursor.fetchone()

        conn.close()
        return status[0]    #   Получает статус пользователя. ((Теоретически бесполезная функция))
        
    def ChangeStatus(self, id):
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
    
    def GetUser(self, id):
        conn = sqlite3.connect('stolovka.db')
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))

        # Получение результата запроса
        status = cursor.fetchone()

        conn.close()
        return status

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
    
db = DB()
