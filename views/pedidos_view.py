import customtkinter as ctk
from tkinter import messagebox, ttk

class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título de la vista
        self.lbl_titulo = ctk.CTkLabel(self, text="Gestión de Pedidos y Comanda", font=("Helvetica", 22, "bold"))
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Contenedor principal
        self.frame_principal = ctk.CTkFrame(self, corner_radius=15)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=1)

        # Panel superior: Datos del Pedido (Cliente y Mesa)
        self.frame_datos = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_datos.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_cliente = ctk.CTkLabel(self.frame_datos, text="Cliente:", font=("Helvetica", 14))
        self.lbl_cliente.pack(side="left", padx=(0, 10))
        
        self.combo_cliente = ctk.CTkComboBox(self.frame_datos, values=["Seleccione cliente..."], width=200)
        self.combo_cliente.pack(side="left", padx=(0, 20))

        self.lbl_mesa = ctk.CTkLabel(self.frame_datos, text="N° Mesa:", font=("Helvetica", 14))
        self.lbl_mesa.pack(side="left", padx=(0, 10))
        
        self.entry_mesa = ctk.CTkEntry(self.frame_mesa if hasattr(self, 'frame_mesa') else self.frame_datos, placeholder_text="Mesa", width=100)
        self.entry_mesa.pack(side="left")

        # Panel intermedio: Detalle / Carrito de Platos
        self.frame_tabla = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_tabla.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        # Configuración de la tabla (Treeview para el carrito)
        columns = ("id", "producto", "cantidad", "precio", "subtotal", "nota")
        self.tree_carrito = ttk.Treeview(self.frame_tabla, columns=columns, show="headings", height=8)
        
        self.tree_carrito.heading("id", text="ID")
        self.tree_carrito.heading("producto", text="Plato / Producto")
        self.tree_carrito.heading("cantidad", text="Cant.")
        self.tree_carrito.heading("precio", text="P. Unit")
        self.tree_carrito.heading("subtotal", text="Subtotal")
        self.tree_carrito.heading("nota", text="Nota de Cocina")

        self.tree_carrito.column("id", width=40, anchor="center")
        self.tree_carrito.column("producto", width=180, anchor="w")
        self.tree_carrito.column("cantidad", width=60, anchor="center")
        self.tree_carrito.column("precio", width=80, anchor="e")
        self.tree_carrito.column("subtotal", width=80, anchor="e")
        self.tree_carrito.column("nota", width=150, anchor="w")

        self.tree_carrito.grid(row=0, column=0, sticky="nsew")

        # --- PANEL INFERIOR: CAJA SIMPLE Y TOTALES ---
        self.frame_caja_simple = ctk.CTkFrame(self.frame_principal, corner_radius=10, fg_color=("gray85", "gray20"))
        self.frame_caja_simple.grid(row=3, column=0, padx=20, pady=15, sticky="ew")
        self.frame_caja_simple.grid_columnconfigure(1, weight=1)

        self.lbl_total_platos = ctk.CTkLabel(self.frame_caja_simple, text="Total Platos: 0", font=("Helvetica", 14, "bold"))
        self.lbl_total_platos.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.lbl_monto_total = ctk.CTkLabel(self.frame_caja_simple, text="TOTAL A PAGAR: S/. 0.00", font=("Helvetica", 18, "bold"), text_color="#2fa572")
        self.lbl_monto_total.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Botón para generar el ticket de consumo
        self.btn_generar_ticket = ctk.CTkButton(
            self.frame_principal, 
            text="Generar Ticket de Consumo", 
            width=300, 
            height=45, 
            font=("Helvetica", 15, "bold"),
            command=self._clic_generar_ticket
        )
        self.btn_generar_ticket.grid(row=4, column=0, padx=20, pady=(0, 20))

    def _clic_generar_ticket(self):
        if self.controlador and hasattr(self.controlador, "manejar_generar_ticket"):
            self.controlador.manejar_generar_ticket()

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Error en Pedido", mensaje)

    def mostrar_exito(self, mensaje: str):
        messagebox.showinfo("Ticket Generado", mensaje)