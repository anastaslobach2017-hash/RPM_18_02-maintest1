import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sql_learning.db")
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.insert_demo_data()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            order_num INTEGER DEFAULT 0
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            date TEXT NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            expected_query TEXT NOT NULL,
            difficulty TEXT DEFAULT 'easy',
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            city TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            amount INTEGER,
            order_date TEXT,
            FOREIGN KEY (user_id) REFERENCES demo_users(id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            category TEXT,
            stock INTEGER
        )
        """)
        
        self.conn.commit()
    
    def insert_demo_data(self):
        cursor = self.conn.cursor()

        if cursor.execute("SELECT COUNT(*) FROM lessons").fetchone()[0] == 0:
            
            lessons_data = [
                ("Введение в SQL", 
                 """SQL (Structured Query Language) — язык структурированных запросов для работы с реляционными базами данных.

Основные возможности SQL:
• Выборка данных (SELECT)
• Добавление данных (INSERT)
• Обновление данных (UPDATE)
• Удаление данных (DELETE)
• Создание таблиц (CREATE TABLE)
• Изменение структуры (ALTER TABLE)

SQL состоит из нескольких подязыков:
1. DDL (Data Definition Language) — определение структуры данных
2. DML (Data Manipulation Language) — манипуляция данными
3. DCL (Data Control Language) — управление доступом
4. TCL (Transaction Control Language) — управление транзакциями

Пример простого запроса:
SELECT * FROM users;
— выберет все записи из таблицы users""",
                 1),
                
                ("Оператор SELECT",
                 """SELECT — основной оператор для выборки данных из базы данных.

Синтаксис:
SELECT column1, column2, ... FROM table_name;

Ключевые слова:
• SELECT — указывает, какие столбцы выбрать
• FROM — указывает таблицу для выборки
• WHERE — фильтрует записи по условию
• ORDER BY — сортирует результаты
• LIMIT — ограничивает количество записей

Примеры:
SELECT * FROM users; — все столбцы
SELECT name, age FROM users; — конкретные столбцы
SELECT * FROM users WHERE age > 18; — с условием
SELECT * FROM users ORDER BY name; — с сортировкой""",
                 2),
                
                ("Фильтрация WHERE",
                 """WHERE используется для фильтрации записей по заданным условиям.

Операторы сравнения:
• = (равно)
• <> или != (не равно)
• > (больше)
• < (меньше)
• >= (больше или равно)
• <= (меньше или равно)

Логические операторы:
• AND — оба условия должны быть истинны
• OR — хотя бы одно условие истинно
• NOT — инвертирует условие

Дополнительные операторы:
• BETWEEN — диапазон значений
• IN — список значений
• LIKE — поиск по шаблону
• IS NULL — проверка на пустое значение

Примеры:
SELECT * FROM users WHERE age BETWEEN 18 AND 30;
SELECT * FROM users WHERE city IN ('Москва', 'СПб');
SELECT * FROM users WHERE name LIKE 'А%';""",
                 3),
                
                ("Сортировка ORDER BY",
                 """ORDER BY используется для сортировки результатов запроса.

Синтаксис:
SELECT * FROM table_name ORDER BY column_name [ASC|DESC];

Параметры:
• ASC — по возрастанию (по умолчанию)
• DESC — по убыванию

Можно сортировать по нескольким столбцам:
SELECT * FROM users ORDER BY city ASC, age DESC;

Примеры:
SELECT * FROM products ORDER BY price DESC;
SELECT * FROM orders ORDER BY order_date ASC;""",
                 4),
                
                ("Агрегатные функции",
                 """Агрегатные функции выполняют вычисления над набором значений.

Основные функции:
• COUNT() — количество записей
• SUM() — сумма значений
• AVG() — среднее значение
• MIN() — минимальное значение
• MAX() — максимальное значение

Примеры:
SELECT COUNT(*) FROM users; — количество пользователей
SELECT AVG(age) FROM users; — средний возраст
SELECT SUM(amount) FROM orders; — общая сумма заказов
SELECT MAX(price) FROM products; — максимальная цена

Группировка с GROUP BY:
SELECT city, COUNT(*) FROM users GROUP BY city;""",
                 5),
                
                ("Объединение таблиц JOIN",
                 """JOIN используется для объединения данных из нескольких таблиц.

Типы соединений:
• INNER JOIN — только совпадающие записи
• LEFT JOIN — все записи из левой таблицы + совпадения из правой
• RIGHT JOIN — все записи из правой таблицы + совпадения из левой
• FULL JOIN — все записи из обеих таблиц

