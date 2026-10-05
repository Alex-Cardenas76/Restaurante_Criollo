import customtkinter as ctk
from tkinter import messagebox, ttk

class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título de la vista
        self.lbl_titulo = ctk.CTkLabel(self, text="Punto de Venta y Toma de Comanda", font=("Helvetica", 22, "bold"))
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        # Contenedor principal
        self.frame_principal = ctk.CTkFrame(self, corner_radius=15)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=1)

        # -------------------------------------------------------------
        # PANEL 0: DATOS GENERALES (Cliente, Mesa, Método de Pago)
        # -------------------------------------------------------------
        self.frame_datos = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_datos.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.lbl_cliente = ctk.CTkLabel(self.frame_datos, text="Cliente:", font=("Helvetica", 13, "bold"))
        self.lbl_cliente.pack(side="left", padx=(0, 6))

        self.combo_cliente = ctk.CTkComboBox(self.frame_datos, values=["Público General"], width=220)
        self.combo_cliente.pack(side="left", padx=(0, 15))

        self.lbl_mesa = ctk.CTkLabel(self.frame_datos, text="Mesa / Ubicación:", font=("Helvetica", 13, "bold"))
        self.lbl_mesa.pack(side="left", padx=(0, 6))

        self.combo_mesa = ctk.CTkComboBox(
            self.frame_datos, 
            values=["Mesa 01", "Mesa 02", "Mesa 03", "Mesa 04", "Mesa 05", "Mesa 06", "Para Llevar"], 
            width=210
        )
        self.combo_mesa.pack(side="left", padx=(0, 15))

        self.lbl_pago = ctk.CTkLabel(self.frame_datos, text="Método Pago:", font=("Helvetica", 13, "bold"))
        self.lbl_pago.pack(side="left", padx=(0, 6))

        self.combo_metodo_pago = ctk.CTkComboBox(self.frame_datos, values=["Efectivo", "Yape", "Plin", "Tarjeta"], width=130)
        self.combo_metodo_pago.pack(side="left")

        # -------------------------------------------------------------
        # PANEL 1: SELECCIÓN DE PLATOS (Agregar al carrito en RAM)
        # -------------------------------------------------------------
        self.frame_seleccion = ctk.CTkFrame(self.frame_principal, fg_color=("gray90", "gray25"), corner_radius=10)
        self.frame_seleccion.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.lbl_plato = ctk.CTkLabel(self.frame_seleccion, text="Plato:", font=("Helvetica", 13, "bold"))
        self.lbl_plato.pack(side="left", padx=(15, 6), pady=10)

        self.combo_plato = ctk.CTkComboBox(self.frame_seleccion, values=["Seleccione plato..."], width=230)
        self.combo_plato.pack(side="left", padx=(0, 10), pady=10)

        self.lbl_cant = ctk.CTkLabel(self.frame_seleccion, text="Cant:", font=("Helvetica", 13, "bold"))
        self.lbl_cant.pack(side="left", padx=(0, 6), pady=10)

        self.entry_cantidad = ctk.CTkEntry(self.frame_seleccion, width=50)
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.pack(side="left", padx=(0, 10), pady=10)

        self.entry_nota = ctk.CTkEntry(self.frame_seleccion, placeholder_text="Nota cocina (ej: sin picante)", width=200)
        self.entry_nota.pack(side="left", padx=(0, 10), pady=10)

        self.btn_agregar = ctk.CTkButton(
            self.frame_seleccion, 
            text="+ Agregar", 
            width=90, 
            fg_color="#28a745", 
            hover_color="#218838",
            command=self._clic_agregar
        )
        self.btn_agregar.pack(side="left", padx=(0, 8), pady=10)

        self.btn_quitar = ctk.CTkButton(
            self.frame_seleccion, 
            text="- Quitar", 
            width=80, 
            fg_color="#dc3545", 
            hover_color="#c82333",
            command=self._clic_quitar
        )
        self.btn_quitar.pack(side="left", padx=(0, 15), pady=10)

        # -------------------------------------------------------------
        # PANEL 2: TABLA DEL CARRITO EN RAM
        # -------------------------------------------------------------
        self.frame_tabla = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columns = ("id", "producto", "cantidad", "precio", "subtotal", "nota")
        self.tree_carrito = ttk.Treeview(self.frame_tabla, columns=columns, show="headings", height=8)

        self.tree_carrito.heading("id", text="ID")
        self.tree_carrito.heading("producto", text="Plato / Producto")
        self.tree_carrito.heading("cantidad", text="Cant.")
        self.tree_carrito.heading("precio", text="P. Unit (S/.)")
        self.tree_carrito.heading("subtotal", text="Subtotal (S/.)")
        self.tree_carrito.heading("nota", text="Nota de Cocina")

        self.tree_carrito.column("id", width=40, anchor="center")
        self.tree_carrito.column("producto", width=220, anchor="w")
        self.tree_carrito.column("cantidad", width=60, anchor="center")
        self.tree_carrito.column("precio", width=90, anchor="e")
        self.tree_carrito.column("subtotal", width=90, anchor="e")
        self.tree_carrito.column("nota", width=180, anchor="w")

        self.tree_carrito.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_carrito.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_carrito.configure(yscrollcommand=scrollbar.set)

        # -------------------------------------------------------------
        # PANEL 3: TOTALES
        # -------------------------------------------------------------
        self.frame_caja_simple = ctk.CTkFrame(self.frame_principal, corner_radius=10, fg_color=("gray85", "gray20"))
        self.frame_caja_simple.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.frame_caja_simple.grid_columnconfigure(1, weight=1)

        self.lbl_total_platos = ctk.CTkLabel(self.frame_caja_simple, text="Total Platos: 0", font=("Helvetica", 14, "bold"))
        self.lbl_total_platos.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        self.lbl_monto_total = ctk.CTkLabel(self.frame_caja_simple, text="TOTAL A PAGAR: S/. 0.00", font=("Helvetica", 18, "bold"), text_color="#2fa572")
        self.lbl_monto_total.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        # -------------------------------------------------------------
        # PANEL 4: ACCIONES DUALES (GUARDAR COMANDA vs COBRAR)
        # -------------------------------------------------------------
        self.frame_acciones = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_acciones.grid(row=4, column=0, padx=20, pady=(0, 15))

        self.btn_guardar_comanda = ctk.CTkButton(
            self.frame_acciones, 
            text="📝 Guardar Comanda (Pendiente)", 
            width=270, 
            height=42, 
            font=("Helvetica", 14, "bold"),
            fg_color="#f0ad4e",
            text_color="black",
            hover_color="#ec971f",
            command=self._clic_guardar_pendiente
        )
        self.btn_guardar_comanda.pack(side="left", padx=(0, 15))

        self.btn_cobrar_instante = ctk.CTkButton(
            self.frame_acciones, 
            text="💳 Cobrar al Instante (Pagado)", 
            width=270, 
            height=42, 
            font=("Helvetica", 14, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            command=self._clic_cobrar_instante
        )
        self.btn_cobrar_instante.pack(side="left")

    # Eventos de botones
    def _clic_agregar(self):
        if self.controlador and hasattr(self.controlador, "agregar_plato_carrito"):
            self.controlador.agregar_plato_carrito()

    def _clic_quitar(self):
        if self.controlador and hasattr(self.controlador, "quitar_plato_carrito"):
            self.controlador.quitar_plato_carrito()

    def _clic_guardar_pendiente(self):
        if self.controlador and hasattr(self.controlador, "procesar_pedido"):
            self.controlador.procesar_pedido(estado_deseado="Pendiente")

    def _clic_cobrar_instante(self):
        if self.controlador and hasattr(self.controlador, "procesar_pedido"):
            self.controlador.procesar_pedido(estado_deseado="Pagado")

    # Métodos accesibles por el Controlador
    def get_cliente_seleccionado(self) -> str:
        return self.combo_cliente.get()

    def get_mesa(self) -> str:
        return self.combo_mesa.get().strip()

    def get_metodo_pago(self) -> str:
        return self.combo_metodo_pago.get()

    def get_plato_seleccionado(self) -> str:
        return self.combo_plato.get()

    def get_cantidad(self) -> str:
        return self.entry_cantidad.get().strip()

    def get_nota(self) -> str:
        return self.entry_nota.get().strip()

    def get_item_carrito_seleccionado(self):
        seleccion = self.tree_carrito.selection()
        if seleccion:
            item = self.tree_carrito.item(seleccion[0])
            return item["values"]
        return None

    def poblar_clientes(self, lista_clientes):
        valores = [f"{c[1]} (DNI: {c[2]})" for c in lista_clientes]
        if not valores:
            valores = ["Público General"]
        self.combo_cliente.configure(values=valores)
        self.combo_cliente.set(valores[0])

    def poblar_platos(self, lista_platos):
        valores = [f"{p[0]} - {p[1]} (S/. {float(p[3]):.2f})" for p in lista_platos]
        if not valores:
            valores = ["Sin platos disponibles"]
        self.combo_plato.configure(values=valores)
        self.combo_plato.set(valores[0])

    def poblar_mesas(self, lista_mesas):
        self.combo_mesa.configure(values=lista_mesas)
        if lista_mesas:
            self.combo_mesa.set(lista_mesas[0])

    def poblar_carrito(self, items_carrito, monto_total, total_cant):
        for fila in self.tree_carrito.get_children():
            self.tree_carrito.delete(fila)
        for item in items_carrito:
            self.tree_carrito.insert("", "end", values=(
                item["id_producto"],
                item["nombre"],
                item["cantidad"],
                f"{item['precio_unitario']:.2f}",
                f"{item['subtotal']:.2f}",
                item.get("nota_plato", "")
            ))
        self.lbl_total_platos.configure(text=f"Total Platos: {total_cant}")
        self.lbl_monto_total.configure(text=f"TOTAL A PAGAR: S/. {monto_total:.2f}")

    def limpiar_formulario(self):
        self.entry_nota.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')
        self.entry_cantidad.insert(0, "1")
        for fila in self.tree_carrito.get_children():
            self.tree_carrito.delete(fila)
        self.lbl_total_platos.configure(text="Total Platos: 0")
        self.lbl_monto_total.configure(text="TOTAL A PAGAR: S/. 0.00")

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Gestión de Pedido", mensaje)

    def mostrar_exito(self, mensaje: str):
        messagebox.showinfo("Gestión de Pedido", mensaje)