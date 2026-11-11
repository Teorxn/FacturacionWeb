"""Pruebas de humo de la interfaz con Streamlit AppTest.

Comprueban que las pantallas se dibujan sin excepciones y que las
validaciones muestran los mensajes en rojo. No insertan ni borran datos.
"""

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app.py"


class TestPantallas(unittest.TestCase):
    def _abrir(self, page, accion=None, id_=None):
        at = AppTest.from_file(str(APP), default_timeout=30)
        at.session_state["page"] = page
        if accion is not None:
            at.session_state["accion"] = accion
        if id_ is not None:
            at.session_state["id"] = id_
        at.run()
        self.assertEqual(list(at.exception), [], f"Excepción en {page}")
        return at

    def test_inicio(self):
        at = self._abrir("inicio")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Inicio", textos)

    def test_lista_clientes(self):
        at = self._abrir("clientes")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Lista de Clientes", textos)
        self.assertIn("NUEVO", textos)

    def test_lista_productos(self):
        at = self._abrir("productos")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Lista de Productos", textos)

    def test_lista_empleados(self):
        at = self._abrir("empleados")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("ADMON EMPLEADOS", textos)

    def test_formulario_nuevo_cliente(self):
        at = self._abrir("clientes", "nuevo")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Nuevo Cliente", textos)

    def test_formulario_nuevo_producto(self):
        at = self._abrir("productos", "nuevo")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Nuevo Producto", textos)

    def test_formulario_nuevo_empleado(self):
        at = self._abrir("empleados", "nuevo")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Ingreso Empleado", textos)

    def test_confirmacion_eliminar_cliente(self):
        at = self._abrir("clientes", "eliminar", 1)
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Eliminar Cliente", textos)
        self.assertIn("¿Está seguro", textos)

    def test_validacion_nombre_obligatorio(self):
        at = self._abrir("clientes", "nuevo")
        at.button[0].click().run()
        errores = " ".join(elemento.value for elemento in at.error)
        self.assertIn("El nombre es obligatorio.", errores)


if __name__ == "__main__":
    unittest.main()
