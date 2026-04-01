import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from test_module import TestWindow
from practice_module import PracticeWindow

class App:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Обучение SQL")
        self.root.geometry("900x600")
        self.root.configure(bg="#2c3e50")
        
        self.current_lesson_id = None
        self.current_lesson_title = None
        
        self._create_header()
        self._create_navigation()
        self._create_content_area()
        self._create_status_bar()
        
        self.load_lessons()
        self.lesson_list.bind("<<ListboxSelect>>", self.show_lesson)
    
    def _create_header(self):
        title = tk.Label(
            self.root, 
            text="📚 Обучение SQL", 
            font=("Arial", 20, "bold"), 
            bg="#2c3e50", 
            fg="white"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            self.root,
            text="Интерактивный курс по основам баз данных",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subtitle.pack(pady=0)
    
    def _create_navigation(self):
        nav_frame = tk.Frame(self.root, bg="#34495e")
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        left_frame = tk.Frame(nav_frame, bg="#34495e")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        lesson_label = tk.Label(
            left_frame,
            text="Уроки:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        )
        lesson_label.pack(anchor="w", padx=5)
        
        self.lesson_list = tk.Listbox(
            left_frame,
            width=35,
            height=8,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            selectbackground="#27ae60",
            selectforeground="white"
        )
        self.lesson_list.pack(padx=5, pady=5)
        
        right_frame = tk.Frame(nav_frame, bg="#34495e")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.theory_btn = tk.Button(
            right_frame,
            text="📖 Теория",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            command=self.show_theory,
            width=12
        )
        self.theory_btn.pack(pady=2)
        
        self.test_btn = tk.Button(
            right_frame,
            text="✅ Тест",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=self.start_test,
            width=12
        )
        self.test_btn.pack(pady=2)
        
        self.practice_btn = tk.Button(
            right_frame,
            text="💻 Практика",
            font=("Arial", 11),
            bg="#e67e22",
            fg="white",
            command=self.start_practice,
            width=12
        )
        self.practice_btn.pack(pady=2)
        
        self.stats_btn = tk.Button(
            right_frame,
            text="📊 Статистика",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            command=self.show_statistics,
            width=12
        )
        self.stats_btn.pack(pady=2)
    
    def _create_content_area(self):
        """Создаёт основную область контента"""
        content_frame = tk.Frame(self.root, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.content_text = tk.Text(
            content_frame,
            height=20,
            width=80,
            font=("Consolas", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.content_text, command=self.content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.config(yscrollcommand=scrollbar.set)
    
    def _create_status_bar(self):
        """Создаёт строку состояния"""
        self.status_var = tk.StringVar()
        self.status_var.set("Выберите урок из списка")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            anchor="w"
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def load_lessons(self):
        """Загружает список уроков"""
        self.lessons = self.db.get_lessons()
        self.lesson_list.delete(0, tk.END)
        for lesson in self.lessons:
            self.lesson_list.insert(tk.END, f"{lesson[3]}. {lesson[1]}")
    
    def show_lesson(self, event):
        """Отображает выбранный урок"""
        index = self.lesson_list.curselection()
        if not index:
            return
        
        lesson = self.lessons[index[0]]
        self.current_lesson_id = lesson[0]
        self.current_lesson_title = lesson[1]
        
        self.status_var.set(f"Урок: {lesson[1]}")
        self.show_theory()
    
    def show_theory(self):
        """Отображает теоретический материал"""
        if not hasattr(self, 'current_lesson_id'):
            messagebox.showwarning("Внимание", "Сначала выберите урок!")
            return
        
        lesson = self.db.conn.execute(
            "SELECT * FROM lessons WHERE id = ?",
            (self.current_lesson_id,)
        ).fetchone()
        
        if lesson:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, f"ТЕМА: {lesson[1]}\n\n")
            self.content_text.insert(tk.END, lesson[2])
            self.status_var.set(f"Просмотр теории: {lesson[1]}")
    
    def start_test(self):
        """Запускает тестирование по уроку"""
        if not hasattr(self, 'current_lesson_id'):
            messagebox.showwarning("Внимание", "Сначала выберите урок!")
            return
        
        questions = self.db.get_questions(self.current_lesson_id)
        if not questions:
            messagebox.showinfo("Информация", "Для этого урока нет тестовых вопросов")
            return
        
        TestWindow(self.root, self.db, self.current_lesson_id, self.current_lesson_title)
        self.status_var.set(f"Тестирование: {self.current_lesson_title}")
    
    def start_practice(self):
        """Запускает практические упражнения"""
        if not hasattr(self, 'current_lesson_id'):
            messagebox.showwarning("Внимание", "Сначала выберите урок!")
            return
        
        exercises = self.db.get_exercises(self.current_lesson_id)
        if not exercises:
            messagebox.showinfo("Информация", "Для этого урока нет практических заданий")
            return
        
        PracticeWindow(self.root, self.db, self.current_lesson_id, self.current_lesson_title)
        self.status_var.set(f"Практика: {self.current_lesson_title}")
    
    def show_statistics(self):
        """Отображает статистику прохождения"""
        results = self.db.get_statistics()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        stats_window.geometry("500x400")
        stats_window.configure(bg="#2c3e50")
        
        title = tk.Label(
            stats_window,
            text="📊 История тестирований",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=10)
        
        text = tk.Text(
            stats_window,
            height=15,
            width=50,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        if results:
            for result in results:
                date = result[3]
                score = result[1]
                total = result[2]
                percentage = (score / total * 100) if total > 0 else 0
                text.insert(tk.END, f"{date} | Результат: {score}/{total} ({percentage:.1f}%)\n")
        else:
            text.insert(tk.END, "Пока нет результатов тестирований")
        
        text.config(state=tk.DISABLED)
        
        close_btn = tk.Button(
            stats_window,
            text="Закрыть",
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            command=stats_window.destroy
        )
        close_btn.pack(pady=5)