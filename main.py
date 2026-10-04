import customtkinter as ctk

from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.clientes_view import ClientesView
from views.productos_view import ProductosView
from views.pedidos_view import PedidosView

from controllers.login_controller import LoginController
from controllers.cliente_controller import ClienteController
from controllers.producto_controller import ProductoController
from controllers.pedido_controller import PedidoController

class AplicacionCriollo:
    def __init__(self, root):
        self.root = root
        self.root.title("El Rincón Criollo - Sistema de Gestión")
        self.root.geometry("1020x680")
        self.root.minsize(960, 600)

        # Configuración estética moderna
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.vista_actual = None
        self.sesion_activa = None

        self.mostrar_login()

    def limpiar_pantalla(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def mostrar_login(self):
        self.limpiar_pantalla()
        self.sesion_activa = None

        # 1. Crear vista de login
        vista_login = LoginView(self.root)
        # 2. Conectar controlador de login con callback de éxito
        ctrl_login = LoginController(vista_login, on_login_success=self.mostrar_dashboard)
        vista_login.controlador = ctrl_login

        vista_login.pack(fill="both", expand=True)
        self.vista_actual = vista_login

    def mostrar_dashboard(self, sesion):
        self.limpiar_pantalla()
        self.sesion_activa = sesion

        # 1. Crear vista principal del Dashboard
        dashboard = DashboardView(self.root, cambiar_vista_callback=self.cambiar_modulo)
        dashboard.actualizar_info_usuario(sesion.get("usuario", "Invitado"), sesion.get("rol", "General"))
        dashboard.pack(fill="both", expand=True)
        self.vista_actual = dashboard

        contenedor = dashboard.obtener_contenedor_contenido()

        # 2. Inicializar las tres vistas hijas dentro del contenedor del dashboard
        self.vistas_modulos = {}
        self.controladores_modulos = {}

        # Módulo Clientes
        vista_cli = ClientesView(contenedor)
        ctrl_cli = ClienteController(vista_cli)
        vista_cli.controlador = ctrl_cli
        self.vistas_modulos["clientes"] = vista_cli
        self.controladores_modulos["clientes"] = ctrl_cli

        # Módulo Productos
        vista_prod = ProductosView(contenedor)
        ctrl_prod = ProductoController(vista_prod)
        vista_prod.controlador = ctrl_prod
        self.vistas_modulos["productos"] = vista_prod
        self.controladores_modulos["productos"] = ctrl_prod

        # Módulo Pedidos y Caja
        vista_ped = PedidosView(contenedor)
        ctrl_ped = PedidoController(vista_ped, sesion_activa=self.sesion_activa)
        vista_ped.controlador = ctrl_ped
        self.vistas_modulos["pedidos"] = vista_ped
        self.controladores_modulos["pedidos"] = ctrl_ped

        # Abrir por defecto la pantalla de Caja / Pedidos
        self.cambiar_modulo("pedidos")

    def cambiar_modulo(self, seccion):
        if seccion == "logout":
            self.mostrar_login()
            return

        # Ocultar todos los submódulos
        for v in self.vistas_modulos.values():
            v.pack_forget()

        # Mostrar el seleccionado y refrescar sus datos desde la BD
        vista_seleccionada = self.vistas_modulos.get(seccion)
        if vista_seleccionada:
            vista_seleccionada.pack(fill="both", expand=True)

            if seccion == "clientes":
                self.controladores_modulos["clientes"].cargar_clientes()
            elif seccion == "productos":
                self.controladores_modulos["productos"].cargar_productos()
            elif seccion == "pedidos":
                self.controladores_modulos["pedidos"].cargar_datos_iniciales()

def main():
    root = ctk.CTk()
    app = AplicacionCriollo(root)
    root.mainloop()

if __name__ == "__main__":
    main()