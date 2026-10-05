import customtkinter as ctk
from tkinter import ttk, messagebox

class ModalFormularioProducto(ctk.CTkToplevel):
    def __init__(self, parent, on_guardar_callback, producto=None):
        super().__init__(parent)
        self.producto = producto
        es_edicion = producto is not None

        self.title("Editar Plato Criollo" if es_edicion else "Registrar Nuevo Plato Criollo")
        self.geometry("490x460")
        self.resizable(False, False)
        self.on_guardar_callback = on_guardar_callback

        # Modal centrado
        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 245
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 230
        self.geometry(f"+{x}+{y}")

        self.frame_contenido = ctk.CTkFrame(self, corner_radius=15)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_contenido, 
            text=f"Editar Plato #{producto['id']}" if es_edicion else "Nuevo Plato / Bebida", 
            font=("Helvetica", 20, "bold")
        )
        self.lbl_titulo.pack(pady=(15, 15))

        self.lbl_nombre = ctk.CTkLabel(self.frame_contenido, text="Nombre del Plato:", font=("Helvetica", 13, "bold"))
        self.lbl_nombre.pack(anchor="w", padx=25, pady=(0, 3))
        self.entry_nombre = ctk.CTkEntry(self.frame_contenido, placeholder_text="Ej: Seco de Res con Frijoles", width=380, height=38, font=("Helvetica", 13))
        self.entry_nombre.pack(padx=25, pady=(0, 10))
        if es_edicion:
            self.entry_nombre.insert(0, producto.get("nombre", ""))

        self.lbl_cat = ctk.CTkLabel(self.frame_contenido, text="Categoría:", font=("Helvetica", 13, "bold"))
        self.lbl_cat.pack(anchor="w", padx=25, pady=(0, 3))
        self.combo_categoria = ctk.CTkComboBox(
            self.frame_contenido, 
            values=["Entradas", "Platos de Fondo", "Guarniciones", "Bebidas", "Postres"], 
            width=380, 
            height=38,
            font=("Helvetica", 13)
        )
        self.combo_categoria.pack(padx=25, pady=(0, 10))
        if es_edicion and producto.get("categoria"):
            self.combo_categoria.set(producto["categoria"])

        self.lbl_precio = ctk.CTkLabel(self.frame_contenido, text="Precio de Venta (S/.):", font=("Helvetica", 13, "bold"))
        self.lbl_precio.pack(anchor="w", padx=25, pady=(0, 3))
        self.entry_precio = ctk.CTkEntry(self.frame_contenido, placeholder_text="Ej: 32.00", width=380, height=38, font=("Helvetica", 13))
        self.entry_precio.pack(padx=25, pady=(0, 14))
        if es_edicion:
            self.entry_precio.insert(0, str(producto.get("precio", "")))

        self.switch_disponible = ctk.CTkSwitch(self.frame_contenido, text="Disponible para venta en comanda / caja", font=("Helvetica", 13))
        self.switch_disponible.pack(anchor="w", padx=25, pady=(0, 20))
        if es_edicion:
            if producto.get("disponible", True):
                self.switch_disponible.select()
            else:
                self.switch_disponible.deselect()
        else:
            self.switch_disponible.select()

        # Botones de Acción (Grandes, Visibles y Ergonómicos)
        self.frame_botones = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_botones.pack(fill="x", padx=25, pady=(0, 10))

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones, 
            text="Cancelar", 
            fg_color="#6c757d", 
            hover_color="#5a6268", 
            width=160, 
            height=44,
            font=("Helvetica", 14, "bold"),
            command=self.destroy
        )
        self.btn_cancelar.pack(side="left")

        self.btn_guardar = ctk.CTkButton(
            self.frame_botones, 
            text="Actualizar Plato" if es_edicion else "Guardar Plato", 
            fg_color="#007bff" if es_edicion else "#28a745", 
            hover_color="#0069d9" if es_edicion else "#218838", 
            width=200, 
            height=44,
            font=("Helvetica", 14, "bold"),
            command=self._guardar
        )
        self.btn_guardar.pack(side="right")

    def _guardar(self):
        datos = {
            "nombre": self.entry_nombre.get().strip(),
            "categoria": self.combo_categoria.get().strip(),
            "precio": self.entry_precio.get().strip(),
            "disponible": self.switch_disponible.get() == 1
        }
        if self.producto:
            datos["id"] = self.producto["id"]
        if self.on_guardar_callback:
            self.on_guardar_callback(datos, self)


