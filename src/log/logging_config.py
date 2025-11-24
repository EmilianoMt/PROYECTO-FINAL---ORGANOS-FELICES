"""
Configuración de loggers para la aplicación.
"""
import logging
import os

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

def setup_loggers():
    """
    Configura y devuelve los loggers para la aplicación. 
    loggers:
    - general: para mensajes informativos generales.
    - transacciones: para registrar transacciones específicas.
    - errores: para registrar errores.
    Cada logger escribe en su propio archivo dentro del directorio de logs.
    """
    general = logging.getLogger("general")
    gh = logging.FileHandler(os.path.join(LOG_DIR, "general.log"), encoding="utf-8")
    gh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    general.addHandler(gh)
    general.setLevel(logging.INFO)
    general.propagate = False

    trans = logging.getLogger("transacciones")
    th = logging.FileHandler(os.path.join(LOG_DIR, "transacciones.log"), encoding="utf-8")
    th.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    trans.addHandler(th)
    trans.setLevel(logging.INFO)
    trans.propagate = False

    errs = logging.getLogger("errores")
    eh = logging.FileHandler(os.path.join(LOG_DIR, "errores.log"), encoding="utf-8")
    eh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    errs.addHandler(eh)
    errs.setLevel(logging.ERROR)
    errs.propagate = False

    return general, trans, errs
