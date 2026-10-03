from database.conexion import conexion_segura


def insertar_pedido(cliente_id, usuario_id, mesa, metodo_pago, total, detalles, estado="Pagado"):
    """
    Guarda un pedido completo (cabecera + detalle) de forma atómica.
    Si algo falla, no se guarda nada (rollback).

    detalles: lista de tuplas (producto_id, cantidad, precio_unitario, subtotal, nota_plato)
              nota_plato puede ser None.
    Devuelve el ID del pedido generado, o None si falló.
    """
    try:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            try:
                # 1. Insertar la cabecera del pedido
                sql_pedido = """
                    INSERT INTO pedidos
                        (cliente_id, usuario_id, mesa, metodo_pago, total, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql_pedido,
                    (cliente_id, usuario_id, mesa, metodo_pago, total, estado)
                )
                pedido_id = cursor.lastrowid

                # 2. Insertar cada renglón del detalle
                sql_detalle = """
                    INSERT INTO detalle_pedidos
                        (pedido_id, producto_id, cantidad, precio_unitario, subtotal, nota_plato)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                for producto_id, cantidad, precio_unitario, subtotal, nota_plato in detalles:
                    cursor.execute(
                        sql_detalle,
                        (pedido_id, producto_id, cantidad, precio_unitario, subtotal, nota_plato)
                    )

                # 3. Confirmar la transacción
                conexion.commit()
                cursor.close()
                return pedido_id

            except Exception as error:
                # Si algo falla, deshacer todo
                conexion.rollback()
                cursor.close()
                print(f"Error al guardar el pedido: {error}")
                return None
    except Exception as error:
        print(f"Error de conexión: {error}")
        return None


def listar_pedidos():
    """
    Lista todos los pedidos con datos del cliente y del usuario.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT p.id, c.nombre AS cliente, u.nombre AS usuario,
                   p.mesa, p.metodo_pago, p.total, p.estado, p.fecha
            FROM pedidos p
            LEFT JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY p.fecha DESC
        """
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def listar_detalle_pedido(pedido_id):
    """
    Lista los renglones de un pedido con nombre del producto.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT dp.id, dp.producto_id, p.nombre, dp.cantidad,
                   dp.precio_unitario, dp.subtotal, dp.nota_plato
            FROM detalle_pedidos dp
            INNER JOIN productos p ON dp.producto_id = p.id
            WHERE dp.pedido_id = %s
        """
        cursor.execute(sql, (pedido_id,))
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def obtener_pedido_por_id(pedido_id):
    """
    Devuelve la cabecera del pedido o None.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT id, cliente_id, usuario_id, mesa, metodo_pago, total, estado, fecha
            FROM pedidos
            WHERE id = %s
        """
        cursor.execute(sql, (pedido_id,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def actualizar_estado_pedido(pedido_id, nuevo_estado):
    """
    Actualiza el estado de un pedido (ej: 'Pagado' -> 'Anulado').
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "UPDATE pedidos SET estado = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_estado, pedido_id))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0