"""Pruebas de las validaciones de los controladores (sin base de datos)."""

import unittest
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import patch

from controllers import clientes_controller, empleados_controller, productos_controller
from controllers.comun import a_datetime, decimal_o_none, entero_o_none, texto


class TestClientes(unittest.TestCase):
    def test_cliente_valido(self):
        datos = {
            "StrNombre": "Ana Pérez",
            "NumDocumento": "123456",
            "StrEmail": "ana@example.com",
        }
        self.assertEqual(clientes_controller.validar_cliente(datos), {})

    def test_nombre_obligatorio(self):
        errores = clientes_controller.validar_cliente({"StrNombre": "   "})
        self.assertEqual(errores["StrNombre"], "El nombre es obligatorio.")

    def test_correo_invalido(self):
        errores = clientes_controller.validar_cliente(
            {"StrNombre": "Ana", "StrEmail": "ana@"}
        )
        self.assertEqual(
            errores["StrEmail"], "El correo no tiene un formato válido."
        )

    def test_documento_opcional_pero_numerico(self):
        self.assertNotIn(
            "NumDocumento",
            clientes_controller.validar_cliente({"StrNombre": "Ana"}),
        )
        errores = clientes_controller.validar_cliente(
            {"StrNombre": "Ana", "NumDocumento": "12a"}
        )
        self.assertIn("NumDocumento", errores)

    @patch("controllers.clientes_controller.cliente.insertar")
    def test_guardar_normaliza_valores(self, insertar):
        ok, _ = clientes_controller.guardar_cliente(
            {
                "StrNombre": "  Ana  ",
                "NumDocumento": "",
                "StrDireccion": None,
                "StrTelefono": None,
                "StrEmail": "",
            }
        )
        self.assertTrue(ok)
        datos = insertar.call_args[0][0]
        self.assertEqual(datos["StrNombre"], "Ana")
        self.assertIsNone(datos["NumDocumento"])
        self.assertEqual(datos["StrDireccion"], "")
        self.assertEqual(datos["StrUsuarioModifica"], "Sistema")
        self.assertIsInstance(datos["DtmFechaModifica"], datetime)


class TestEmpleados(unittest.TestCase):
    def test_empleado_valido(self):
        datos = {
            "strNombre": "Luis",
            "NumDocumento": "987654",
            "StrEmail": "luis@example.com",
        }
        self.assertEqual(empleados_controller.validar_empleado(datos), {})

    def test_nombre_y_documento_obligatorios(self):
        errores = empleados_controller.validar_empleado(
            {"strNombre": "", "NumDocumento": ""}
        )
        self.assertIn("strNombre", errores)
        self.assertIn("NumDocumento", errores)

    def test_documento_numerico(self):
        errores = empleados_controller.validar_empleado(
            {"strNombre": "Luis", "NumDocumento": "9x"}
        )
        self.assertIn("NumDocumento", errores)

    def test_correo_invalido(self):
        errores = empleados_controller.validar_empleado(
            {"strNombre": "Luis", "NumDocumento": "1", "StrEmail": "malo"}
        )
        self.assertEqual(
            errores["StrEmail"], "El correo no tiene un formato válido."
        )

    @patch("controllers.empleados_controller.empleado.insertar")
    def test_guardar_usa_usuario_javier_y_convierte_fechas(self, insertar):
        ok, _ = empleados_controller.guardar_empleado(
            {
                "strNombre": "Luis",
                "NumDocumento": "123",
                "StrEmail": "",
                "IdRolEmpleado": 1,
                "DtmIngreso": date(2026, 1, 2),
                "DtmRetiro": None,
            }
        )
        self.assertTrue(ok)
        datos = insertar.call_args[0][0]
        self.assertEqual(datos["StrUsuarioModifico"], "javier")
        self.assertEqual(datos["DtmIngreso"], datetime(2026, 1, 2))
        self.assertIsNone(datos["DtmRetiro"])


class TestProductos(unittest.TestCase):
    def test_producto_valido(self):
        datos = {"StrNombreProducto": "Café", "NumPrecio": 10.5, "NumStock": 3}
        self.assertEqual(productos_controller.validar_producto(datos), {})

    def test_nombre_obligatorio(self):
        errores = productos_controller.validar_producto(
            {"StrNombreProducto": "  "}
        )
        self.assertEqual(errores["StrNombreProducto"], "El nombre es obligatorio.")

    def test_precio_y_stock_negativos(self):
        errores = productos_controller.validar_producto(
            {"StrNombreProducto": "Café", "NumPrecio": -1, "NumStock": -2}
        )
        self.assertIn("NumPrecio", errores)
        self.assertIn("NumStock", errores)

    @patch("controllers.productos_controller.producto.insertar")
    def test_guardar_convierte_activo_y_permite_nulos(self, insertar):
        ok, _ = productos_controller.guardar_producto(
            {
                "StrNombreProducto": "Café",
                "NumPrecio": None,
                "NumStock": None,
                "BitActivo": False,
            }
        )
        self.assertTrue(ok)
        datos = insertar.call_args[0][0]
        self.assertIsNone(datos["NumPrecio"])
        self.assertIsNone(datos["NumStock"])
        self.assertEqual(datos["BitActivo"], 0)
        self.assertEqual(datos["StrUsuarioModifica"], "Sistema")


class TestComun(unittest.TestCase):
    def test_texto_convierte_none(self):
        self.assertEqual(texto(None), "")
        self.assertEqual(texto("  hola  "), "hola")

    def test_entero_o_none(self):
        self.assertIsNone(entero_o_none(""))
        self.assertIsNone(entero_o_none(None))
        self.assertEqual(entero_o_none("123"), 123)

    def test_decimal_o_none(self):
        self.assertIsNone(decimal_o_none(""))
        self.assertEqual(decimal_o_none("10.50"), Decimal("10.50"))

    def test_a_datetime(self):
        self.assertIsNone(a_datetime(None))
        self.assertEqual(
            a_datetime(date(2026, 1, 2)), datetime(2026, 1, 2, 0, 0, 0)
        )
        valor = datetime(2026, 1, 2, 15, 30)
        self.assertIs(a_datetime(valor), valor)


if __name__ == "__main__":
    unittest.main()
