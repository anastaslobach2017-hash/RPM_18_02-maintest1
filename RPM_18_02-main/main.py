from api.model import TaskModel
from api.views import TaskView
from api.controller import TaskController


def main():
    """Точка входа в приложение"""
    # Создаем компоненты MVC
    model = TaskModel()
    view = TaskView()
    controller = TaskController(model, view)

    # Запускаем приложение
    controller.run()


if __name__ == "__main__":
    main()