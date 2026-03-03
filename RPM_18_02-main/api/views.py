class TaskView:
    """Представление - отвечает за отображение данных"""

    @staticmethod
    def show_tasks(tasks):
        """Отображение всех задач"""
        if not tasks:
            print("\n📋 Список задач пуст")
            return

        print("\n" + "=" * 50)
        print("📋 СПИСОК ЗАДАЧ")
        print("=" * 50)

        for task in tasks:
            status = "✅" if task['completed'] else "⭕"
            print(f"\n{status} Задача #{task['id']}")
            print(f"   Название: {task['title']}")
            if task['description']:
                print(f"   Описание: {task['description']}")

    @staticmethod
    def show_task(task):
        """Отображение одной задачи"""
        if not task:
            print("\n❌ Задача не найдена")
            return

        status = "Выполнена" if task['completed'] else "Не выполнена"
        print("\n" + "=" * 50)
        print(f"📌 ЗАДАЧА #{task['id']}")
        print("=" * 50)
        print(f"Название: {task['title']}")
        if task['description']:
            print(f"Описание: {task['description']}")
        print(f"Статус: {status}")

    @staticmethod
    def show_message(message, type='info'):
        """Отображение сообщения"""
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        }
        icon = icons.get(type, 'ℹ️')
        print(f"\n{icon} {message}")

    @staticmethod
    def show_menu():
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("📌 ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Показать задачу по ID")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Отметить как выполненную/невыполненную")
        print("0. Выход")
        print("=" * 50)

    @staticmethod
    def get_input(prompt):
        """Получение ввода от пользователя"""
        return input(f"\n{prompt}: ").strip()