class ProductosView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Barra superior con título y botones de acción del CRUD
        self.frame_superior = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_superior.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_superior, 
            text="Carta de Platos Criollos", 
            font=("Helvetica", 22, "bold")
        )
        self.lbl_titulo.pack(side="left")

        self.lbl_total = ctk.CTkLabel(
            self.frame_superior, 
            text="Total: 0 platos", 
            font=("Helvetica", 14), 
            text_color="gray"
        )
        self.lbl_total.pack(side="left", padx=15)

        # Botones de Acciones CRUD
        self.btn_eliminar = ctk.CTkButton(
            self.frame_superior, 
            text="🗑️ Eliminar", 
            font=("Helvetica", 13, "bold"),
            fg_color="#dc3545", 
            hover_color="#c82333", 
            height=38,
            width=100,
            command=self._clic_eliminar
        )
        self.btn_eliminar.pack(side="right", padx=(6, 0))

        self.btn_disponibilidad = ctk.CTkButton(
            self.frame_superior, 
            text="🔄 Disponibilidad", 
            font=("Helvetica", 13, "bold"),
            fg_color="#ffc107", 
            text_color="black",
            hover_color="#e0a800", 
            height=38,
            width=135,
            command=self._clic_disponibilidad
        )
        self.btn_disponibilidad.pack(side="right", padx=(6, 0))

        self.btn_editar = ctk.CTkButton(
            self.frame_superior, 
            text="✏️ Editar Plato", 
            font=("Helvetica", 13, "bold"),
            fg_color="#17a2b8", 
            hover_color="#138496", 
            height=38,
            width=120,
            command=self._clic_editar
        )
        self.btn_editar.pack(side="right", padx=(6, 0))

        self.btn_nuevo = ctk.CTkButton(
            self.frame_superior, 
            text="+ Nuevo Plato", 
            font=("Helvetica", 13, "bold"),
            fg_color="#28a745", 
            hover_color="#218838", 
            height=38,
            width=130,
            command=self._clic_nuevo
        )
        self.btn_nuevo.pack(side="right")

        # Tabla amplia para visualizar el catálogo
        self.frame_tabla = ctk.CTkFrame(self, corner_radius=12)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("id", "nombre", "categoria", "precio", "disponible")
        self.tree_productos = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        self.tree_productos.heading("id", text="ID")
        self.tree_productos.heading("nombre", text="Plato Criollo")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio (S/.)")
        self.tree_productos.heading("disponible", text="Disponibilidad")

        self.tree_productos.column("id", width=50, anchor="center")
        self.tree_productos.column("nombre", width=320, anchor="w")
        self.tree_productos.column("categoria", width=180, anchor="center")
        self.tree_productos.column("precio", width=120, anchor="e")
        self.tree_productos.column("disponible", width=130, anchor="center")

        self.tree_productos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_productos.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

    def _clic_nuevo(self):
        if self.controlador and hasattr(self.controlador, "abrir_modal_nuevo"):
            self.controlador.abrir_modal_nuevo()

    def _clic_editar(self):
        if self.controlador and hasattr(self.controlador, "abrir_modal_editar"):
            self.controlador.abrir_modal_editar()

    def _clic_disponibilidad(self):
        if self.controlador and hasattr(self.controlador, "conmutar_disponibilidad"):
            self.controlador.conmutar_disponibilidad()

    def _clic_eliminar(self):
        if self.controlador and hasattr(self.controlador, "eliminar_producto_seleccionado"):
            self.controlador.eliminar_producto_seleccionado()

    def get_producto_seleccionado(self):
        seleccion = self.tree_productos.selection()
        if seleccion:
            return self.tree_productos.item(seleccion[0])["values"]
        return None

    def abrir_modal_registro(self, on_guardar_cb):
        return ModalFormularioProducto(self, on_guardar_cb)

    def abrir_modal_edicion(self, producto_datos, on_guardar_cb):
        return ModalFormularioProducto(self, on_guardar_cb, producto=producto_datos)

    def poblar_tabla(self, lista_productos):
        for fila in self.tree_productos.get_children():
            self.tree_productos.delete(fila)
        for prod in lista_productos:
            self.tree_productos.insert("", "end", values=prod)
        self.lbl_total.configure(text=f"Total: {len(lista_productos)} platos")

    def mostrar_error(self, msg):
        messagebox.showerror("Error - Productos", msg)

    def mostrar_exito(self, msg):
        messagebox.showinfo("Éxito - Productos", msg)

    def confirmar_accion(self, titulo, mensaje) -> bool:
        return messagebox.askyesno(titulo, mensaje)