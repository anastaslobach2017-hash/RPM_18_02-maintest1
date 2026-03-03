class TaskController:
    """Контроллер - отвечает за обработку действий пользователя"""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def run(self):
        """Запуск контроллера"""
        while self.running:
            self.view.show_menu()
            choice = self.view.get_input("Выберите действие")
            self.handle_choice(choice)

    def handle_choice(self, choice):
        """Обработка выбора пользователя"""
        actions = {
            '1': self.show_all_tasks,
            '2': self.add_task,
            '3': self.show_task_by_id,
            '4': self.edit_task,
            '5': self.delete_task,
            '6': self.toggle_task,
            '0': self.exit_app
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            self.view.show_message("Неверный выбор. Попробуйте снова.", 'warning')

    def show_all_tasks(self):
        """Показать все задачи"""
        tasks = self.model.get_all_tasks()
        self.view.show_tasks(tasks)

    def add_task(self):
        """Добавить новую задачу"""
        self.view.show_message("Добавление новой задачи", 'info')
        title = self.view.get_input("Введите название задачи")

        if not title:
            self.view.show_message("Название не может быть пустым", 'error')
            return

        description = self.view.get_input("Введите описание (можно пропустить)")

        task = self.model.add_task(title, description)
        self.view.show_message(f"Задача #{task['id']} успешно добавлена", 'success')

    def show_task_by_id(self):
        """Показать задачу по ID"""
        try:
            task_id = int(self.view.get_input("Введите ID задачи"))
            task = self.model.get_task(task_id)
            self.view.show_task(task)
        except ValueError:
            self.view.show_message("Некорректный ID", 'error')

    def edit_task(self):
        """Редактировать задачу"""
        try:
            task_id = int(self.view.get_input("Введите ID задачи для редактирования"))
            task = self.model.get_task(task_id)

            if not task:
                self.view.show_message("Задача не найдена", 'error')
                return

            self.view.show_message(f"Редактирование задачи #{task_id}", 'info')

            new_title = self.view.get_input(f"Новое название (было: {task['title']})")
            new_description = self.view.get_input(f"Новое описание (было: {task['description']})")

            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_description:
                updates['description'] = new_description

            if updates:
                self.model.update_task(task_id, **updates)
                self.view.show_message("Задача обновлена", 'success')
            else:
                self.view.show_message("Нет изменений", 'info')

        except ValueError:
            self.view.show_message("Некорректный ID", 'error')

    def delete_task(self):
        """Удалить задачу"""
        try:
            task_id = int(self.view.get_input("Введите ID задачи для удаления"))
            task = self.model.get_task(task_id)

            if not task:
                self.view.show_message("Задача не найдена", 'error')
                return

            self.view.show_task(task)
            confirm = self.view.get_input("Удалить эту задачу? (д/н)")

            if confirm.lower() in ['д', 'да', 'y', 'yes']:
                self.model.delete_task(task_id)
                self.view.show_message("Задача удалена", 'success')
            else:
                self.view.show_message("Удаление отменено", 'info')

        except ValueError:
            self.view.show_message("Некорректный ID", 'error')

    def toggle_task(self):
        """Переключить статус задачи"""
        try:
            task_id = int(self.view.get_input("Введите ID задачи"))
            task = self.model.toggle_task(task_id)

            if task:
                status = "выполнена" if task['completed'] else "не выполнена"
                self.view.show_message(f"Задача #{task_id} отмечена как {status}", 'success')
            else:
                self.view.show_message("Задача не найдена", 'error')

        except ValueError:
            self.view.show_message("Некорректный ID", 'error')

    def exit_app(self):
        """Выход из приложения"""
        self.view.show_message("До свидания!", 'info')
        self.running = False