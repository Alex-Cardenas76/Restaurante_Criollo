from database.conexion import conexion_segura


def insertar_cliente(nombre, dni, telefono):
    """
    Inserta un nuevo cliente.
    Devuelve el ID generado, o None si falló (por ejemplo, DNI duplicado).
    """
    try:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, dni, telefono) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, dni, telefono))
            conexion.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            return nuevo_id
    except Exception as error:
        print(f"Error al insertar cliente: {error}")
        return None


def listar_clientes():
    """
    Devuelve una lista con todos los clientes.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, dni, telefono FROM clientes")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def buscar_cliente_por_dni(dni):
    """
    Busca un cliente por su DNI.
    Devuelve una tupla (id, nombre, dni, telefono) o None si no existe.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, dni, telefono FROM clientes WHERE dni = %s"
        cursor.execute(sql, (dni,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def buscar_cliente_por_id(id_cliente):
    """
    Busca un cliente por su ID.
    Devuelve una tupla (id, nombre, dni, telefono) o None si no existe.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, dni, telefono FROM clientes WHERE id = %s"
        cursor.execute(sql, (id_cliente,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def actualizar_cliente(id_cliente, nombre=None, dni=None, telefono=None):
    """
    Actualiza solo los campos que se pasen (no None).
    Devuelve True si modificó al menos una fila.
    """
    campos = []
    valores = []
    if nombre is not None:
        campos.append("nombre = %s")
        valores.append(nombre)
    if dni is not None:
        campos.append("dni = %s")
        valores.append(dni)
    if telefono is not None:
        campos.append("telefono = %s")
        valores.append(telefono)

    if not campos:
        return False

    valores.append(id_cliente)
    sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id = %s"

    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute(sql, tuple(valores))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0


def eliminar_cliente(id_cliente):
    """
    Elimina un cliente por su ID.
    Devuelve True si eliminó una fila.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(sql, (id_cliente,))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0