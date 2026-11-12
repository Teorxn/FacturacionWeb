"""Usuarios del login definidos en .streamlit/secrets.toml.

No se guardan contraseñas en texto plano: solo hashes PBKDF2-HMAC-SHA256
con sal aleatoria. Al no crear tablas nuevas, no se modifica la base de
datos compartida del profesor.

Formato del hash:
    pbkdf2_sha256$<iteraciones>$<sal_base64>$<hash_base64>
"""

import base64
import binascii
import hashlib
import hmac
import secrets as _secrets
from functools import lru_cache

import streamlit as st

ALGORITMO_HASH = "pbkdf2_sha256"
ITERACIONES = 600_000
ITERACIONES_MINIMAS = 100_000


class ErrorAuth(Exception):
    """Error controlado de configuración de autenticación."""


def cargar_config():
    """Devuelve la sección [auth] de secrets.toml."""
    try:
        return st.secrets["auth"]
    except Exception as exc:
        raise ErrorAuth(
            "Falta la sección [auth] en .streamlit/secrets.toml. "
            "Ejecuta: python configurar_auth.py init"
        ) from exc


def _b64(datos):
    return base64.b64encode(datos).decode("ascii")


def generar_hash(password, iteraciones=ITERACIONES):
    """Genera un hash seguro para guardar en secrets.toml."""
    if not password:
        raise ValueError("La contraseña no puede estar vacía.")
    iteraciones = int(iteraciones)
    if iteraciones < ITERACIONES_MINIMAS:
        raise ValueError("Se requieren al menos 100000 iteraciones.")
    sal = _secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", str(password).encode("utf-8"), sal, iteraciones
    )
    return f"{ALGORITMO_HASH}${iteraciones}${_b64(sal)}${_b64(digest)}"


def verificar_hash(password, almacenado):
    """Compara una contraseña con el hash guardado en tiempo constante."""
    try:
        algoritmo, iteraciones, sal_b64, hash_b64 = str(almacenado).split("$", 3)
        if algoritmo != ALGORITMO_HASH:
            return False
        iteraciones = int(iteraciones)
        if iteraciones < ITERACIONES_MINIMAS:
            return False
        sal = base64.b64decode(sal_b64, validate=True)
        esperado = base64.b64decode(hash_b64, validate=True)
        calculado = hashlib.pbkdf2_hmac(
            "sha256", str(password).encode("utf-8"), sal, iteraciones
        )
        return hmac.compare_digest(calculado, esperado)
    except (ValueError, TypeError, binascii.Error):
        return False


@lru_cache(maxsize=1)
def _hash_ficticio():
    """Hash de relleno para igualar tiempos cuando el usuario no existe."""
    return generar_hash("contrasena-ficticia-para-igualar-tiempos")


def normalizar_usuario(valor):
    """Los nombres de usuario se comparan sin espacios ni mayúsculas."""
    return str(valor or "").strip().lower()


def listar_usuarios(config=None):
    """Devuelve {usuario: datos} a partir de [auth.users.*]."""
    cfg = cargar_config() if config is None else config
    usuarios = cfg.get("users") or {}
    salida = {}

    for clave, datos in usuarios.items():
        nombre = normalizar_usuario(clave)
        if not nombre:
            continue
        datos = datos or {}
        salida[nombre] = {
            "usuario": nombre,
            "nombre": str(datos.get("nombre") or nombre),
            "rol": normalizar_usuario(datos.get("rol") or "consulta"),
            "activo": bool(datos.get("activo", True)),
            "password_hash": str(datos.get("password_hash") or ""),
        }

    return salida


def obtener_usuario(nombre, config=None):
    """Busca un usuario por nombre normalizado."""
    return listar_usuarios(config).get(normalizar_usuario(nombre))


def autenticar(nombre, password, config=None):
    """Devuelve el usuario si las credenciales son correctas, o None.

    Siempre se calcula un hash (real o ficticio) para no revelar por el
    tiempo de respuesta si un usuario existe o está activo.
    """
    usuario = obtener_usuario(nombre, config)
    password = str(password or "")

    if usuario is None or not usuario["activo"]:
        verificar_hash(password, _hash_ficticio())
        return None

    if not verificar_hash(password, usuario["password_hash"]):
        return None

    return usuario


__all__ = [
    "ErrorAuth",
    "ALGORITMO_HASH",
    "ITERACIONES",
    "cargar_config",
    "generar_hash",
    "verificar_hash",
    "normalizar_usuario",
    "listar_usuarios",
    "obtener_usuario",
    "autenticar",
]