Синтаксис:
SELECT * FROM table1
INNER JOIN table2 ON table1.id = table2.table1_id;

Пример:
SELECT users.name, orders.product
FROM users
INNER JOIN orders ON users.id = orders.user_id;""",
                 6),
                
                ("Вставка данных INSERT",
                 """INSERT используется для добавления новых записей в таблицу.

Синтаксис:
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);

Примеры:
INSERT INTO users (name, age, city)
VALUES ('Иван', 25, 'Москва');

INSERT INTO users (name, age, city)
VALUES ('Анна', 30, 'СПб'), ('Петр', 28, 'Казань');

Вставка из другой таблицы:
INSERT INTO archive_users
SELECT * FROM users WHERE age > 60;""",
                 7),
                
                ("Обновление данных UPDATE",
                 """UPDATE используется для изменения существующих записей.

Синтаксис:
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

Примеры:
UPDATE users SET age = 26 WHERE name = 'Иван';

UPDATE products SET price = price * 1.1 WHERE category = 'Электроника';

UPDATE users SET city = 'Москва' WHERE city = 'Московская область';

Важно: всегда используйте WHERE, иначе обновятся все записи!""",
                 8),
                
                ("Удаление данных DELETE",
                 """DELETE используется для удаления записей из таблицы.

Синтаксис:
DELETE FROM table_name WHERE condition;

Примеры:
DELETE FROM users WHERE id = 5;

DELETE FROM orders WHERE order_date < '2024-01-01';

DELETE FROM products WHERE stock = 0;

Важно: всегда используйте WHERE, иначе удалится вся таблица!

Очистка таблицы без удаления структуры:
TRUNCATE TABLE users;""",
                 9),
                
                ("Создание таблиц CREATE TABLE",
                 """CREATE TABLE создаёт новую таблицу в базе данных.

Синтаксис:
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...
);

Типы данных:
• INTEGER — целые числа
• REAL — числа с плавающей точкой
• TEXT — текстовые строки
• BLOB — бинарные данные
• DATE/DATETIME — даты и время

Ограничения:
• PRIMARY KEY — первичный ключ
• NOT NULL — обязательное поле
• UNIQUE — уникальное значение
• DEFAULT — значение по умолчанию
• FOREIGN KEY — внешний ключ

