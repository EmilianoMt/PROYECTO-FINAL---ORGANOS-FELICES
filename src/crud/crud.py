"""
CRUD para la tabla organos.
"""
import pymysql
from src.db.db import get_connection
from src.log.logging_config import setup_loggers
from src.validations.validation import validate_nombre, validate_precio, validate_descripcion

general, log_transacciones, log_errores = setup_loggers()

def obtener_organos():
    """Retorna lista de dicts: id_organo, nombre, descripcion, precio"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_organo, nombre, descripcion, precio FROM organos")
            rows = cursor.fetchall()
        log_transacciones.info('Órganos obtenidos exitosamente')
        return rows or []
    except pymysql.MySQLError as e:
        log_errores.error('Error al obtener órganos (DB): %s', e, exc_info=True)
        return []
    finally:
        if conn:
            conn.close()

def insertar_organo(nombre, precio, descripcion):
    """Inserta y devuelve id insertado (int) o None en error DB.

    Nota: las validaciones lanzan ValueError y se dejan propagar para que la UI/tests las detecten.
    """
    if not (validate_nombre(nombre) and validate_precio(precio)
            and validate_descripcion(descripcion)):
        raise ValueError("Datos inválidos")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO organos (nombre, descripcion, precio) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre.strip(), descripcion.strip(), float(precio)))
            conn.commit()
            last = cursor.lastrowid
        log_transacciones.info('Órgano insertado: %s, Precio: %s', nombre, precio)
        return last
    except pymysql.MySQLError as e:
        log_errores.error('Error al insertar órgano (DB): %s', e, exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def actualizar_organo(id_organo, nombre, precio, descripcion):
    """Actualiza y devuelve True si se actualizó, False en caso contrario."""
    if not (validate_nombre(nombre) and validate_precio(precio)
            and validate_descripcion(descripcion)):
        raise ValueError("Datos inválidos")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE organos SET nombre=%s, descripcion=%s, precio=%s WHERE id_organo=%s"
            cursor.execute(sql, (nombre.strip(), descripcion.strip(), float(precio), id_organo))
            conn.commit()
            if cursor.rowcount == 0:
                log_errores.error('No se encontró el órgano con ID %s para actualizar', id_organo)
                return False
        log_transacciones.info('Órgano actualizado: ID %s, Nombre: %s', id_organo, nombre)
        return True
    except pymysql.MySQLError as e:
        log_errores.error('Error al actualizar órgano (DB): %s', e, exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def eliminar_organo(id_organo):
    """Elimina y devuelve True si se eliminó, False en caso contrario."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM organos WHERE id_organo=%s"
            cursor.execute(sql, (id_organo,))
            conn.commit()
            if cursor.rowcount == 0:
                log_errores.error('No se encontró el órgano con ID %s para eliminar', id_organo)
                return False
        log_transacciones.info('Órgano eliminado: ID %s', id_organo)
        return True
    except pymysql.MySQLError as e:
        log_errores.error('Error al eliminar órgano (DB): %s', e, exc_info=True)
        return False
    finally:
        if conn:
            conn.close()
