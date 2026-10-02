from database.conexion import obtener_conexion


def insertar_producto(nombre, precio, disponible=True):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO productos (nombre, precio, disponible) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, precio, disponible))
    conexion.commit()
    cursor.close()
    conexion.close()


def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio, disponible FROM productos")
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def actualizar_disponibilidad(producto_id, disponible):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "UPDATE productos SET disponible = %s WHERE id = %s"
    cursor.execute(sql, (disponible, producto_id))
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_producto_por_id(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "SELECT id, nombre, precio, disponible FROM productos WHERE id = %s"
    cursor.execute(sql, (producto_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado