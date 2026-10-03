from database.conexion import conexion_segura


def insertar_producto(nombre, categoria, precio, disponible=True):
    """
    Inserta un producto. Devuelve el ID generado o None si falló.
    """
    try:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO productos (nombre, categoria, precio, disponible)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, categoria, precio, disponible))
            conexion.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            return nuevo_id
    except Exception as error:
        print(f"Error al insertar producto: {error}")
        return None


def listar_productos():
    """
    Devuelve todos los productos (disponibles y no disponibles).
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, categoria, precio, disponible FROM productos")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def listar_productos_disponibles():
    """
    Devuelve solo los productos con disponible = TRUE.
    Usado por la pantalla de Caja (regla RN-PRO-04).
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT id, nombre, categoria, precio, disponible
            FROM productos
            WHERE disponible = TRUE
            ORDER BY categoria, nombre
        """
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def listar_productos_por_categoria(categoria):
    """
    Devuelve los productos de una categoría específica.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = """
            SELECT id, nombre, categoria, precio, disponible
            FROM productos
            WHERE categoria = %s
        """
        cursor.execute(sql, (categoria,))
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def actualizar_disponibilidad(producto_id, disponible):
    """
    Cambia el estado de disponibilidad de un producto.
    Devuelve True si modificó una fila.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "UPDATE productos SET disponible = %s WHERE id = %s"
        cursor.execute(sql, (disponible, producto_id))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0


def actualizar_producto(producto_id, nombre=None, categoria=None, precio=None, disponible=None):
    """
    Actualiza solo los campos que se pasen (no None).
    """
    campos = []
    valores = []
    if nombre is not None:
        campos.append("nombre = %s")
        valores.append(nombre)
    if categoria is not None:
        campos.append("categoria = %s")
        valores.append(categoria)
    if precio is not None:
        campos.append("precio = %s")
        valores.append(precio)
    if disponible is not None:
        campos.append("disponible = %s")
        valores.append(disponible)

    if not campos:
        return False

    valores.append(producto_id)
    sql = f"UPDATE productos SET {', '.join(campos)} WHERE id = %s"

    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute(sql, tuple(valores))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0


def obtener_producto_por_id(producto_id):
    """
    Devuelve (id, nombre, categoria, precio, disponible) o None.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, categoria, precio, disponible FROM productos WHERE id = %s"
        cursor.execute(sql, (producto_id,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def eliminar_producto(producto_id):
    """
    Elimina un producto por su ID.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (producto_id,))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0