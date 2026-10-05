import customtkinter as ctk
from tkinter import ttk, messagebox

class ModalFormularioCliente(ctk.CTkToplevel):
    def __init__(self, parent, on_guardar_callback):
        super().__init__(parent)
        self.title("Registrar Nuevo Cliente")
        self.geometry("450x360")
        self.resizable(False, False)
        self.on_guardar_callback = on_guardar_callback

        # Mantener al frente y modal
        self.transient(parent)
        self.grab_set()

        # Centrar con respecto a la ventana padre
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 225
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 180
        self.geometry(f"+{x}+{y}")

        self.frame_contenido = ctk.CTkFrame(self, corner_radius=15)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_contenido, 
            text="Nuevo Cliente", 
            font=("Helvetica", 18, "bold")
        )
        self.lbl_titulo.pack(pady=(15, 15))

        self.lbl_dni = ctk.CTkLabel(self.frame_contenido, text="DNI (8 dígitos):", font=("Helvetica", 12, "bold"))
        self.lbl_dni.pack(anchor="w", padx=25, pady=(0, 2))
        self.entry_dni = ctk.CTkEntry(self.frame_contenido, placeholder_text="Ej: 72345678", width=340, height=36)
        self.entry_dni.pack(padx=25, pady=(0, 10))

        self.lbl_nombres = ctk.CTkLabel(self.frame_contenido, text="Nombres y Apellidos:", font=("Helvetica", 12, "bold"))
        self.lbl_nombres.pack(anchor="w", padx=25, pady=(0, 2))
        self.entry_nombres = ctk.CTkEntry(self.frame_contenido, placeholder_text="Ej: Carlos Alberto Flores", width=340, height=36)
        self.entry_nombres.pack(padx=25, pady=(0, 10))

        self.lbl_telefono = ctk.CTkLabel(self.frame_contenido, text="Teléfono / Celular:", font=("Helvetica", 12, "bold"))
        self.lbl_telefono.pack(anchor="w", padx=25, pady=(0, 2))
        self.entry_telefono = ctk.CTkEntry(self.frame_contenido, placeholder_text="Ej: 987654321", width=340, height=36)
        self.entry_telefono.pack(padx=25, pady=(0, 15))

        # Botones
        self.frame_botones = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_botones.pack(fill="x", padx=25, pady=(5, 10))

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones, 
            text="Cancelar", 
            fg_color="#6c757d", 
            hover_color="#5a6268", 
            width=140, 
            height=36,
            command=self.destroy
        )
        self.btn_cancelar.pack(side="left")

        self.btn_guardar = ctk.CTkButton(
            self.frame_botones, 
            text="Guardar Cliente", 
            fg_color="#28a745", 
            hover_color="#218838", 
            width=180, 
            height=36,
            command=self._guardar
        )
        self.btn_guardar.pack(side="right")

    def _guardar(self):
        datos = {
            "dni": self.entry_dni.get().strip(),
            "nombres": self.entry_nombres.get().strip(),
            "telefono": self.entry_telefono.get().strip()
        }
        if self.on_guardar_callback:
            self.on_guardar_callback(datos, self)


class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Barra superior con título y botón de acción
        self.frame_superior = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_superior.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_superior, 
            text="Directorio de Clientes", 
            font=("Helvetica", 22, "bold")
        )
        self.lbl_titulo.pack(side="left")

        self.lbl_total = ctk.CTkLabel(
            self.frame_superior, 
            text="Total: 0 clientes", 
            font=("Helvetica", 14), 
            text_color="gray"
        )
        self.lbl_total.pack(side="left", padx=20)

        self.btn_nuevo = ctk.CTkButton(
            self.frame_superior, 
            text="+ Registrar Nuevo Cliente", 
            font=("Helvetica", 13, "bold"),
            fg_color="#007bff", 
            hover_color="#0069d9", 
            height=38,
            command=self._clic_nuevo
        )
        self.btn_nuevo.pack(side="right")

        # Tabla amplia para visualizar clientes
        self.frame_tabla = ctk.CTkFrame(self, corner_radius=12)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("id", "dni", "nombres", "telefono")
        self.tree_clientes = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("dni", text="DNI")
        self.tree_clientes.heading("nombres", text="Nombres y Apellidos")
        self.tree_clientes.heading("telefono", text="Teléfono / Celular")

        self.tree_clientes.column("id", width=50, anchor="center")
        self.tree_clientes.column("dni", width=120, anchor="center")
        self.tree_clientes.column("nombres", width=380, anchor="w")
        self.tree_clientes.column("telefono", width=160, anchor="center")

        self.tree_clientes.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_clientes.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

    def _clic_nuevo(self):
        if self.controlador and hasattr(self.controlador, "abrir_modal_nuevo"):
            self.controlador.abrir_modal_nuevo()

    def abrir_modal_registro(self, on_guardar_cb):
        return ModalFormularioCliente(self, on_guardar_cb)

    def poblar_tabla(self, lista_clientes):
        for fila in self.tree_clientes.get_children():
            self.tree_clientes.delete(fila)
        for c in lista_clientes:
            self.tree_clientes.insert("", "end", values=c)
        self.lbl_total.configure(text=f"Total: {len(lista_clientes)} clientes")

    def mostrar_error(self, msg):
        messagebox.showerror("Error - Clientes", msg)

    def mostrar_exito(self, msg):
        messagebox.showinfo("Éxito - Clientes", msg)