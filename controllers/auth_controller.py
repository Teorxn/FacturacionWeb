"""Autenticación con JWT, control de intentos y permisos por rol.

El token se firma con HS256 y se guarda en st.session_state. No se expone
en la URL ni en una cookie legible por JavaScript. La sesión se valida en
cada recarga de la aplicación, no solo al mostrar el menú.
"""

import secrets
import threading
import time
from datetime import datetime, timedelta, timezone

import jwt
import streamlit as st

from models import usuario as modelo_usuario
from models.usuario import ErrorAuth

ALGORITMO = "HS256"
ISSUER_POR_DEFECTO = "facturacion-streamlit"
TOKEN_MINUTOS_POR_DEFECTO = 30
MAX_INTENTOS_POR_DEFECTO = 5
BLOQUEO_MINUTOS_POR_DEFECTO = 5
LONGITUD_MINIMA_SECRETO = 32

# Permisos por rol. Se comprueban en app.py antes de dibujar cada pantalla.
PERMISOS = {
    "admin": {
        "inicio",
        "acerca",
        "ayuda",
        "contacto",
        "clientes",
        "productos",
        "categorias",
        "facturas",
        "informes",
        "empleados",
        "roles",
        "seguridad",
    },
    "vendedor": {
        "inicio",
        "acerca",
        "ayuda",
        "contacto",
        "clientes",
        "productos",
        "categorias",
        "facturas",
        "informes",
    },
    "consulta": {
        "inicio",
        "acerca",
        "ayuda",
        "contacto",
        "clientes",
        "productos",
        "informes",
    },
}

# Intentos fallidos por usuario. Es memoria del proceso: sirve para frenar
# fuerza bruta en un servidor pequeño. En producción conviene Redis.
_INTENTOS = {}
_CANDADO = threading.Lock()


def _config(config=None):
    return modelo_usuario.cargar_config() if config is None else config


def _entero(cfg, clave, defecto):
    try:
        return max(1, int(cfg.get(clave, defecto)))
    except (TypeError, ValueError):
        return defecto


def _secreto(cfg):
    secreto = str(cfg.get("jwt_secret") or "")
    if len(secreto) < LONGITUD_MINIMA_SECRETO:
        raise ErrorAuth(
            "El jwt_secret de [auth] debe tener al menos 32 caracteres. "
            "Ejecuta: python configurar_auth.py init"
        )
    return secreto


def _issuer(cfg):
    return str(cfg.get("issuer") or ISSUER_POR_DEFECTO)


def _ahora():
    return datetime.now(timezone.utc)


def crear_token(usuario, config=None, ahora=None):
    """Crea un JWT firmado para un usuario ya autenticado."""
    cfg = _config(config)
    secreto = _secreto(cfg)
    ahora = ahora or _ahora()
    minutos = _entero(cfg, "token_minutos", TOKEN_MINUTOS_POR_DEFECTO)

    payload = {
        "sub": usuario["usuario"],
        "nombre": usuario.get("nombre") or usuario["usuario"],
        "rol": usuario.get("rol") or "consulta",
        "iss": _issuer(cfg),
        "iat": ahora,
        "nbf": ahora,
        "exp": ahora + timedelta(minutes=minutos),
        "jti": secrets.token_urlsafe(16),
    }
    return jwt.encode(payload, secreto, algorithm=ALGORITMO)


def validar_token(token, config=None):
    """Valida firma, expiración, emisor y campos obligatorios."""
    if not token:
        return None

    cfg = _config(config)
    secreto = _secreto(cfg)

    try:
        return jwt.decode(
            token,
            secreto,
            algorithms=[ALGORITMO],
            issuer=_issuer(cfg),
            options={"require": ["exp", "iat", "nbf", "sub", "iss"]},
        )
    except jwt.PyJWTError:
        return None


def sesion_actual():
    """Devuelve el payload del token activo o None si no es válido."""
    token = st.session_state.get("_auth_token")
    if not token:
        return None

    try:
        payload = validar_token(token)
        if payload is None:
            cerrar_sesion()
            return None

        # Si el usuario se eliminó, desactivó o cambió de rol, se invalida.
        cfg = modelo_usuario.cargar_config()
        usuario = modelo_usuario.obtener_usuario(payload.get("sub"), cfg)
        if (
            not usuario
            or not usuario["activo"]
            or usuario["rol"] != payload.get("rol")
        ):
            cerrar_sesion()
            return None
    except ErrorAuth:
        cerrar_sesion()
        return None

    return payload


