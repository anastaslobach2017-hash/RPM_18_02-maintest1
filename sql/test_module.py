import tkinter as tk
from tkinter import messagebox

class TestWindow:
    def __init__(self, root, db, lesson_id, lesson_title):
        self.db = db
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title
        self.questions = db.get_questions(lesson_id)
        self.index = 0
        self.score = 0
        
        self.window = tk.Toplevel(root)
        self.window.title(f"Тест: {lesson_title}")
        self.window.geometry("500x400")
        self.window.configure(bg="#2c3e50")
        self.window.resizable(False, False)
        
        self._create_interface()
        self._load_question()
    
    def _create_interface(self):
        """Создаёт интерфейс окна теста"""
        
        title = tk.Label(
            self.window,
            text=f"✅ Тестирование",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=10)
        
        self.progress_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.progress_label.pack(pady=5)
        
        self.question_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            wraplength=450,
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        self.question_label.pack(fill=tk.X, padx=10, pady=10)
        
        self.var = tk.StringVar()
        
        self.buttons = []
        for i in range(4):
            btn = tk.Radiobutton(
                self.window,
                variable=self.var,
                value="",
                font=("Arial", 11),
                bg="#ecf0f1",
                fg="#2c3e50",
                selectcolor="#27ae60",
                anchor="w",
                padx=20
            )
            btn.pack(fill=tk.X, padx=20, pady=2)
            self.buttons.append(btn)
        
        self.next_btn = tk.Button(
            self.window,
            text="Далее →",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=self.next,
            width=20
        )
        self.next_btn.pack(pady=20)
    
    def _load_question(self):
        """Загружает текущий вопрос"""
        if self.index >= len(self.questions):
            self._show_result()
            return
        
        q = self.questions[self.index]
        
        self.progress_label.config(
            text=f"Вопрос {self.index + 1} из {len(self.questions)}"
        )
        
        self.question_label.config(text=q[2])
        
        answers = self.db.get_answers(q[0])
        
        for i, btn in enumerate(self.buttons):
            if i < len(answers):
                btn.config(text=answers[i][2], value=answers[i][2], state=tk.NORMAL)
            else:
                btn.config(text="", value="", state=tk.DISABLED)
        
        self.var.set("")
    
    def next(self):
        """Переходит к следующему вопросу"""
        selected = self.var.get()
        
        if not selected:
            messagebox.showwarning("Внимание", "Выберите вариант ответа!")
            return
        
        q = self.questions[self.index]
        
        if selected == q[3]:
            self.score += 1
        
        self.index += 1
        self._load_question()
    
    def _show_result(self):
        """Отображает результат теста"""
        percentage = (self.score / len(self.questions) * 100) if self.questions else 0
        
        self.question_label.config(
            text=f"🎉 Тест завершён!\n\nВаш результат: {self.score}/{len(self.questions)} ({percentage:.1f}%)"
        )
        
        self.progress_label.config(text="")
        
        if percentage >= 80:
            color = "#27ae60"
            message = "Отлично! 🌟"
        elif percentage >= 60:
            color = "#f39c12"
            message = "Хорошо! 👍"
        else:
            color = "#e74c3c"
            message = "Стоит повторить материал 📚"
        
        self.question_label.config(bg=color)
        
        self.db.save_result(self.score, len(self.questions))
        

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        self.next_btn.config(text="Закрыть", command=self.window.destroy)
        
        messagebox.showinfo("Результат", f"{message}\n\nПравильных ответов: {self.score} из {len(self.questions)}")