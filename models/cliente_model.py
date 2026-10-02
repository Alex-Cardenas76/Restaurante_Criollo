from database.conexion import obtener_conexion


def insertar_cliente(nombre, dni, telefono):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO clientes (nombre, dni, telefono) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, dni, telefono))
    conexion.commit()
    cursor.close()
    conexion.close()


def listar_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, dni, telefono FROM clientes")
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultado


def buscar_cliente_por_dni(dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "SELECT id, nombre, dni, telefono FROM clientes WHERE dni = %s"
    cursor.execute(sql, (dni,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado