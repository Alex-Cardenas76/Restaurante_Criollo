import customtkinter as ctk
from tkinter import ttk, messagebox

class ModalDetalleComanda(ctk.CTkToplevel):
    def __init__(self, parent, info_pedido, items_detalle):
        super().__init__(parent)
        self.title(f"Detalle de Comanda N° {info_pedido.get('id', '')}")
        self.geometry("680x480")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 340
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 240
        self.geometry(f"+{x}+{y}")

        self.frame_contenido = ctk.CTkFrame(self, corner_radius=15)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        # Encabezado del ticket
        self.lbl_titulo = ctk.CTkLabel(
            self.frame_contenido, 
            text=f"Comprobante de Venta N° {info_pedido.get('id', '')}", 
            font=("Helvetica", 18, "bold")
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # Tarjeta de metadatos
        self.frame_meta = ctk.CTkFrame(self.frame_contenido, fg_color=("gray90", "gray25"), corner_radius=10)
        self.frame_meta.pack(fill="x", padx=15, pady=(0, 10))

        lbl_txt_1 = f"Mesa: {info_pedido.get('mesa', '-')}  |  Cliente: {info_pedido.get('cliente', '-')}  |  Pago: {info_pedido.get('metodo_pago', '-')}"
        lbl_txt_2 = f"Cajero: {info_pedido.get('usuario', '-')}  |  Fecha: {info_pedido.get('fecha', '-')}  |  Estado: {info_pedido.get('estado', '-')}"

        self.lbl_info1 = ctk.CTkLabel(self.frame_meta, text=lbl_txt_1, font=("Helvetica", 12))
        self.lbl_info1.pack(pady=(6, 2))

        self.lbl_info2 = ctk.CTkLabel(self.frame_meta, text=lbl_txt_2, font=("Helvetica", 12))
        self.lbl_info2.pack(pady=(0, 6))

        # Tabla de platos consumidos
        self.frame_tabla = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        columnas = ("producto", "cantidad", "precio_unitario", "subtotal", "nota")
        self.tree_detalle = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=7)
        self.tree_detalle.heading("producto", text="Plato Criollo")
        self.tree_detalle.heading("cantidad", text="Cant.")
        self.tree_detalle.heading("precio_unitario", text="P. Unit (S/.)")
        self.tree_detalle.heading("subtotal", text="Subtotal (S/.)")
        self.tree_detalle.heading("nota", text="Nota de Cocina")

        self.tree_detalle.column("producto", width=200, anchor="w")
        self.tree_detalle.column("cantidad", width=50, anchor="center")
        self.tree_detalle.column("precio_unitario", width=90, anchor="e")
        self.tree_detalle.column("subtotal", width=90, anchor="e")
        self.tree_detalle.column("nota", width=180, anchor="w")

        self.tree_detalle.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_detalle.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_detalle.configure(yscrollcommand=scrollbar.set)

        # Llenar la tabla de detalles
        for item in items_detalle:
            # item = (dp.id, dp.producto_id, p.nombre, dp.cantidad, dp.precio_unitario, dp.subtotal, dp.nota_plato)
            self.tree_detalle.insert("", "end", values=(
                item[2],
                item[3],
                f"{float(item[4]):.2f}",
                f"{float(item[5]):.2f}",
                item[6] or "-"
            ))

        # Total inferior
        self.frame_total = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self.frame_total.pack(fill="x", padx=15, pady=(10, 5))

        self.lbl_total = ctk.CTkLabel(
            self.frame_total, 
            text=f"TOTAL LIQUIDADO: S/. {float(info_pedido.get('total', 0.0)):.2f}", 
            font=("Helvetica", 16, "bold"), 
            text_color="#2fa572"
        )
        self.lbl_total.pack(side="left")

        self.btn_cerrar = ctk.CTkButton(
            self.frame_total, 
            text="Cerrar", 
            width=120, 
            command=self.destroy
        )
        self.btn_cerrar.pack(side="right")


