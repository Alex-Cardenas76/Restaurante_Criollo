from models import usuario_model

class LoginController:
    def __init__(self, vista, on_login_success=None):
        self.vista = vista
        self.on_login_success = on_login_success
        self.sesion_activa = None

    def manejar_login(self):
        usuario = self.vista.get_usuario()
        password = self.vista.get_password()

        if not usuario or not password:
            self.vista.mostrar_error("Los campos de usuario y contraseña no pueden estar vacíos.")
            return

        try:
            datos_usuario = usuario_model.obtener_usuario_por_nombre(usuario)
        except Exception as error:
            self.vista.mostrar_error(f"Error de conexión con la base de datos: {error}")
            return

        if not datos_usuario:
            self.vista.mostrar_error("Usuario o contraseña incorrectos.")
            return

        id_u, nombre, contrasena_bd, rol = datos_usuario

        if contrasena_bd != password:
            self.vista.mostrar_error("Usuario o contraseña incorrectos.")
            return

        self.sesion_activa = {
            "id_usuario": id_u,
            "usuario": nombre,
            "rol": rol
        }

        self.vista.limpiar()
        if self.on_login_success:
            self.on_login_success(self.sesion_activa)

    def cerrar_sesion(self):
        self.sesion_activa = None