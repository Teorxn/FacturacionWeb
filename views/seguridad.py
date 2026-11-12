"""Pantalla de Seguridad: estado de la sesión y controles aplicados."""

from datetime import datetime, timezone

import streamlit as st

from controllers import auth_controller as auth
from views.componentes import (
    tabla_detalle,
    titulo,
)


def _fecha_local(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).astimezone()
    except (TypeError, ValueError, OSError):
        return None


def _formatear_fecha(valor):
    if valor is None:
        return ""
    return valor.strftime("%Y-%m-%d %H:%M:%S %Z")


def render(sesion):
    """Muestra los datos del JWT activo y las medidas de seguridad."""
    titulo("Seguridad")

    expira = _fecha_local(sesion.get("exp"))
    emitido = _fecha_local(sesion.get("iat"))
    rol = str(sesion.get("rol") or "")
    paginas = sorted(auth.paginas_permitidas(rol))

    st.markdown(
        tabla_detalle(
            [
                ("Usuario", sesion.get("sub")),
                ("Nombre", sesion.get("nombre")),
                ("Rol", rol),
                ("Token", "JWT firmado con HS256"),
                ("Emitido", _formatear_fecha(emitido)),
                ("Expira", _formatear_fecha(expira)),
                ("Identificador (jti)", sesion.get("jti")),
                ("Emisor", sesion.get("iss")),
            ]
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### Accesos de este rol")
    st.write(", ".join(paginas) if paginas else "Sin accesos asignados.")

    with st.expander("Controles de seguridad aplicados", expanded=True):
        st.markdown(
            "- **Inyección SQL:** todas las consultas usan parámetros `%s` y "
            "tuplas; nunca se concatenan datos del usuario.\n"
            "- **XSS:** todo texto que llega a HTML se escapa y las tablas "
            "escapan sus celdas por defecto.\n"
            "- **Contraseñas:** se guardan como hash PBKDF2-HMAC-SHA256 con "
            "sal aleatoria y comparación en tiempo constante.\n"
            "- **JWT:** firma HS256, expiración, emisor, `iat`, `nbf`, `jti` y "
            "validación en cada recarga.\n"
            "- **Fuerza bruta:** bloqueo temporal tras varios intentos "
            "fallidos.\n"
            "- **CSRF:** no hay endpoints propios de escritura; las acciones "
            "pasan por formularios y botones de Streamlit con protección XSRF.\n"
            "- **Secretos:** `secrets.toml` está excluido de Git y del `.zip`."
        )

    col_renovar, col_salir = st.columns(2)
    with col_renovar:
        if st.button("Renovar sesión", use_container_width=True):
            if auth.renovar_sesion():
                st.success("Sesión renovada.")
                st.rerun()
            else:
                st.error("No se pudo renovar la sesión. Vuelve a iniciar sesión.")
    with col_salir:
        if st.button(
            "Cerrar sesión", type="primary", use_container_width=True
        ):
            auth.cerrar_sesion()
            st.rerun()
