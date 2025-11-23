"""
Módulo para validaciones de datos de órganos.
"""
from decimal import Decimal, InvalidOperation

def validate_nombre(nombre: str) -> bool:
    """Valida que el nombre no esté vacío y no exceda 100 caracteres."""
    return bool(nombre and nombre.strip() and len(nombre.strip()) <= 100)

def validate_descripcion(descripcion: str) -> bool:
    """Valida que la descripción no exceda 255 caracteres (puede estar vacía)."""
    return bool(descripcion is not None and len(descripcion.strip()) <= 255)

def validate_precio(precio) -> bool:
    """Valida que el precio sea un número decimal no negativo."""
    try:
        p = Decimal(str(precio))
        return p >= 0
    except (InvalidOperation, TypeError, ValueError):
        return False
