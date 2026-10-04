class LoginController:
    def __init__(self, modelo_usuario, vista_mensajes):
        self.modelo_usuario = modelo_usuario
        self.vista_mensajes = vista_mensajes
        self.sesion_activa = None 

    def autenticar(self, usuario, password):
        if not usuario.strip() or not password.strip():
            self.vista_mensajes.mostrar_advertencia("Los campos no pueden estar vacíos.")
            return False

        datos_usuario = self.modelo_usuario.verificar_credenciales(usuario, password)
        
        if datos_usuario:
            self.sesion_activa = datos_usuario
            self.vista_mensajes.mostrar_info(f"Acceso concedido. Rol: {datos_usuario['rol']}")
            return True
        else:
            self.vista_mensajes.mostrar_error("Credenciales incorrectas o usuario inactivo.")
            return False

    def cerrar_sesion(self):
        self.sesion_activa = None