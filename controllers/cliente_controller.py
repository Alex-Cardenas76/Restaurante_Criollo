import re

class ClienteController:
    def __init__(self, modelo_cliente, vista_mensajes):
        self.modelo_cliente = modelo_cliente
        self.vista_mensajes = vista_mensajes

    def registrar_cliente(self, dni, nombres, telefono):
        if not re.fullmatch(r'\d{8}', dni):
            self.vista_mensajes.mostrar_error("El DNI debe tener exactamente 8 números.")
            return False

        if not re.fullmatch(r'[A-Za-zÁ-Úá-úÑñ\s]+', nombres):
            self.vista_mensajes.mostrar_error("El nombre contiene caracteres inválidos.")
            return False

        if telefono and not re.fullmatch(r'9\d{8}', telefono):
            self.vista_mensajes.mostrar_error("El teléfono debe ser un celular válido de 9 dígitos.")
            return False

        datos_limpios = {
            "dni": dni, 
            "nombres": nombres.strip(), 
            "telefono": telefono
        }
        
        exito = self.modelo_cliente.insertar_cliente(datos_limpios)

        if exito:
            self.vista_mensajes.mostrar_info("Cliente registrado correctamente.")
            return True
        return False