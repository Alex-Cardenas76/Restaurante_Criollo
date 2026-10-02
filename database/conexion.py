import mysql.connector
import os
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
            port=os.getenv("DB_PORT")
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None