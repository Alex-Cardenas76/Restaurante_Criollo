from decimal import Decimal
from datetime import datetime

class PedidoController:
    def __init__(self, modelo_pedido, vista_mensajes):
        self.carrito = [] 
        self.modelo_pedido = modelo_pedido
        self.vista_mensajes = vista_mensajes 
        self.sesion_activa = None 

    def agregar_plato(self, id_producto, nombre, cantidad, precio_unitario, nota_plato=""):
        try:
            cantidad_int = int(cantidad)
            if cantidad_int <= 0:
                self.vista_mensajes.mostrar_advertencia("La cantidad debe ser mayor a cero.")
                return False
        except ValueError:
            self.vista_mensajes.mostrar_error("La cantidad debe ser un número entero.")
            return False

        precio_exacto = Decimal(str(precio_unitario))
        subtotal_exacto = precio_exacto * cantidad_int

        item = {
            "id_producto": id_producto, 
            "nombre": nombre,
            "cantidad": cantidad_int,
            "precio_unitario": precio_exacto,
            "subtotal": subtotal_exacto,
            "nota_plato": nota_plato
        }
        
        self.carrito.append(item)
        return True 

    def calcular_total(self):
        return sum((item["subtotal"] for item in self.carrito), Decimal('0.00'))

    def consolidar_pedido(self, id_cliente, numero_mesa, metodo_pago):
        if not self.carrito:
            self.vista_mensajes.mostrar_advertencia("El carrito está vacío.")
            return False

        if not id_cliente or not numero_mesa:
            self.vista_mensajes.mostrar_advertencia("Faltan datos del cliente o mesa.")
            return False

        cabecera_pedido = {
            "id_cliente": id_cliente,
            "id_usuario": self.sesion_activa.get("id_usuario"),
            "fecha": datetime.now(), 
            "numero_mesa": numero_mesa,
            "total": self.calcular_total(),
            "metodo_pago": metodo_pago,
            "estado": "Completado"
        }

        exito = self.modelo_pedido.guardar_transaccion(cabecera_pedido, self.carrito)
        
        if exito:
            self.carrito.clear() 
            self.vista_mensajes.mostrar_info("Cobro realizado y guardado con éxito.")
            return True
        else:
            self.vista_mensajes.mostrar_error("Error al guardar en la base de datos.")
            return False