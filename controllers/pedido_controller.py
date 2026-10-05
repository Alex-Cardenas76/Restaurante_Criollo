from decimal import Decimal
from models import cliente_model, producto_model, pedido_model

class PedidoController:
    MESAS_BASE = ["Mesa 01", "Mesa 02", "Mesa 03", "Mesa 04", "Mesa 05", "Mesa 06", "Para Llevar"]

    def __init__(self, vista, sesion_activa=None, vista_historial=None):
        self.vista = vista
        self.vista_historial = vista_historial
        self.sesion_activa = sesion_activa or {"id_usuario": 1, "usuario": "admin", "rol": "administrador"}
        self.carrito = []
        self.clientes_map = {}
        self.platos_map = {}
        self.mesas_ocupadas = {}

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

            # 3. Cargar estado de mesas ocupadas/libres
            self.mesas_ocupadas = pedido_model.obtener_mesas_ocupadas()
            opciones_mesas = []
            for m in self.MESAS_BASE:
                if m == "Para Llevar":
                    opciones_mesas.append("Para Llevar")
                elif m in self.mesas_ocupadas:
                    opciones_mesas.append(f"{m} (Ocupada - Pedido #{self.mesas_ocupadas[m]})")
                else:
                    opciones_mesas.append(f"{m} (Disponible)")
            self.vista.poblar_mesas(opciones_mesas)

        except Exception as error:
            self.vista.mostrar_error(f"Error al cargar datos de pedidos: {error}")

    def _limpiar_nombre_mesa(self, mesa_texto: str) -> str:
        # Extraer el nombre base de la mesa quitando sufijos de estado
        for m in self.MESAS_BASE:
            if mesa_texto.startswith(m):
                return m
        return mesa_texto.split("(")[0].strip()

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

    def procesar_pedido(self, estado_deseado="Pagado"):
        if not self.carrito:
            self.vista.mostrar_error("No hay platos en el carrito para procesar.")
            return

        mesa_cruda = self.vista.get_mesa()
        if not mesa_cruda:
            self.vista.mostrar_error("Debe indicar el número de mesa o ubicación.")
            return

        mesa = self._limpiar_nombre_mesa(mesa_cruda)

        # VALIDACIÓN DE MESA OCUPADA
        # Si la mesa no es "Para Llevar" y ya tiene un pedido en estado 'Pendiente':
        self.mesas_ocupadas = pedido_model.obtener_mesas_ocupadas()
        if mesa != "Para Llevar" and mesa in self.mesas_ocupadas:
            id_ped_ocupado = self.mesas_ocupadas[mesa]
            self.vista.mostrar_error(
                f"⚠️ ATENCIÓN: La '{mesa}' ya se encuentra OCUPADA con el Pedido N° {id_ped_ocupado} pendiente de cobro.\n\n"
                f"Debe cobrar o liberar ese pedido en el 'Historial de Ventas' antes de abrir una nueva comanda en esta mesa."
            )
            return

        cliente_str = self.vista.get_cliente_seleccionado()
        id_cliente = self.clientes_map.get(cliente_str)
        if not id_cliente:
            id_cliente = list(self.clientes_map.values())[0] if self.clientes_map else 1

        metodo_pago = self.vista.get_metodo_pago() if estado_deseado == "Pagado" else "Por cobrar"
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
                estado=estado_deseado
            )

            if pedido_id:
                self.carrito.clear()
                self.vista.limpiar_formulario()
                self.cargar_datos_iniciales()  # Refresca el estado de mesas

                if estado_deseado == "Pendiente":
                    self.vista.mostrar_exito(
                        f"📝 ¡Comanda enviada a cocina!\n\n"
                        f"Pedido N°: {pedido_id}\n"
                        f"Mesa: {mesa} (Queda OCUPADA)\n"
                        f"Estado: PENDIENTE DE COBRO\n"
                        f"Total acumulado: S/. {total:.2f}"
                    )
                else:
                    self.vista.mostrar_exito(
                        f"💳 ¡Cobro registrado con éxito!\n\n"
                        f"Comprobante N°: {pedido_id}\n"
                        f"Mesa: {mesa} (Queda LIBRE)\n"
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
    # LÓGICA DE HISTORIAL DE PEDIDOS Y COBRO DE COMANDAS PENDIENTES
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

    def iniciar_cobro_pedido(self, info_pedido):
        if not self.vista_historial:
            return
        self.vista_historial.abrir_modal_cobro(info_pedido, self.confirmar_cobro_pendiente)

    def confirmar_cobro_pendiente(self, pedido_id, metodo_pago, modal):
        try:
            exito = pedido_model.pagar_pedido(pedido_id, metodo_pago)
            if exito:
                modal.destroy()
                self.vista_historial.mostrar_exito(
                    f"¡Pago confirmado!\n\nEl Pedido N° {pedido_id} ha sido marcado como PAGADO mediante {metodo_pago}.\nLa mesa asociada ha quedado LIBRE."
                )
                self.cargar_historial()
                self.cargar_datos_iniciales()  # Libera la mesa en la vista de pedidos
            else:
                self.vista_historial.mostrar_error("No se pudo actualizar el estado del pedido.")
        except Exception as error:
            self.vista_historial.mostrar_error(f"Error al procesar cobro: {error}")