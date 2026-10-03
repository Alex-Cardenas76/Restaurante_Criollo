import mysql.connector
import os
from contextlib import contextmanager
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


def obtener_conexion():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    Usa las credenciales del archivo .env
    """
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None


@contextmanager
def conexion_segura():
    """
    Context manager que entrega una conexión y garantiza su cierre
    incluso si ocurre una excepción dentro del bloque `with`.

    Uso:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT ...")
            ...

    Si la conexión falla, lanza RuntimeError para que el llamador
    no reciba un None silencioso.
    """
    conexion = obtener_conexion()
    if conexion is None:
        raise RuntimeError("No se pudo establecer conexión con MySQL")
    try:
        yield conexion
    finally:
        if conexion.is_connected():
            conexion.close()