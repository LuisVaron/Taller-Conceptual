from model import InMemoryTaskRepository, TaskRepository
from view import TkinterTaskView, TaskView
from controller import TaskController

if __name__ == "__main__":
    repository: TaskRepository = InMemoryTaskRepository()
    view: TaskView = TkinterTaskView(lambda: controller)
    controller = TaskController(repository, view)
    view.start_mainloop()