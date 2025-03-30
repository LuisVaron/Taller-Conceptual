import abc
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Frame, Label, Entry, Button, Scrollbar, END, SINGLE

from model import Task

class TaskView(abc.ABC):
    """Interfaz (Clase Base Abstracta) para la vista (OCP, LSP, ISP)."""
    @abc.abstractmethod
    def set_controller(self, controller):
        """Establece el controlador para la vista."""
        pass

    @abc.abstractmethod
    def show_tasks(self, tasks: list[Task]):
        """Muestra la lista de tareas."""
        pass

    @abc.abstractmethod
    def show_task_detail(self, task: Task | None):
        """Muestra los detalles de una tarea."""
        pass

    @abc.abstractmethod
    def get_task_description(self) -> str:
        """Obtiene la descripción de la tarea desde la entrada del usuario."""
        pass

    @abc.abstractmethod
    def get_selected_task_id(self) -> int | None:
        """Obtiene el ID de la tarea seleccionada por el usuario."""
        pass

    @abc.abstractmethod
    def show_message(self, title: str, message: str):
        """Muestra un mensaje al usuario."""
        pass

    @abc.abstractmethod
    def clear_task_input(self):
        """Limpia el campo de entrada de la descripción."""
        pass

    @abc.abstractmethod
    def start_mainloop(self):
        """Inicia el bucle principal de la interfaz gráfica."""
        pass


class TkinterTaskView(TaskView):
    """Implementación concreta de la vista con Tkinter (SRP)."""

    def __init__(self, controller_provider):
        self.root = tk.Tk()
        self.root.title("Gestor de Tareas MVC")
        self.root.geometry("550x400")

        self._controller_provider = controller_provider
        self._controller = None

        # Layout
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        input_frame = Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        Label(input_frame, text="Nueva Tarea:").pack(side=tk.LEFT, padx=5)
        self.task_entry = Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.add_button = Button(input_frame, text="Añadir", command=self._on_add_task)
        self.add_button.pack(side=tk.LEFT)

        # List Frame
        list_frame = Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        Label(list_frame, text="Tareas:").pack(anchor=tk.W)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = Listbox(list_frame, selectmode=SINGLE, yscrollcommand=scrollbar.set)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Buttons Frame
        button_frame = Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.done_button = Button(button_frame, text="Marcar como Hecha", command=self._on_mark_done)
        self.done_button.pack(side=tk.LEFT, padx=5)

        self.unmark_button = Button(button_frame, text="Desmarcar Tarea", command=self._on_unmark_done)
        self.unmark_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = Button(button_frame, text="Eliminar Tarea", command=self._on_delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def set_controller(self, controller):
        """Asigna el controlador una vez que esté disponible."""
        self._controller = controller

    def show_tasks(self, tasks: list[Task]):
        """Actualiza el Listbox con las tareas."""
        self.task_listbox.delete(0, END)
        for task in tasks:
            self.task_listbox.insert(END, str(task))

    def show_task_detail(self, task: Task | None):
        """Muestra detalles (usamos messagebox por simplicidad)."""
        if task:
            self.show_message("Detalle Tarea", str(task))

    def get_task_description(self) -> str:
        """Obtiene el texto del campo de entrada."""
        return self.task_entry.get().strip()

    def get_selected_task_id(self) -> int | None:
        """Obtiene el ID de la tarea seleccionada en el Listbox."""
        selected_indices = self.task_listbox.curselection()
        if not selected_indices:
            self.show_message("Error", "Por favor, selecciona una tarea de la lista.")
            return None
        try:
            selected_string = self.task_listbox.get(selected_indices[0])
            id_str = selected_string[selected_string.find("[")+1:selected_string.find("]")]
            return int(id_str)
        except (ValueError, IndexError):
            self.show_message("Error", "No se pudo obtener el ID de la tarea seleccionada.")
            return None

    def show_message(self, title: str, message: str):
        """Muestra un mensaje al usuario."""
        messagebox.showinfo(title, message)

    def clear_task_input(self):
        """Limpia el campo de entrada de nueva tarea."""
        self.task_entry.delete(0, END)

    def start_mainloop(self):
        """Inicia el bucle principal de Tkinter."""
        if self._controller:
             self._controller.load_initial_tasks()
        else:
            print("Error: Controller no asignado a la vista.")
        self.root.mainloop()

    # Callbacks Internos
    def _on_add_task(self):
        if self._controller:
            self._controller.add_task()
        else:
            print("Error: Controller no disponible para añadir tarea.")

    def _on_mark_done(self):
        if self._controller:
            self._controller.mark_task_done()
        else:
             print("Error: Controller no disponible para marcar tarea.")

    def _on_unmark_done(self):
        if self._controller:
            self._controller.unmark_task_done()
        else:
             print("Error: Controller no disponible para desmarcar tarea.")

    def _on_delete_task(self):
        if self._controller:
            if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar la tarea seleccionada?"):
                self._controller.delete_task()
        else:
            print("Error: Controller no disponible para eliminar tarea.")