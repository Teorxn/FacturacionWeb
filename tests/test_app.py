"""Pruebas de humo de la interfaz con Streamlit AppTest.

Comprueban que el login aparece sin sesión y que las pantallas se dibujan
sin excepciones cuando hay un JWT válido. No insertan ni borran datos.
"""

import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from streamlit.testing.v1 import AppTest

from controllers import auth_controller
from models import usuario

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app.py"
SECRETS = RAIZ / ".streamlit" / "secrets.toml"


def _config_auth():
    if not SECRETS.exists():
        return None
    with SECRETS.open("rb") as archivo:
        return tomllib.load(archivo).get("auth")


AUTH_CONFIG = _config_auth()


def _token_rol(rol):
    if not AUTH_CONFIG:
        return None
    usuarios = usuario.listar_usuarios(AUTH_CONFIG)
    elegido = next(
        (dato for dato in usuarios.values() if dato["rol"] == rol),
        None,
    )
    if elegido is None:
        return None
    return auth_controller.crear_token(elegido, AUTH_CONFIG)


TOKEN_ADMIN = _token_rol("admin")
TOKEN_CONSULTA = _token_rol("consulta")


class TestLogin(unittest.TestCase):
    def test_sin_sesion_muestra_login(self):
        at = AppTest.from_file(str(APP), default_timeout=30)
        at.run()
        self.assertEqual(list(at.exception), [])
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Acceso al sistema", textos)
        self.assertEqual(len(at.text_input), 2)

    def test_token_invalido_muestra_login(self):
        at = AppTest.from_file(str(APP), default_timeout=30)
        at.session_state["_auth_token"] = "token-falso"
        at.run()
        self.assertEqual(list(at.exception), [])
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Acceso al sistema", textos)


class TestPantallas(unittest.TestCase):
    def _abrir(self, page, accion=None, id_=None):
        if not TOKEN_ADMIN:
            self.skipTest("Falta [auth] o un usuario admin en secrets.toml")

        at = AppTest.from_file(str(APP), default_timeout=30)
        at.session_state["_auth_token"] = TOKEN_ADMIN
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
        guardar = next(
            boton for boton in at.button if boton.label == "Guardar"
        )
        guardar.click().run()
        errores = " ".join(elemento.value for elemento in at.error)
        self.assertIn("El nombre es obligatorio.", errores)

    def test_pagina_seguridad(self):
        at = self._abrir("seguridad")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertIn("Seguridad", textos)
        self.assertIn("JWT firmado con HS256", textos)


class TestSoloLectura(unittest.TestCase):
    def _abrir(self, page, accion=None):
        if not TOKEN_CONSULTA:
            self.skipTest("Falta un usuario con rol consulta en secrets.toml")

        at = AppTest.from_file(str(APP), default_timeout=30)
        at.session_state["_auth_token"] = TOKEN_CONSULTA
        at.session_state["page"] = page
        if accion is not None:
            at.session_state["accion"] = accion
        at.run()
        self.assertEqual(list(at.exception), [], f"Excepción en {page}")
        return at

    def test_lista_sin_botones_de_escritura(self):
        at = self._abrir("clientes")
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertNotIn("NUEVO", textos)
        self.assertIn("Modo consulta", " ".join(e.value for e in at.info))

    def test_no_puede_abrir_formulario_nuevo(self):
        at = self._abrir("clientes", "nuevo")
        errores = " ".join(elemento.value for elemento in at.error)
        self.assertIn("solo permite consultar", errores)
        textos = " ".join(elemento.value for elemento in at.markdown)
        self.assertNotIn("Nuevo Cliente", textos)


if __name__ == "__main__":
    unittest.main()
