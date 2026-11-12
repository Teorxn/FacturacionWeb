"""Pruebas de seguridad: contraseñas, JWT, permisos, XSS y SQL injection."""

import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt

from controllers import auth_controller
from controllers.comun import texto
from models import cliente, usuario
from views.componentes import enlace, escapar, tabla, unir_html

CONFIG = {
    "jwt_secret": "x" * 64,
    "token_minutos": 30,
    "max_intentos": 3,
    "bloqueo_minutos": 5,
    "issuer": "facturacion-streamlit",
    "users": {
        "ana": {
            "nombre": "Ana",
            "rol": "vendedor",
            "activo": True,
            "password_hash": usuario.generar_hash("ClaveSegura123"),
        },
        "inactivo": {
            "nombre": "Inactivo",
            "rol": "consulta",
            "activo": False,
            "password_hash": usuario.generar_hash("ClaveSegura123"),
        },
    },
}


class TestPasswords(unittest.TestCase):
    def test_hash_y_verificacion(self):
        almacenado = usuario.generar_hash("ClaveSegura123")
        self.assertTrue(almacenado.startswith("pbkdf2_sha256$600000$"))
        self.assertTrue(usuario.verificar_hash("ClaveSegura123", almacenado))
        self.assertFalse(usuario.verificar_hash("otra", almacenado))

    def test_hash_malformado_no_lanza_error(self):
        self.assertFalse(usuario.verificar_hash("x", "texto"))
        self.assertFalse(usuario.verificar_hash("x", ""))
        self.assertFalse(usuario.verificar_hash("x", None))

    def test_rechaza_iteraciones_debiles(self):
        with self.assertRaises(ValueError):
            usuario.generar_hash("ClaveSegura123", iteraciones=1000)

    def test_password_vacia(self):
        with self.assertRaises(ValueError):
            usuario.generar_hash("")


class TestUsuarios(unittest.TestCase):
    def test_autenticar_correcto(self):
        encontrado = usuario.autenticar("ANA", "ClaveSegura123", CONFIG)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado["rol"], "vendedor")

    def test_autenticar_incorrecto(self):
        self.assertIsNone(usuario.autenticar("ana", "mala", CONFIG))
        self.assertIsNone(usuario.autenticar("nadie", "ClaveSegura123", CONFIG))

    def test_usuario_inactivo_no_entra(self):
        self.assertIsNone(
            usuario.autenticar("inactivo", "ClaveSegura123", CONFIG)
        )

    def test_normaliza_usuario(self):
        self.assertEqual(usuario.normalizar_usuario("  Ana "), "ana")


class TestJWT(unittest.TestCase):
    def _payload(self):
        return {
            "usuario": "ana",
            "nombre": "Ana",
            "rol": "vendedor",
        }

    def test_crear_y_validar(self):
        token = auth_controller.crear_token(self._payload(), CONFIG)
        payload = auth_controller.validar_token(token, CONFIG)
        self.assertEqual(payload["sub"], "ana")
        self.assertEqual(payload["rol"], "vendedor")
        self.assertEqual(payload["iss"], "facturacion-streamlit")
        self.assertIn("exp", payload)
        self.assertIn("jti", payload)

    def test_token_alterado(self):
        token = auth_controller.crear_token(self._payload(), CONFIG)
        self.assertIsNone(auth_controller.validar_token(token + "x", CONFIG))

    def test_token_expirado(self):
        ayer = datetime.now(timezone.utc) - timedelta(hours=2)
        token = auth_controller.crear_token(
            self._payload(), CONFIG, ahora=ayer
        )
        self.assertIsNone(auth_controller.validar_token(token, CONFIG))

    def test_secreto_equivocado(self):
        token = auth_controller.crear_token(self._payload(), CONFIG)
        otro = {**CONFIG, "jwt_secret": "y" * 64}
        self.assertIsNone(auth_controller.validar_token(token, otro))

    def test_algoritmo_none_rechazado(self):
        payload = {
            "sub": "ana",
            "rol": "admin",
            "iss": "facturacion-streamlit",
            "iat": datetime.now(timezone.utc),
            "nbf": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        }
        token = jwt.encode(payload, None, algorithm="none")
        self.assertIsNone(auth_controller.validar_token(token, CONFIG))

    def test_secreto_corto_rechazado(self):
        with self.assertRaises(usuario.ErrorAuth):
            auth_controller.crear_token(
                self._payload(), {**CONFIG, "jwt_secret": "corto"}
            )


