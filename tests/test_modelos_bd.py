"""Pruebas de los modelos contra MySQL, sin dejar cambios guardados.

Se abre una conexión con autocommit desactivado. Los modelos llaman a
commit(), pero aquí commit() no hace nada y al final se ejecuta rollback().
Así se prueba INSERT, UPDATE, DELETE y SELECT de verdad, y la base de datos
del curso queda igual.

Si no hay conexión, las pruebas se marcan como omitidas (skip).
"""

import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import mysql.connector

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from models import cliente, empleado, producto

RAIZ = Path(__file__).resolve().parent.parent
SECRETS = RAIZ / ".streamlit" / "secrets.toml"


def _config():
    with SECRETS.open("rb") as archivo:
        return tomllib.load(archivo)["mysql"]


def _conectar():
    cfg = _config()
    return mysql.connector.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        database=cfg["database"],
        user=cfg["user"],
        password=cfg["password"],
        connection_timeout=10,
        autocommit=False,
        client_flags=[mysql.connector.constants.ClientFlag.FOUND_ROWS],
    )


class ConexionSinCommit:
    """Envuelve una conexión para que commit() y close() no hagan nada."""

    def __init__(self, con):
        self._con = con

    def cursor(self, **kwargs):
        return self._con.cursor(**kwargs)

    def commit(self):
        pass

    def close(self):
        pass


class TestModelosBD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SECRETS.exists():
            raise unittest.SkipTest("No existe .streamlit/secrets.toml")
        try:
            cls.con = _conectar()
        except mysql.connector.Error as exc:
            raise unittest.SkipTest(f"No se pudo conectar a MySQL: {exc}")

    @classmethod
    def tearDownClass(cls):
        cls.con.rollback()
        cls.con.close()

    def setUp(self):
        self.conexion = ConexionSinCommit(self.con)
        self.parches = [
            patch.object(cliente, "get_connection", return_value=self.conexion),
            patch.object(empleado, "get_connection", return_value=self.conexion),
            patch.object(producto, "get_connection", return_value=self.conexion),
        ]
        for parche in self.parches:
            parche.start()

    def tearDown(self):
        for parche in reversed(self.parches):
            parche.stop()
        self.con.rollback()

    def test_crud_cliente(self):
        datos = {
            "StrNombre": "ZZ Cliente de prueba",
            "NumDocumento": 99999999,
            "StrDireccion": "Calle 1",
            "StrTelefono": "3000000000",
            "StrEmail": "zz@example.com",
            "DtmFechaModifica": datetime.now(),
            "StrUsuarioModifica": "Sistema",
        }
        id_cliente = cliente.insertar(datos)
        self.assertIsNotNone(id_cliente)

        fila = cliente.obtener(id_cliente)
        self.assertEqual(fila["StrNombre"], "ZZ Cliente de prueba")

        filas = cliente.actualizar(
            id_cliente, {**datos, "StrNombre": "ZZ Cliente actualizado"}
        )
        self.assertEqual(filas, 1)
        self.assertEqual(
            cliente.obtener(id_cliente)["StrNombre"], "ZZ Cliente actualizado"
        )

        self.assertEqual(cliente.eliminar(id_cliente), 1)
        self.assertIsNone(cliente.obtener(id_cliente))

    def test_crud_empleado(self):
        datos = {
            "strNombre": "ZZ Empleado de prueba",
            "NumDocumento": 88888888,
            "StrDireccion": "Calle 2",
            "StrTelefono": "3010000000",
            "StrEmail": "zzemp@example.com",
            "IdRolEmpleado": 1,
            "DtmIngreso": datetime(2026, 1, 2),
            "DtmRetiro": None,
            "strDatosAdicionales": "Prueba",
            "DtmFechaModifica": datetime.now(),
            "StrUsuarioModifico": "javier",
        }
        id_empleado = empleado.insertar(datos)
        self.assertIsNotNone(id_empleado)

        fila = empleado.obtener(id_empleado)
        self.assertEqual(fila["strNombre"], "ZZ Empleado de prueba")
        self.assertEqual(fila["StrDescripcionRol"], "Gerente")

        filas = empleado.actualizar(
            id_empleado, {**datos, "strNombre": "ZZ Empleado actualizado"}
        )
        self.assertEqual(filas, 1)

        self.assertEqual(empleado.eliminar(id_empleado), 1)
        self.assertIsNone(empleado.obtener(id_empleado))

    def test_crud_producto(self):
        datos = {
            "StrNombreProducto": "ZZ Producto de prueba",
            "StrDescripcion": "Prueba",
            "NumPrecio": Decimal("12.50"),
            "NumStock": 3,
            "StrCategoria": "Prueba",
            "BitActivo": 1,
            "DtmFechaModifica": datetime.now(),
            "StrUsuarioModifica": "Sistema",
        }
        id_producto = producto.insertar(datos)
        self.assertIsNotNone(id_producto)

        fila = producto.obtener(id_producto)
        self.assertEqual(fila["StrNombreProducto"], "ZZ Producto de prueba")
        self.assertEqual(fila["NumPrecio"], Decimal("12.50"))

        filas = producto.actualizar(
            id_producto,
            {**datos, "StrNombreProducto": "ZZ Producto actualizado"},
        )
        self.assertEqual(filas, 1)

        self.assertEqual(producto.eliminar(id_producto), 1)
        self.assertIsNone(producto.obtener(id_producto))


if __name__ == "__main__":
    unittest.main()
