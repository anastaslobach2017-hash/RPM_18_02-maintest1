import tkinter as tk
from tkinter import ttk, messagebox

class PracticeWindow:
    def __init__(self, root, db, lesson_id, lesson_title):
        self.db = db
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title
        self.exercises = db.get_exercises(lesson_id)
        self.current_index = 0
        
        self.window = tk.Toplevel(root)
        self.window.title(f"Практика: {lesson_title}")
        self.window.geometry("1000x700")
        self.window.configure(bg="#2c3e50")
        
        self._create_interface()
        self._load_exercise()
    
    def _create_interface(self):
        """Создаёт интерфейс окна практики"""
        title = tk.Label(
            self.window,
            text=f"💻 Практические упражнения",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=10)
        
        self.progress_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.progress_label.pack(pady=5)
        
        task_frame = tk.Frame(self.window, bg="#34495e")
        task_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.task_label = tk.Label(
            task_frame,
            text="",
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            wraplength=900,
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        self.task_label.pack(fill=tk.X)

        top_panel = tk.Frame(self.window, bg="#2c3e50")
        top_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        left_panel = tk.Frame(top_panel, bg="#2c3e50")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tables_label = tk.Label(
            left_panel,
            text="📋 Доступные таблицы:",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        tables_label.pack(anchor="w", pady=(0, 5))
        
        self.tables_combo = ttk.Combobox(
            left_panel,
            values=["demo_users", "demo_orders", "demo_products"],
            state="readonly",
            width=25,
            font=("Arial", 11)
        )
        self.tables_combo.pack(anchor="w", pady=(0, 10))
        self.tables_combo.bind("<<ComboboxSelected>>", self.show_table_schema)
        
        # Структура таблицы - УВЕЛИЧЕННАЯ ОБЛАСТЬ
        schema_frame = tk.LabelFrame(
            left_panel,
            text="📊 Структура таблицы",
            font=("Arial", 11, "bold"),
            bg="#34495e",
            fg="white"
        )
        schema_frame.pack(fill=tk.BOTH, expand=True)
        
        self.schema_text = tk.Text(
            schema_frame,
            height=12,
            width=50,
            font=("Consolas", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            wrap=tk.NONE
        )
        schema_scrollbar_y = tk.Scrollbar(schema_frame, orient=tk.VERTICAL, command=self.schema_text.yview)
        schema_scrollbar_x = tk.Scrollbar(schema_frame, orient=tk.HORIZONTAL, command=self.schema_text.xview)
        self.schema_text.configure(yscrollcommand=schema_scrollbar_y.set, xscrollcommand=schema_scrollbar_x.set)
        
        self.schema_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        schema_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        schema_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Правая часть: результаты запроса
        right_panel = tk.Frame(top_panel, bg="#2c3e50")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        result_label = tk.Label(
            right_panel,
            text="📈 Результат запроса:",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        result_label.pack(anchor="w", pady=(0, 5))
        
        self.result_display = tk.Text(
            right_panel,
            height=12,
            width=50,
            font=("Consolas", 10),
            bg="#d5f5e3",
            fg="#2c3e50",
            wrap=tk.NONE
        )
        result_scrollbar_y = tk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.result_display.yview)
        result_scrollbar_x = tk.Scrollbar(right_panel, orient=tk.HORIZONTAL, command=self.result_display.xview)
        self.result_display.configure(yscrollcommand=result_scrollbar_y.set, xscrollcommand=result_scrollbar_x.set)
        
        self.result_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        result_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Поле для ввода запроса
        query_frame = tk.Frame(self.window, bg="#2c3e50")
        query_frame.pack(fill=tk.X, padx=10, pady=10)
        
        query_label = tk.Label(
            query_frame,
            text="Ваш SQL-запрос:",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        query_label.pack(anchor="w", pady=(0, 5))
        
        self.query_text = tk.Text(
            query_frame,
            height=5,
            width=80,
            font=("Consolas", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.query_text.pack()
        
        # Кнопки
        buttons_frame = tk.Frame(self.window, bg="#2c3e50")
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.check_btn = tk.Button(
            buttons_frame,
            text="✓ Проверить",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.check_query,
            width=15,
            height=2
        )
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(
            buttons_frame,
            text="Далее →",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            command=self.next_exercise,
            width=15,
            height=2
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.hint_btn = tk.Button(
            buttons_frame,
            text="💡 Подсказка",
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            command=self.show_hint,
            width=15,
            height=2
        )
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_label = tk.Label(
            self.window,
            text="Введите SQL-запрос и нажмите 'Проверить'",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.status_label.pack(pady=5)
    
    def _load_exercise(self):
        """Загружает текущее упражнение"""
        if self.current_index >= len(self.exercises):
            self._show_completion()
            return
        
        exercise = self.exercises[self.current_index]
        self.current_exercise = exercise
        
        self.progress_label.config(
            text=f"Задание {self.current_index + 1} из {len(self.exercises)}"
        )
        
        self.task_label.config(
            text=f"📝 {exercise[2]}: {exercise[3]}"
        )
        
        self.query_text.delete(1.0, tk.END)
        
        # Очищаем результат
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, "📊 Здесь появится результат вашего запроса...\n\n")
        self.result_display.insert(tk.END, "Выполните запрос правильно, чтобы увидеть данные из таблицы.")
        self.result_display.config(bg="#d5f5e3")
        
        self.status_label.config(text="Введите SQL-запрос и нажмите 'Проверить'")
        
        self.tables_combo.current(0)
        self.show_table_schema(None)
    
    def show_table_schema(self, event):
        """Отображает структуру выбранной таблицы"""
        table_name = self.tables_combo.get()
        schema = self.db.get_demo_table_schema(table_name)
        
        self.schema_text.delete(1.0, tk.END)
        self.schema_text.insert(tk.END, f"📋 Таблица: {table_name}\n\n")
        
        if not schema:
            self.schema_text.insert(tk.END, "Таблица не найдена или пуста")
            return
        
        self.schema_text.insert(tk.END, f"{'№':<3} {'Столбец':<15} {'Тип':<12} {'NOT NULL':<10} {'PK':<5}\n")
        self.schema_text.insert(tk.END, "-" * 50 + "\n")
        
        for i, col in enumerate(schema, 1):
            col_name = col[1] if col[1] else "N/A"
            col_type = col[2] if col[2] else "TEXT"
            not_null = "✓" if col[3] else ""
            pk = "✓" if col[5] else ""
            
            self.schema_text.insert(
                tk.END,
                f"{i:<3} {col_name:<15} {col_type:<12} {not_null:<10} {pk:<5}\n"
            )
        
        self.schema_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.schema_text.insert(tk.END, "📄 Пример данных (первые 5 строк):\n\n")
        
        data = self.db.get_table_data(table_name)
        if data:
            columns = [col[1] for col in schema]
            self.schema_text.insert(tk.END, " | ".join(columns) + "\n")
            self.schema_text.insert(tk.END, "-" * 40 + "\n")
            
            for row in data[:5]:
                self.schema_text.insert(tk.END, " | ".join(str(x) for x in row) + "\n")
        else:
            self.schema_text.insert(tk.END, "Таблица пуста")
    
    def check_query(self):

        user_query = self.query_text.get(1.0, tk.END).strip()
        
        if not user_query:
            messagebox.showwarning("Внимание", "Введите SQL-запрос!")
            return
        
        result = self.db.execute_query(user_query)
        
        self.result_display.delete(1.0, tk.END)
        
        if not result['success']:
            self.result_display.insert(tk.END, "❌ Ошибка выполнения запроса:\n\n")
            self.result_display.insert(tk.END, result['error'])
            self.result_display.config(bg="#fadbd8")
            self.status_label.config(text="❌ Ошибка в запросе. Проверьте синтаксис.")
            return
        
        expected = self.current_exercise[4]
        
        if user_query.upper().startswith('SELECT'):
            expected_result = self.db.execute_query(expected)
            
            if result['rows']:
                self.result_display.insert(tk.END, "✅ Запрос выполнен успешно!\n\n")
                self.result_display.insert(tk.END, "📊 Результат:\n\n")
                
                self.result_display.insert(tk.END, " | ".join(result['columns']) + "\n")
                self.result_display.insert(tk.END, "-" * 60 + "\n")
                
                for row in result['rows']:
                    self.result_display.insert(tk.END, " | ".join(str(x) for x in row) + "\n")
                
                self.result_display.insert(tk.END, f"\n✓ Найдено строк: {len(result['rows'])}")
            else:
                self.result_display.insert(tk.END, "ℹ️ Запрос выполнен, но результат пуст")
            
            if (result['columns'] == expected_result['columns'] and 
                set(map(tuple, result['rows'])) == set(map(tuple, expected_result['rows']))):
                self._show_success(expected)
            else:
                self.result_display.insert(tk.END, "\n\n⚠️ Результат не совпадает с ожидаемым")
                self.status_label.config(text="⚠️ Запрос выполнен, но результат неверный")
                self.result_display.config(bg="#fcf3cf")
        else:

            self.result_display.insert(tk.END, f"✅ Запрос выполнен!\n\n")
            if 'message' in result:
                self.result_display.insert(tk.END, result['message'])
            
            if self._normalize_query(user_query) == self._normalize_query(expected):
                self._show_success(expected)
            else:
                self.status_label.config(text="✓ Запрос выполнен")
                self.result_display.config(bg="#d5f5e3")
    
    def _normalize_query(self, query):
        """Нормализует запрос для сравнения"""
        return ' '.join(query.upper().split())
    
    def _show_success(self, expected_query):
        """Отображает сообщение об успехе"""
        self.status_label.config(text="✅ Правильно! Отличная работа!")
        self.result_display.insert(tk.END, "\n\n" + "="*60 + "\n")
        self.result_display.insert(tk.END, "🎉 ПРАВИЛЬНО!\n")
        self.result_display.insert(tk.END, "="*60 + "\n\n")
        self.result_display.insert(tk.END, "✓ Ваш запрос дал правильный результат!\n\n")
        self.result_display.config(bg="#d5f5e3")
    
    def _show_completion(self):
        """Отображает сообщение о завершении"""
        self.task_label.config(text="🎉 Все упражнения выполнены!")
        self.query_text.config(state=tk.DISABLED)
        self.check_btn.config(state=tk.DISABLED)
        self.next_btn.config(text="Закрыть", command=self.window.destroy)
        self.hint_btn.config(state=tk.DISABLED)
        
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, "🎊 Поздравляем!\n\n")
        self.result_display.insert(tk.END, "Вы выполнили все практические задания по теме:\n")
        self.result_display.insert(tk.END, f"«{self.lesson_title}»\n\n")
        self.result_display.insert(tk.END, "Вы можете вернуться к списку уроков и выбрать другую тему.")
        self.result_display.config(bg="#d5f5e3")
        
        self.status_label.config(text="✅ Все задания выполнены!")
    
    def next_exercise(self):
        """Переходит к следующему упражнению"""
        self.current_index += 1
        self._load_exercise()
    
    def show_hint(self):
        """Показывает подсказку"""
        hint = self.current_exercise[4]
        hint_preview = hint.split()[0:4]
        
        messagebox.showinfo(
            "💡 Подсказка",
            f"Начните запрос с: {' '.join(hint_preview)} ...\n\n"
            f"💡 Обратите внимание:\n"
            f"- Посмотрите структуру таблицы в левой панели\n"
            f"- Используйте правильные имена столбцов\n"
            f"- Проверьте синтаксис SQL"
        )