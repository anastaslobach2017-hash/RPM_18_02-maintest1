import json
import os


class TaskModel:
    """Модель - отвечает за данные и бизнес-логику"""

    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []

    def save_tasks(self):
        """Сохранение задач в файл"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, title, description=''):
        """Добавление новой задачи"""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_all_tasks(self):
        """Получение всех задач"""
        return self.tasks

    def get_task(self, task_id):
        """Получение задачи по ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id, **kwargs):
        """Обновление задачи"""
        task = self.get_task(task_id)
        if task:
            task.update(kwargs)
            self.save_tasks()
            return task
        return None

    def delete_task(self, task_id):
        """Удаление задачи"""
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks()

    def toggle_task(self, task_id):
        """Переключение статуса задачи"""
        task = self.get_task(task_id)
        if task:
            task['completed'] = not task['completed']
            self.save_tasks()
            return task
        return None