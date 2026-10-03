import customtkinter as ctk
from tkinter import ttk, messagebox

class ProductosView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Formulario superior
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.entry_nombre = ctk.CTkEntry(self.frame_form, placeholder_text="Nombre del Plato", width=200)
        self.entry_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.combo_categoria = ctk.CTkComboBox(self.frame_form, values=["Entradas", "Platos de Fondo", "Bebidas", "Postres"])
        self.combo_categoria.grid(row=0, column=1, padx=10, pady=10)

        self.entry_precio = ctk.CTkEntry(self.frame_form, placeholder_text="Precio (S/.)", width=100)
        self.entry_precio.grid(row=0, column=2, padx=10, pady=10)

        self.switch_disponible = ctk.CTkSwitch(self.frame_form, text="Disponible")
        self.switch_disponible.grid(row=0, column=3, padx=10, pady=10)
        self.switch_disponible.select()

        self.btn_guardar_producto = ctk.CTkButton(self.frame_form, text="Registrar Plato", command=self._clic_guardar)
        self.btn_guardar_producto.grid(row=0, column=4, padx=10, pady=10)

        # Tabla / Grilla
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("nombre", "categoria", "precio", "disponible")
        self.tree_productos = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        self.tree_productos.heading("nombre", text="Plato")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio (S/.)")
        self.tree_productos.heading("disponible", text="Disponibilidad")

        self.tree_productos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_productos.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

    def _clic_guardar(self):
        if self.controlador and hasattr(self.controlador, "guardar_producto"):
            self.controlador.guardar_producto()

    def get_datos_producto(self) -> dict:
        return {
            "nombre": self.entry_nombre.get(),
            "categoria": self.combo_categoria.get(),
            "precio": self.entry_precio.get(),
            "disponible": "Disponible" if self.switch_disponible.get() == 1 else "Agotado"
        }

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_precio.delete(0, 'end')
        self.switch_disponible.select()

    def poblar_tabla(self, lista_productos):
        for fila in self.tree_productos.get_children():
            self.tree_productos.delete(fila)
        for prod in lista_productos:
            self.tree_productos.insert("", "end", values=prod)

    def mostrar_error(self, msg):
        messagebox.showerror("Error - Productos", msg)

    def mostrar_exito(self, msg):
        messagebox.showinfo("Éxito - Productos", msg)