class HistorialPedidosView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Barra superior con título y botones de acción
        self.frame_superior = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_superior.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_superior, 
            text="Historial de Ventas y Comandas", 
            font=("Helvetica", 22, "bold")
        )
        self.lbl_titulo.pack(side="left")

        self.lbl_recaudado = ctk.CTkLabel(
            self.frame_superior, 
            text="Total Recaudado: S/. 0.00", 
            font=("Helvetica", 15, "bold"), 
            text_color="#2fa572"
        )
        self.lbl_recaudado.pack(side="left", padx=25)

        self.btn_ver_detalle = ctk.CTkButton(
            self.frame_superior, 
            text="👁️ Ver Detalle de Comanda", 
            font=("Helvetica", 13, "bold"), 
            fg_color="#17a2b8", 
            hover_color="#138496",
            height=38,
            command=self._clic_ver_detalle
        )
        self.btn_ver_detalle.pack(side="right", padx=(10, 0))

        self.btn_refrescar = ctk.CTkButton(
            self.frame_superior, 
            text="🔄 Refrescar", 
            font=("Helvetica", 13), 
            fg_color="#6c757d", 
            hover_color="#5a6268", 
            width=100, 
            height=38,
            command=self._clic_refrescar
        )
        self.btn_refrescar.pack(side="right")

        # Tabla del historial
        self.frame_tabla = ctk.CTkFrame(self, corner_radius=12)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("id", "fecha", "mesa", "cliente", "usuario", "metodo_pago", "total", "estado")
        self.tree_historial = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        self.tree_historial.heading("id", text="N° Ticket")
        self.tree_historial.heading("fecha", text="Fecha y Hora")
        self.tree_historial.heading("mesa", text="Mesa / Ubicación")
        self.tree_historial.heading("cliente", text="Cliente")
        self.tree_historial.heading("usuario", text="Cajero / Usuario")
        self.tree_historial.heading("metodo_pago", text="Método Pago")
        self.tree_historial.heading("total", text="Total (S/.)")
        self.tree_historial.heading("estado", text="Estado")

        self.tree_historial.column("id", width=60, anchor="center")
        self.tree_historial.column("fecha", width=150, anchor="center")
        self.tree_historial.column("mesa", width=110, anchor="center")
        self.tree_historial.column("cliente", width=180, anchor="w")
        self.tree_historial.column("usuario", width=120, anchor="center")
        self.tree_historial.column("metodo_pago", width=100, anchor="center")
        self.tree_historial.column("total", width=110, anchor="e")
        self.tree_historial.column("estado", width=90, anchor="center")

        self.tree_historial.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_historial.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.tree_historial.configure(yscrollcommand=scrollbar.set)

    def _clic_refrescar(self):
        if self.controlador and hasattr(self.controlador, "cargar_historial"):
            self.controlador.cargar_historial()

    def _clic_ver_detalle(self):
        seleccion = self.tree_historial.selection()
        if not seleccion:
            self.mostrar_error("Por favor, seleccione un pedido de la tabla para ver su detalle.")
            return

        valores = self.tree_historial.item(seleccion[0])["values"]
        # valores = [id, fecha, mesa, cliente, usuario, metodo_pago, total, estado]
        info_pedido = {
            "id": valores[0],
            "fecha": valores[1],
            "mesa": valores[2],
            "cliente": valores[3],
            "usuario": valores[4],
            "metodo_pago": valores[5],
            "total": valores[6],
            "estado": valores[7]
        }
        if self.controlador and hasattr(self.controlador, "abrir_detalle_pedido"):
            self.controlador.abrir_detalle_pedido(info_pedido)

    def abrir_modal_detalle(self, info_pedido, items_detalle):
        return ModalDetalleComanda(self, info_pedido, items_detalle)

    def poblar_tabla(self, lista_pedidos):
        for fila in self.tree_historial.get_children():
            self.tree_historial.delete(fila)

        total_acumulado = 0.0
        for p in lista_pedidos:
            # p = (id, cliente, usuario, mesa, metodo_pago, total, estado, fecha)
            monto = float(p[5]) if p[5] else 0.0
            total_acumulado += monto
            self.tree_historial.insert("", "end", values=(
                p[0],
                str(p[7])[:19] if p[7] else "-",
                p[3],
                p[1] or "Público General",
                p[2] or "Sistema",
                p[4],
                f"{monto:.2f}",
                p[6]
            ))
        self.lbl_recaudado.configure(text=f"Total Recaudado: S/. {total_acumulado:.2f}")

    def mostrar_error(self, msg):
        messagebox.showerror("Historial de Pedidos", msg)

    def mostrar_exito(self, msg):
        messagebox.showinfo("Historial de Pedidos", msg)
