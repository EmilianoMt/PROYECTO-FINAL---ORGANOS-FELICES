"""
Módulo de pruebas para las operaciones CRUD de órganos.
"""
import decimal
import pytest
import pymysql

from src.crud.crud import (
    insertar_organo,
    obtener_organos,
    actualizar_organo,
    eliminar_organo,
)


@pytest.fixture(scope="module", name="temporal_ids")
def temporal_ids_fixture():
    """Fixture para almacenar IDs de órganos creados durante las pruebas."""
    ids = []
    yield ids
    for _id in ids:
        try:
            eliminar_organo(_id)
        except pymysql.MySQLError:
            pass


def test_insertar_obtener(temporal_ids):
    """Prueba la inserción y obtención de órganos."""
    idn = insertar_organo("Test Órgano", 1234.5, "Descripción test")
    assert idn is not None
    temporal_ids.append(idn)
    rows = obtener_organos()
    assert any(r.get("id_organo") == idn for r in rows)


def test_obtener_organos_estructura():
    """Prueba la estructura de los datos obtenidos de órganos."""
    rows = obtener_organos()
    assert isinstance(rows, list)
    if rows:
        r = rows[0]
        assert "id_organo" in r
        assert "nombre" in r
        assert "descripcion" in r
        assert "precio" in r


def test_validacion_nombre():
    """Prueba las validaciones de nombre al insertar órganos."""
    with pytest.raises(ValueError):
        insertar_organo("", 1000, "x")


def test_actualizar(temporal_ids):
    """Prueba la actualización de un órgano."""
    idn = temporal_ids[0]
    ok = actualizar_organo(idn, "Test Actualizado", 2000, "Desc nueva")
    assert ok is True
    row = next((r for r in obtener_organos() if r.get("id_organo") == idn), None)
    assert row and row.get("nombre") == "Test Actualizado"


def test_eliminar_temporal():
    """Prueba la eliminación de un órgano."""
    idn = insertar_organo("Temp A Eliminar", 10, "tmp")
    assert idn is not None
    ok = eliminar_organo(idn)
    assert ok is True
    rows = obtener_organos()
    assert not any(r.get("id_organo") == idn for r in rows)


def test_precio_tipo():
    """Comprueba que el tipo de 'precio' es numérico/Decimal."""
    rows = obtener_organos()
    if rows:
        p = rows[0].get("precio")
        assert isinstance(p, (float, int, decimal.Decimal))
