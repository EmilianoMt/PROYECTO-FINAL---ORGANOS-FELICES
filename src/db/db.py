"""
Módulo para manejar la conexión a la base de datos MySQL usando pymysql.
"""
import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    """Devuelve una conexión pymysql usando variables fijas (no variables de entorno)."""
    host = "localhost"
    user = "root"
    password = "1234"
    db = "organos_felices"
    port = 3306
    return pymysql.connect(host=host,
                           user=user,
                           passwd=password,
                           db=db,
                           port=port,
                           cursorclass=DictCursor)
