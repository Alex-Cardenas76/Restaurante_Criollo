import customtkinter as ctk
from tkinter import ttk, messagebox

class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Formulario superior
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.entry_dni = ctk.CTkEntry(self.frame_form, placeholder_text="DNI", width=120)
        self.entry_dni.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nombres = ctk.CTkEntry(self.frame_form, placeholder_text="Nombres y Apellidos", width=250)
        self.entry_nombres.grid(row=0, column=1, padx=10, pady=10)

        self.entry_telefono = ctk.CTkEntry(self.frame_form, placeholder_text="Teléfono", width=150)
        self.entry_telefono.grid(row=0, column=2, padx=10, pady=10)

        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Guardar Cliente", command=self._clic_guardar)
        self.btn_guardar.grid(row=0, column=3, padx=10, pady=10)

        # Tabla inferior con Treeview y scrollbar
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("dni", "nombres", "telefono")
        self.tree_clientes = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        self.tree_clientes.heading("dni", text="DNI")
        self.tree_clientes.heading("nombres", text="Nombres y Apellidos")
        self.tree_clientes.heading("telefono", text="Teléfono")
        
        self.tree_clientes.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_clientes.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

    def _clic_guardar(self):
        if self.controlador and hasattr(self.controlador, "guardar_cliente"):
            self.controlador.guardar_cliente()

    def get_datos_formulario(self) -> dict:
        return {
            "dni": self.entry_dni.get(),
            "nombres": self.entry_nombres.get(),
            "telefono": self.entry_telefono.get()
        }

    def limpiar_formulario(self):
        self.entry_dni.delete(0, 'end')
        self.entry_nombres.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')

    def poblar_tabla(self, lista_clientes):
        for fila in self.tree_clientes.get_children():
            self.tree_clientes.delete(fila)
        for cliente in lista_clientes:
            self.tree_clientes.insert("", "end", values=cliente)

    def mostrar_error(self, msg):
        messagebox.showerror("Error - Clientes", msg)

    def mostrar_exito(self, msg):
        messagebox.showinfo("Éxito - Clientes", msg)