Пример:
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
);""",
                 10)
            ]
            
            for title, content, order_num in lessons_data:
                cursor.execute(
                    "INSERT INTO lessons (title, content, order_num) VALUES (?, ?, ?)",
                    (title, content, order_num)
                )
                lesson_id = cursor.lastrowid
                
                self._insert_questions(cursor, lesson_id, title)
                
                self._insert_exercises(cursor, lesson_id, title)
        
        if cursor.execute("SELECT COUNT(*) FROM demo_users").fetchone()[0] == 0:
            self._insert_demo_tables_data(cursor)
        
        self.conn.commit()
    
    def _insert_questions(self, cursor, lesson_id, topic):
        questions_map = {
            "Введение в SQL": [
                ("Что означает аббревиатура SQL?", "Structured Query Language",
                 ["Structured Query Language", "Simple Query Language", "System Query Logic", "Standard Question List"]),
                ("Какой оператор используется для выборки данных?", "SELECT",
                 ["SELECT", "INSERT", "UPDATE", "DELETE"]),
            ],
            "Оператор SELECT": [
                ("Что делает оператор SELECT?", "Выбирает данные из таблицы",
                 ["Выбирает данные из таблицы", "Удаляет таблицу", "Создаёт таблицу", "Обновляет данные"]),
                ("Как выбрать все столбцы?", "SELECT *",
                 ["SELECT *", "SELECT ALL", "SELECT EVERY", "SELECT FULL"]),
            ],
            "Фильтрация WHERE": [
                ("Какой оператор используется для фильтрации?", "WHERE",
                 ["WHERE", "WHEN", "WHICH", "WHAT"]),
                ("Какой оператор означает 'не равно'?", "<> или !=",
                 ["<> или !=", "==", "<>", "=!"]),
            ],
            "Сортировка ORDER BY": [
                ("Как сортировать по убыванию?", "ORDER BY ... DESC",
                 ["ORDER BY ... DESC", "ORDER BY ... ASC", "SORT DESC", "ORDER DOWN"]),
                ("Сортировка по умолчанию?", "По возрастанию (ASC)",
                 ["По возрастанию (ASC)", "По убыванию (DESC)", "Без сортировки", "Случайно"]),
            ],
            "Агрегатные функции": [
                ("Какая функция считает количество записей?", "COUNT()",
                 ["COUNT()", "SUM()", "TOTAL()", "NUMBER()"]),
                ("Какая функция вычисляет среднее?", "AVG()",
                 ["AVG()", "MEAN()", "AVERAGE()", "MEDIAN()"]),
            ],
            "Объединение таблиц JOIN": [
                ("Какой JOIN возвращает только совпадения?", "INNER JOIN",
                 ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]),
                ("Какой JOIN возвращает все записи из левой таблицы?", "LEFT JOIN",
                 ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "OUTER JOIN"]),
            ],
            "Вставка данных INSERT": [
                ("Какой оператор добавляет данные?", "INSERT",
                 ["INSERT", "ADD", "CREATE", "NEW"]),
                ("Можно ли вставить несколько записей одним запросом?", "Да",
                 ["Да", "Нет", "Только в PostgreSQL", "Только в MySQL"]),
            ],
            "Обновление данных UPDATE": [
                ("Какой оператор изменяет данные?", "UPDATE",
                 ["UPDATE", "CHANGE", "MODIFY", "ALTER"]),
                ("Что будет без WHERE в UPDATE?", "Обновятся все записи",
                 ["Обновятся все записи", "Ошибка", "Ничего не изменится", "Удалится таблица"]),
            ],
            "Удаление данных DELETE": [
                ("Какой оператор удаляет данные?", "DELETE",
                 ["DELETE", "REMOVE", "DROP", "CLEAR"]),
                ("Как очистить таблицу полностью?", "TRUNCATE TABLE",
                 ["TRUNCATE TABLE", "DELETE ALL", "CLEAR TABLE", "EMPTY TABLE"]),
            ],
            "Создание таблиц CREATE TABLE": [
                ("Как создать новую таблицу?", "CREATE TABLE",
                 ["CREATE TABLE", "NEW TABLE", "MAKE TABLE", "ADD TABLE"]),
                ("Что означает PRIMARY KEY?", "Первичный ключ",
                 ["Первичный ключ", "Главная таблица", "Основной индекс", "Уникальное поле"]),
            ],
        }
        
        questions = questions_map.get(topic, [])
        for q_text, correct, answers in questions:
            cursor.execute(
                "INSERT INTO questions (lesson_id, question, correct_answer) VALUES (?, ?, ?)",
                (lesson_id, q_text, correct)
            )
            q_id = cursor.lastrowid
            for ans in answers:
                cursor.execute(
                    "INSERT INTO answers (question_id, answer_text) VALUES (?, ?)",
                    (q_id, ans)
                )
    
    def _insert_exercises(self, cursor, lesson_id, topic):
        """Добавляет практические упражнения для урока"""
        exercises_map = {
            "Введение в SQL": [
                ("Первый запрос", "Выберите все данные из таблицы demo_users", 
                 "SELECT * FROM demo_users;", "easy"),
            ],
            "Оператор SELECT": [
                ("Выбор столбцов", "Выберите только name и age из demo_users", 
                 "SELECT name, age FROM demo_users;", "easy"),
                ("Выбор с условием", "Выберите пользователей старше 25 лет", 
                 "SELECT * FROM demo_users WHERE age > 25;", "medium"),
            ],
            "Фильтрация WHERE": [
                ("Фильтр по городу", "Найдите пользователей из Москвы", 
                 "SELECT * FROM demo_users WHERE city = 'Москва';", "easy"),
                ("Диапазон значений", "Найдите пользователей от 20 до 30 лет", 
                 "SELECT * FROM demo_users WHERE age BETWEEN 20 AND 30;", "medium"),
            ],
            "Сортировка ORDER BY": [
                ("Сортировка по имени", "Отсортируйте пользователей по имени", 
                 "SELECT * FROM demo_users ORDER BY name;", "easy"),
                ("Сортировка по возрасту", "Отсортируйте по возрасту (старшие сначала)", 
                 "SELECT * FROM demo_users ORDER BY age DESC;", "medium"),
            ],
            "Агрегатные функции": [
                ("Подсчёт пользователей", "Посчитайте количество пользователей", 
                 "SELECT COUNT(*) FROM demo_users;", "easy"),
                ("Средний возраст", "Вычислите средний возраст пользователей", 
                 "SELECT AVG(age) FROM demo_users;", "medium"),
            ],
            "Объединение таблиц JOIN": [
                ("Простое соединение", "Соедините users и orders по user_id", 
                 "SELECT * FROM demo_users INNER JOIN demo_orders ON demo_users.id = demo_orders.user_id;", "hard"),
            ],
            "Вставка данных INSERT": [
                ("Добавить пользователя", "Добавьте нового пользователя с именем 'Тест'", 
                 "INSERT INTO demo_users (name, age, city) VALUES ('Тест', 25, 'Москва');", "medium"),
            ],
            "Обновление данных UPDATE": [
                ("Изменить возраст", "Измените возраст пользователя с id=1 на 30", 
                 "UPDATE demo_users SET age = 30 WHERE id = 1;", "medium"),
            ],
            "Удаление данных DELETE": [
                ("Удалить запись", "Удалите пользователя с id=1", 
                 "DELETE FROM demo_users WHERE id = 1;", "medium"),
            ],
            "Создание таблиц CREATE TABLE": [
                ("Создать таблицу", "Создайте таблицу test_table с полями id и name", 
                 "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);", "hard"),
            ],
        }
        
        exercises = exercises_map.get(topic, [])
        for title, desc, expected, difficulty in exercises:
            cursor.execute(
                "INSERT INTO exercises (lesson_id, title, description, expected_query, difficulty) VALUES (?, ?, ?, ?, ?)",
                (lesson_id, title, desc, expected, difficulty)
            )
    
    def _insert_demo_tables_data(self, cursor):
        users_data = [
            ('Иван Петров', 25, 'ivan@example.com', 'Москва'),
            ('Анна Сидорова', 30, 'anna@example.com', 'СПб'),
            ('Петр Иванов', 28, 'petr@example.com', 'Казань'),
            ('Мария Козлова', 35, 'maria@example.com', 'Москва'),
            ('Дмитрий Волков', 22, 'dmitry@example.com', 'СПб'),
        ]
        cursor.executemany(
            "INSERT INTO demo_users (name, age, email, city) VALUES (?, ?, ?, ?)",
            users_data
        )
        
        orders_data = [
            (1, 'Ноутбук', 50000, '2024-01-15'),
            (2, 'Телефон', 30000, '2024-01-20'),
            (1, 'Мышь', 1500, '2024-02-01'),
            (3, 'Клавиатура', 3000, '2024-02-05'),
            (4, 'Монитор', 15000, '2024-02-10'),
        ]
        cursor.executemany(
            "INSERT INTO demo_orders (user_id, product, amount, order_date) VALUES (?, ?, ?, ?)",
            orders_data
        )
        
        products_data = [
            ('Ноутбук', 50000.0, 'Электроника', 10),
            ('Телефон', 30000.0, 'Электроника', 25),
            ('Мышь', 1500.0, 'Аксессуары', 50),
            ('Клавиатура', 3000.0, 'Аксессуары', 30),
            ('Монитор', 15000.0, 'Электроника', 15),
        ]
        cursor.executemany(
            "INSERT INTO demo_products (name, price, category, stock) VALUES (?, ?, ?, ?)",
            products_data
        )
    
    def get_lessons(self):
        return self.conn.execute(
            "SELECT * FROM lessons ORDER BY order_num"
        ).fetchall()
    
    def get_questions(self, lesson_id):
        return self.conn.execute(
            "SELECT * FROM questions WHERE lesson_id = ?",
            (lesson_id,)
        ).fetchall()
    
    def get_answers(self, question_id):
        return self.conn.execute(
            "SELECT * FROM answers WHERE question_id = ?",
            (question_id,)
        ).fetchall()
    
    def get_exercises(self, lesson_id):
        return self.conn.execute(
            "SELECT * FROM exercises WHERE lesson_id = ?",
            (lesson_id,)
        ).fetchall()
    
    def get_demo_table_schema(self, table_name):
        try:
            return self.conn.execute(
                f"PRAGMA table_info({table_name})"
            ).fetchall()
        except sqlite3.Error:
            return []
    
    def get_table_data(self, table_name):
        try:
            return self.conn.execute(
                f"SELECT * FROM {table_name} LIMIT 10"
            ).fetchall()
        except sqlite3.Error:
            return []
    
    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                return {'success': True, 'columns': columns, 'rows': rows, 'error': None}
            else:
                self.conn.commit()
                return {'success': True, 'columns': [], 'rows': [], 'error': None, 'message': f'Затронуто строк: {cursor.rowcount}'}
        except sqlite3.Error as e:
            return {'success': False, 'columns': [], 'rows': [], 'error': str(e)}
    
    def save_result(self, score, total):
        self.conn.execute(
            "INSERT INTO results (score, total, date) VALUES (?, ?, ?)",
            (score, total, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.conn.commit()
    
    def get_statistics(self):
        return self.conn.execute(
            "SELECT * FROM results ORDER BY date DESC LIMIT 10"
        ).fetchall()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()