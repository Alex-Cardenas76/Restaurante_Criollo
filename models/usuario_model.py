from database.conexion import obtener_conexion


def obtener_usuario_por_nombre(nombre):
    """
    Busca un usuario por su nombre.
    Devuelve una tupla (id, nombre, contrasena, rol) o None si no existe.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "SELECT id, nombre, contrasena, rol FROM usuarios WHERE nombre = %s"
    cursor.execute(sql, (nombre,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado


def insertar_usuario(nombre, contrasena, rol="vendedor"):
    """
    Inserta un nuevo usuario en la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO usuarios (nombre, contrasena, rol) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, contrasena, rol))
    conexion.commit()
    cursor.close()
    conexion.close()


def listar_usuarios():
    """
    Devuelve una lista con todos los usuarios.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, rol FROM usuarios")
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado