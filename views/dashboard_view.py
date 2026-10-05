import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, cambiar_vista_callback=None):
        super().__init__(parent)
        self.cambiar_vista_callback = cambiar_vista_callback

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Encabezado superior (Muestra usuario y rol activo)
        self.frame_header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.lbl_sistema = ctk.CTkLabel(
            self.frame_header, 
            text="Sistema de Restaurante - El Rincón Criollo", 
            font=("Helvetica", 15, "bold")
        )
        self.lbl_sistema.pack(side="left", padx=20, pady=15)

        self.lbl_usuario_rol = ctk.CTkLabel(
            self.frame_header, 
            text="Usuario: [Invitado] | Rol: [Sin Asignar]", 
            font=("Helvetica", 13, "bold"),
            text_color="#17a2b8"
        )
        self.lbl_usuario_rol.pack(side="right", padx=20, pady=15)

        # Menú Lateral (Sidebar)
        self.frame_sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.frame_sidebar.grid(row=1, column=0, sticky="nsew")
        
        self.lbl_menu = ctk.CTkLabel(self.frame_sidebar, text="MENÚ PRINCIPAL", font=("Helvetica", 13, "bold"), text_color="gray")
        self.lbl_menu.pack(padx=20, pady=(20, 10), anchor="w")

        self.btn_pedidos = ctk.CTkButton(
            self.frame_sidebar, 
            text="🛒 Caja (Nuevo Pedido)", 
            font=("Helvetica", 13, "bold"),
            height=38,
            command=lambda: self._navegar("pedidos")
        )
        self.btn_pedidos.pack(padx=15, pady=6, fill="x")

        self.btn_historial = ctk.CTkButton(
            self.frame_sidebar, 
            text="📋 Historial de Ventas", 
            font=("Helvetica", 13, "bold"),
            height=38,
            command=lambda: self._navegar("historial")
        )
        self.btn_historial.pack(padx=15, pady=6, fill="x")

        self.btn_clientes = ctk.CTkButton(
            self.frame_sidebar, 
            text="👥 Directorio de Clientes", 
            font=("Helvetica", 13),
            height=38,
            command=lambda: self._navegar("clientes")
        )
        self.btn_clientes.pack(padx=15, pady=6, fill="x")

        self.btn_productos = ctk.CTkButton(
            self.frame_sidebar, 
            text="🍽️ Carta de Productos", 
            font=("Helvetica", 13),
            height=38,
            command=lambda: self._navegar("productos")
        )
        self.btn_productos.pack(padx=15, pady=6, fill="x")

        self.btn_logout = ctk.CTkButton(
            self.frame_sidebar, 
            text="🚪 Cerrar Sesión", 
            font=("Helvetica", 13),
            fg_color="#d9534f", 
            hover_color="#c9302c", 
            height=36,
            command=lambda: self._navegar("logout")
        )
        self.btn_logout.pack(padx=15, pady=(35, 15), fill="x")

        # Contenedor dinámico principal
        self.frame_contenido = ctk.CTkFrame(self, corner_radius=0)
        self.frame_contenido.grid(row=1, column=1, sticky="nsew")
        self.frame_contenido.grid_columnconfigure(0, weight=1)
        self.frame_contenido.grid_rowconfigure(0, weight=1)

    def _navegar(self, seccion: str):
        if self.cambiar_vista_callback:
            self.cambiar_vista_callback(seccion)

    def actualizar_info_usuario(self, usuario: str, rol: str):
        self.lbl_usuario_rol.configure(text=f"Usuario: {usuario}  |  Rol: {rol.upper()}")

    def obtener_contenedor_contenido(self):
        return self.frame_contenido