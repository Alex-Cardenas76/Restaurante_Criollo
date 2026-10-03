from database.conexion import conexion_segura


def obtener_usuario_por_nombre(nombre):
    """
    Busca un usuario por su nombre.
    Devuelve una tupla (id, nombre, contrasena, rol) o None si no existe.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, contrasena, rol FROM usuarios WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def obtener_usuario_por_id(id_usuario):
    """
    Busca un usuario por su ID.
    Devuelve una tupla (id, nombre, contrasena, rol) o None si no existe.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, contrasena, rol FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado


def insertar_usuario(nombre, contrasena, rol="vendedor"):
    """
    Inserta un nuevo usuario.
    Devuelve el ID generado o None si falló.
    """
    try:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            sql = "INSERT INTO usuarios (nombre, contrasena, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, contrasena, rol))
            conexion.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            return nuevo_id
    except Exception as error:
        print(f"Error al insertar usuario: {error}")
        return None


def listar_usuarios():
    """
    Devuelve una lista con todos los usuarios.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, rol FROM usuarios")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado


def actualizar_usuario(id_usuario, nombre=None, contrasena=None, rol=None):
    """
    Actualiza solo los campos que se pasen (no None).
    Devuelve True si modificó al menos una fila.
    """
    campos = []
    valores = []

    if nombre is not None:
        campos.append("nombre = %s")
        valores.append(nombre)
    if contrasena is not None:
        campos.append("contrasena = %s")
        valores.append(contrasena)
    if rol is not None:
        campos.append("rol = %s")
        valores.append(rol)

    if not campos:
        return False

    valores.append(id_usuario)
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"

    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        cursor.execute(sql, tuple(valores))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0


def eliminar_usuario(id_usuario):
    """
    Elimina un usuario por su ID.
    Devuelve True si eliminó una fila.
    """
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        return filas > 0