class TestPermisos(unittest.TestCase):
    def test_admin_ve_todo(self):
        for page in auth_controller.PERMISOS["admin"]:
            self.assertTrue(auth_controller.tiene_permiso("admin", page))

    def test_consulta_no_administra(self):
        self.assertTrue(auth_controller.tiene_permiso("consulta", "clientes"))
        self.assertFalse(auth_controller.tiene_permiso("consulta", "empleados"))
        self.assertFalse(auth_controller.tiene_permiso("consulta", "seguridad"))

    def test_rol_desconocido_no_tiene_permisos(self):
        self.assertFalse(auth_controller.tiene_permiso("hacker", "inicio"))

    def test_solo_admin_y_vendedor_escriben(self):
        self.assertTrue(auth_controller.puede_escribir("admin"))
        self.assertTrue(auth_controller.puede_escribir("vendedor"))
        self.assertFalse(auth_controller.puede_escribir("consulta"))
        self.assertFalse(auth_controller.puede_escribir("hacker"))

    def test_solo_admin_administra_seguridad(self):
        self.assertTrue(auth_controller.puede_administrar("admin"))
        self.assertFalse(auth_controller.puede_administrar("vendedor"))
        self.assertFalse(auth_controller.puede_administrar("consulta"))


class TestRateLimit(unittest.TestCase):
    def setUp(self):
        auth_controller._INTENTOS.clear()

    def tearDown(self):
        auth_controller._INTENTOS.clear()

    def test_bloqueo_tras_intentos(self):
        for _ in range(3):
            auth_controller._registrar_fallo("ana", CONFIG)
        self.assertGreater(auth_controller._segundos_bloqueo("ana"), 0)

    def test_login_correcto_limpia_intentos(self):
        auth_controller._registrar_fallo("ana", CONFIG)
        auth_controller._limpiar_fallos("ana")
        self.assertEqual(auth_controller._segundos_bloqueo("ana"), 0)


class TestXSS(unittest.TestCase):
    def test_escapar_html(self):
        self.assertEqual(
            escapar('<script>alert("x")</script>'),
            "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;",
        )
        self.assertEqual(escapar(None), "")

    def test_tabla_escapa_celdas_por_defecto(self):
        html = tabla(["Nombre"], [["<script>alert(1)</script>"]])
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_tabla_respeta_enlaces_de_la_app(self):
        acciones = unir_html(
            enlace("Editar", "?page=clientes&accion=editar&id=1", "btn btn-info"),
            " ",
            enlace("Eliminar", "?page=clientes&accion=eliminar&id=1", "btn btn-danger"),
        )
        html = tabla(["Acciones"], [[acciones]])
        self.assertIn('<a class="btn btn-info"', html)
        self.assertIn("&amp;accion=editar", html)
        self.assertNotIn("&lt;a", html)

    def test_enlace_escapa_texto_y_destino(self):
        html = enlace('<img src=x onerror=alert(1)>', '"><script>')
        self.assertNotIn("<img", html)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;img", html)


class CursorFalso:
    def __init__(self):
        self.sql = None
        self.params = None
        self.rowcount = 0
        self.lastrowid = 1

    def execute(self, sql, params=None):
        self.sql = sql
        self.params = params

    def fetchone(self):
        return None

    def fetchall(self):
        return []

    def close(self):
        pass


class ConexionFalsa:
    def __init__(self):
        self.cursor_obj = CursorFalso()

    def cursor(self, **kwargs):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


class TestSQLInjection(unittest.TestCase):
    PAYLOAD = "1 OR 1=1; DROP TABLE TBLCLIENTES; --"

    def test_obtener_usa_parametros(self):
        con = ConexionFalsa()
        with patch("models.cliente.get_connection", return_value=con):
            cliente.obtener(self.PAYLOAD)

        cur = con.cursor_obj
        self.assertIn("%s", cur.sql)
        self.assertNotIn(self.PAYLOAD, cur.sql)
        self.assertEqual(cur.params, (self.PAYLOAD,))

    def test_eliminar_usa_parametros(self):
        con = ConexionFalsa()
        with patch("models.cliente.get_connection", return_value=con):
            cliente.eliminar(self.PAYLOAD)

        cur = con.cursor_obj
        self.assertIn("%s", cur.sql)
        self.assertNotIn(self.PAYLOAD, cur.sql)
        self.assertEqual(cur.params, (self.PAYLOAD,))


class TestCaracteresControl(unittest.TestCase):
    def test_elimina_byte_nulo_y_controles(self):
        self.assertEqual(texto("a\x00b\x1fc"), "abc")

    def test_conserva_saltos_de_linea(self):
        self.assertEqual(texto("linea1\nlinea2"), "linea1\nlinea2")


if __name__ == "__main__":
    unittest.main()
