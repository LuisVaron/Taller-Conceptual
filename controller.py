from model import Task, TaskRepository
from view import TaskView, TkinterTaskView

class TaskController:
    """
    Controlador que conecta Modelo y Vista (SRP).
    Depende de las abstracciones TaskRepository y TaskView (DIP).
    """
    def __init__(self, repository: TaskRepository, view: TaskView):
        self._repository = repository
        self._view = view
        if isinstance(self._view, TkinterTaskView):
            self._view.set_controller(self)

    def load_initial_tasks(self):
        """Carga y muestra las tareas al inicio."""
        tasks = self._repository.get_all_tasks()
        self._view.show_tasks(tasks)

    def add_task(self):
        """Añade una nueva tarea obteniendo la descripción de la vista."""
        description = self._view.get_task_description()
        if description:
            new_task = Task(description=description)
            if self._repository.add_task(new_task):
                 self._view.clear_task_input()
                 self.refresh_view()
            else:
                self._view.show_message("Error", f"No se pudo añadir la tarea '{description}'.")
        else:
            self._view.show_message("Info", "La descripción no puede estar vacía.")

    def mark_task_done(self):
        """Marca una tarea seleccionada como hecha."""
        task_id = self._view.get_selected_task_id()
        if task_id is not None:
            task = self._repository.get_task(task_id)
            if task:
                if not task.done:
                    task.done = True
                    if self._repository.update_task(task):
                         self.refresh_view()
                    else:
                         self._view.show_message("Error", f"No se pudo actualizar la tarea ID {task_id}.")
                else:
                    self._view.show_message("Info", "La tarea ya estaba marcada como hecha.")

    def unmark_task_done(self):
        """Desmarca una tarea seleccionada (la pone como pendiente)."""
        task_id = self._view.get_selected_task_id()
        if task_id is not None:
            task = self._repository.get_task(task_id)
            if task:
                if task.done:
                    task.done = False
                    if self._repository.update_task(task):
                         self.refresh_view()
                    else:
                         self._view.show_message("Error", f"No se pudo actualizar la tarea ID {task_id}.")
                else:
                    self._view.show_message("Info", "La tarea ya estaba pendiente.")

    def delete_task(self):
        """Elimina la tarea seleccionada."""
        task_id = self._view.get_selected_task_id()
        if task_id is not None:
            if self._repository.delete_task(task_id):
                 self.refresh_view()

    def refresh_view(self):
        """Función auxiliar para recargar y mostrar todas las tareas en la vista."""
        tasks = self._repository.get_all_tasks()
        self._view.show_tasks(tasks)