def _segundos_bloqueo(usuario):
    ahora = time.time()
    with _CANDADO:
        datos = _INTENTOS.get(usuario)
        if not datos:
            return 0
        if datos.get("hasta", 0) > ahora:
            return int(datos["hasta"] - ahora)
        if datos.get("hasta"):
            _INTENTOS.pop(usuario, None)
    return 0


def _registrar_fallo(usuario, cfg):
    maximo = _entero(cfg, "max_intentos", MAX_INTENTOS_POR_DEFECTO)
    minutos = _entero(cfg, "bloqueo_minutos", BLOQUEO_MINUTOS_POR_DEFECTO)

    with _CANDADO:
        datos = _INTENTOS.setdefault(usuario, {"fallos": 0, "hasta": 0})
        datos["fallos"] += 1
        if datos["fallos"] >= maximo:
            datos["hasta"] = time.time() + minutos * 60
            datos["fallos"] = 0


def _limpiar_fallos(usuario):
    with _CANDADO:
        _INTENTOS.pop(usuario, None)


def iniciar_sesion(nombre, password):
    """Valida credenciales y guarda un JWT en la sesión. (ok, mensaje)."""
    nombre = modelo_usuario.normalizar_usuario(nombre)
    password = str(password or "")

    if not nombre or not password:
        return False, "Escribe tu usuario y contraseña."

    segundos = _segundos_bloqueo(nombre)
    if segundos:
        minutos = max(1, (segundos + 59) // 60)
        return False, (
            f"Demasiados intentos fallidos. Intenta de nuevo en {minutos} "
            f"minuto(s)."
        )

    try:
        cfg = modelo_usuario.cargar_config()
        usuario = modelo_usuario.autenticar(nombre, password, cfg)
    except ErrorAuth:
        return False, (
            "El sistema de autenticación no está configurado. "
            "Contacta al administrador."
        )

    if usuario is None:
        _registrar_fallo(nombre, cfg)
        return False, "Usuario o contraseña incorrectos."

    _limpiar_fallos(nombre)

    try:
        token = crear_token(usuario, cfg)
    except ErrorAuth:
        return False, "No se pudo iniciar la sesión. Contacta al administrador."

    st.session_state["_auth_token"] = token
    st.session_state["_auth_usuario"] = usuario["usuario"]
    st.session_state["_auth_ultimo_acceso"] = time.time()
    return True, "Sesión iniciada correctamente."


def cerrar_sesion():
    """Elimina el token y los datos de sesión."""
    for clave in ("_auth_token", "_auth_usuario", "_auth_ultimo_acceso"):
        st.session_state.pop(clave, None)


def renovar_sesion():
    """Emite un token nuevo para el usuario actual. True si lo logró."""
    sesion = sesion_actual()
    if not sesion:
        return False

    try:
        cfg = modelo_usuario.cargar_config()
        usuario = modelo_usuario.obtener_usuario(sesion.get("sub"), cfg)
        if not usuario:
            return False
        st.session_state["_auth_token"] = crear_token(usuario, cfg)
        st.session_state["_auth_ultimo_acceso"] = time.time()
    except ErrorAuth:
        return False

    return True


def tiene_permiso(rol, page):
    """True si el rol puede ver la página indicada."""
    return page in PERMISOS.get(str(rol or ""), set())


def paginas_permitidas(rol):
    """Conjunto de páginas visibles para el rol."""
    return PERMISOS.get(str(rol or ""), set())


def puede_escribir(rol):
    """True si el rol puede crear, editar o eliminar registros."""
    return str(rol or "") in {"admin", "vendedor"}


def puede_administrar(rol):
    """True si el rol puede administrar empleados, roles y seguridad."""
    return str(rol or "") == "admin"


__all__ = [
    "ALGORITMO",
    "PERMISOS",
    "crear_token",
    "validar_token",
    "sesion_actual",
    "iniciar_sesion",
    "cerrar_sesion",
    "renovar_sesion",
    "tiene_permiso",
    "paginas_permitidas",
    "puede_escribir",
    "puede_administrar",
]
