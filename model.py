import abc

class Task:
    """Representa una única tarea (SRP)."""
    _id_counter = 0
    def __init__(self, description: str, done: bool = False):
        Task._id_counter += 1
        self.id = Task._id_counter
        self.description = description
        self.done = done

    def __str__(self):
        status = "Hecha" if self.done else "Pendiente"
        return f"[{self.id}] {self.description} ({status})"

class TaskRepository(abc.ABC):
    """
    Interfaz (Clase Base Abstracta) para el almacenamiento de tareas (OCP, LSP, ISP).
    """
    @abc.abstractmethod
    def add_task(self, task: Task) -> bool:
        """Añade una tarea al repositorio."""
        pass

    @abc.abstractmethod
    def get_task(self, task_id: int) -> Task | None:
        """Obtiene una tarea por su ID."""
        pass

    @abc.abstractmethod
    def get_all_tasks(self) -> list[Task]:
        """Obtiene todas las tareas."""
        pass

    @abc.abstractmethod
    def update_task(self, task: Task) -> bool:
        """Actualiza una tarea existente."""
        pass

    @abc.abstractmethod
    def delete_task(self, task_id: int) -> bool:
        """Elimina una tarea por su ID."""
        pass

class InMemoryTaskRepository(TaskRepository):
    """
    Implementación concreta del repositorio que guarda las tareas en memoria (SRP).
    """
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        Task._id_counter = 0

    def add_task(self, task: Task) -> bool:
        if task.id in self._tasks:
            print(f"Error: Ya existe una tarea con ID {task.id}")
            return False
        self._tasks[task.id] = task
        print(f"Tarea '{task.description}' añadida con ID {task.id}.")
        return True

    def get_task(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def update_task(self, updated_task: Task) -> bool:
        if updated_task.id in self._tasks:
            self._tasks[updated_task.id] = updated_task
            print(f"Tarea ID {updated_task.id} actualizada.")
            return True
        else:
            print(f"Error: Tarea ID {updated_task.id} no encontrada para actualizar.")
            return False

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            print(f"Tarea ID {task_id} eliminada.")
            return True
        else:
             print(f"Error: Tarea ID {task_id} no encontrada para eliminar.")
             return False