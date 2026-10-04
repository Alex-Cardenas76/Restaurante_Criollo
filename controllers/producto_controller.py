from decimal import Decimal, InvalidOperation

class ProductoController:
    def __init__(self, modelo_producto, vista_mensajes):
        self.modelo_producto = modelo_producto
        self.vista_mensajes = vista_mensajes

    def registrar_plato(self, nombre, categoria, precio_str):
        if not nombre.strip() or not categoria.strip():
            self.vista_mensajes.mostrar_advertencia("El nombre y categoría son obligatorios.")
            return False

        try:
            precio_exacto = Decimal(precio_str)
            if precio_exacto <= 0:
                self.vista_mensajes.mostrar_error("El precio debe ser estrictamente mayor a cero.")
                return False
        except InvalidOperation:
            self.vista_mensajes.mostrar_error("El formato del precio es inválido (ejemplo válido: 25.50).")
            return False

        datos_plato = {
            "nombre": nombre.strip(),
            "categoria": categoria.strip(),
            "precio": precio_exacto,
            "disponible": True
        }
        
        exito = self.modelo_producto.insertar_producto(datos_plato)
        if exito:
            self.vista_mensajes.mostrar_info("Plato agregado a la carta exitosamente.")
            return True
        return False