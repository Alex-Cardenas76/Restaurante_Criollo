from database.conexion import obtener_conexion


def insertar_pedido(cliente_id, usuario_id, mesa, metodo_pago, total, detalles):
    """
    Guarda un pedido completo (cabecera + detalle) de forma atómica.
    Si algo falla, no se guarda nada (rollback).

    detalles: lista de tuplas (producto_id, cantidad, subtotal)
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # 1. Insertar la cabecera del pedido
        sql_pedido = """
            INSERT INTO pedidos (cliente_id, usuario_id, mesa, metodo_pago, total)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_pedido, (cliente_id, usuario_id, mesa, metodo_pago, total))
        pedido_id = cursor.lastrowid

        # 2. Insertar cada renglón del detalle
        sql_detalle = """
            INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, subtotal)
            VALUES (%s, %s, %s, %s)
        """
        for producto_id, cantidad, subtotal in detalles:
            cursor.execute(sql_detalle, (pedido_id, producto_id, cantidad, subtotal))

        # 3. Confirmar la transacción
        conexion.commit()
        return pedido_id

    except Exception as error:
        # Si algo falla, deshacer todo
        conexion.rollback()
        print(f"Error al guardar el pedido: {error}")
        return None

    finally:
        cursor.close()
        conexion.close()


def listar_pedidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        SELECT id, cliente_id, usuario_id, mesa, metodo_pago, total, fecha
        FROM pedidos
        ORDER BY fecha DESC
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def listar_detalle_pedido(pedido_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        SELECT dp.id, dp.producto_id, p.nombre, dp.cantidad, dp.subtotal
        FROM detalle_pedidos dp
        INNER JOIN productos p ON dp.producto_id = p.id
        WHERE dp.pedido_id = %s
    """
    cursor.execute(sql, (pedido_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado