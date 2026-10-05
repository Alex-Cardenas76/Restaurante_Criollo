from decimal import Decimal
from models import cliente_model, producto_model, pedido_model

class PedidoController:
    def __init__(self, vista, sesion_activa=None, vista_historial=None):
        self.vista = vista
        self.vista_historial = vista_historial
        self.sesion_activa = sesion_activa or {"id_usuario": 1, "usuario": "admin", "rol": "administrador"}
        self.carrito = []
        self.clientes_map = {}
        self.platos_map = {}

    def establecer_sesion(self, sesion):
        self.sesion_activa = sesion

    def establecer_vista_historial(self, vista_historial):
        self.vista_historial = vista_historial

    # =========================================================================
    # LÓGICA DE PUNTO DE VENTA Y CAJA (NUEVO PEDIDO)
    # =========================================================================
    def cargar_datos_iniciales(self):
        try:
            # 1. Cargar clientes
            clientes = cliente_model.listar_clientes()
            self.clientes_map = {}
            for c in clientes:
                etiqueta = f"{c[1]} (DNI: {c[2]})"
                self.clientes_map[etiqueta] = c[0]
            self.vista.poblar_clientes(clientes)

            # 2. Cargar platos disponibles para la carta
            platos = producto_model.listar_productos_disponibles()
            self.platos_map = {}
            for p in platos:
                etiqueta = f"{p[0]} - {p[1]} (S/. {float(p[3]):.2f})"
                self.platos_map[etiqueta] = {
                    "id": p[0],
                    "nombre": p[1],
                    "precio": Decimal(str(p[3]))
                }
            self.vista.poblar_platos(platos)

        except Exception as error:
            self.vista.mostrar_error(f"Error al cargar datos de pedidos: {error}")

    def agregar_plato_carrito(self):
        plato_seleccionado = self.vista.get_plato_seleccionado()
        cant_str = self.vista.get_cantidad()
        nota = self.vista.get_nota()

        if plato_seleccionado not in self.platos_map:
            self.vista.mostrar_error("Por favor, seleccione un plato válido de la carta.")
            return

        try:
            cantidad = int(cant_str)
            if cantidad < 1:
                self.vista.mostrar_error("La cantidad debe ser al menos 1.")
                return
        except ValueError:
            self.vista.mostrar_error("La cantidad debe ser un número entero válido.")
            return

        info_plato = self.platos_map[plato_seleccionado]
        precio_unitario = info_plato["precio"]
        subtotal = precio_unitario * Decimal(cantidad)

        item = {
            "id_producto": info_plato["id"],
            "nombre": info_plato["nombre"],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
            "nota_plato": nota
        }

        self.carrito.append(item)
        self._actualizar_interfaz_carrito()

    def quitar_plato_carrito(self):
        valores = self.vista.get_item_carrito_seleccionado()
        if not valores:
            self.vista.mostrar_error("Seleccione un plato de la tabla del carrito para eliminar.")
            return

        id_producto_quitar = int(valores[0])
        for i, item in enumerate(self.carrito):
            if item["id_producto"] == id_producto_quitar:
                del self.carrito[i]
                break

        self._actualizar_interfaz_carrito()

    def _actualizar_interfaz_carrito(self):
        total_monto = sum((item["subtotal"] for item in self.carrito), Decimal('0.00'))
        total_cant = sum(item["cantidad"] for item in self.carrito)
        self.vista.poblar_carrito(self.carrito, total_monto, total_cant)

    def manejar_generar_ticket(self):
        if not self.carrito:
            self.vista.mostrar_error("No hay platos en el carrito para cobrar.")
            return

        mesa = self.vista.get_mesa()
        if not mesa:
            self.vista.mostrar_error("Debe indicar el número de mesa o barra.")
            return

        cliente_str = self.vista.get_cliente_seleccionado()
        id_cliente = self.clientes_map.get(cliente_str)
        if not id_cliente:
            id_cliente = list(self.clientes_map.values())[0] if self.clientes_map else 1

        metodo_pago = self.vista.get_metodo_pago()
        usuario_id = self.sesion_activa.get("id_usuario", 1)
        total = sum((item["subtotal"] for item in self.carrito), Decimal('0.00'))

        detalles = [
            (
                item["id_producto"],
                item["cantidad"],
                item["precio_unitario"],
                item["subtotal"],
                item.get("nota_plato") or None
            )
            for item in self.carrito
        ]

        try:
            pedido_id = pedido_model.insertar_pedido(
                cliente_id=id_cliente,
                usuario_id=usuario_id,
                mesa=mesa,
                metodo_pago=metodo_pago,
                total=total,
                detalles=detalles,
                estado="Pagado"
            )

            if pedido_id:
                self.carrito.clear()
                self.vista.limpiar_formulario()
                self.vista.mostrar_exito(
                    f"¡Ticket generado y cobrado exitosamente!\n\n"
                    f"Comprobante N°: {pedido_id}\n"
                    f"Mesa: {mesa}\n"
                    f"Método de pago: {metodo_pago}\n"
                    f"Total Pagado: S/. {total:.2f}"
                )
                if self.vista_historial:
                    self.cargar_historial()
            else:
                self.vista.mostrar_error("No se pudo registrar el pedido en la base de datos.")
        except Exception as error:
            self.vista.mostrar_error(f"Error en la transacción del pedido: {error}")

    # =========================================================================
    # LÓGICA DE HISTORIAL DE PEDIDOS Y CONSULTA DE COMANDAS
    # =========================================================================
    def cargar_historial(self):
        if not self.vista_historial:
            return
        try:
            pedidos = pedido_model.listar_pedidos()
            self.vista_historial.poblar_tabla(pedidos)
        except Exception as error:
            self.vista_historial.mostrar_error(f"Error al cargar historial: {error}")

    def abrir_detalle_pedido(self, info_pedido):
        if not self.vista_historial:
            return
        pedido_id = info_pedido.get("id")
        try:
            detalles = pedido_model.listar_detalle_pedido(pedido_id)
            self.vista_historial.abrir_modal_detalle(info_pedido, detalles)
        except Exception as error:
            self.vista_historial.mostrar_error(f"Error al obtener detalle del pedido: {error}")