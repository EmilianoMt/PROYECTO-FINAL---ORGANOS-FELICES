"""
Módulo para manejar la conexión a la base de datos MySQL usando pymysql.
"""
import logging
import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    """Devuelve una conexión pymysql usando variables fijas."""
    host = "localhost"
    user = "root"
    password = "1234"
    db = "organos_felices"
    port = 3306
    general = logging.getLogger("general")
    general.info("Estableciendo conexión a la base de datos")
    return pymysql.connect(host=host,
                           user=user,
                           passwd=password,
                           db=db,
                           port=port,
                           cursorclass=DictCursor)
