"""Aplicación FACTURACION - entrada, layout general y navegación.

El flujo MVC se ve así:
usuario -> app.py (navegación) -> vista -> controlador -> modelo -> MySQL

La autenticación se valida en cada recarga antes de dibujar cualquier
pantalla. Ocultar un enlace del menú no es suficiente: el permiso se
comprueba también en el servidor.
"""

import streamlit as st

import config
from controllers import auth_controller as auth
from views import (
    acerca,
    ayuda,
    clientes,
    contacto,
    empleados,
    en_construccion,
    inicio,
    login,
    productos,
    seguridad,
)
from views.componentes import enlace_menu, escapar, ir_a, param
from views.estilos import CSS

PAGINAS = {
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
}

NO_FUNCIONALES = {
    "categorias": "Categorias",
    "facturas": "facturas",
    "informes": "Informes",
    "roles": "Roles",
}


def _topbar(page, sesion):
    def link(texto, destino):
        clase = "activo" if page == destino else ""
        return (
            f'<a class="{clase}" href="?page={destino}" '
            f'target="_self">{texto}</a>'
        )

    nombre = escapar(sesion.get("nombre") or sesion.get("sub"))
    rol = escapar(sesion.get("rol"))

    return f"""
    <div class="topbar">
        <div class="marca">{escapar(config.APP_NOMBRE)}</div>
        <div class="enlaces">
            {link("Inicio", "inicio")}
            {link("Acerca", "acerca")}
            {link("Ayuda", "ayuda")}
            {link("Contacto", "contacto")}
            <span class="usuario" title="Sesión activa">{nombre} · {rol}</span>
        </div>
    </div>
    """


def _sidebar(page, rol):
    with st.sidebar:
        st.markdown(
            f'<div class="marca-sidebar">{escapar(config.APP_NOMBRE)}</div>',
            unsafe_allow_html=True,
        )

        if auth.tiene_permiso(rol, "clientes") or auth.tiene_permiso(
            rol, "productos"
        ):
            with st.expander("TABLAS", expanded=True):
                if auth.tiene_permiso(rol, "clientes"):
                    enlace_menu("Clientes", "clientes", page)
                if auth.tiene_permiso(rol, "productos"):
                    enlace_menu("Productos", "productos", page)
                if auth.tiene_permiso(rol, "categorias"):
                    enlace_menu("Categorias", "categorias", page)

        if auth.tiene_permiso(rol, "facturas") or auth.tiene_permiso(
            rol, "informes"
        ):
            with st.expander("FACTURAS", expanded=True):
                if auth.tiene_permiso(rol, "facturas"):
                    enlace_menu("facturas", "facturas", page)
                if auth.tiene_permiso(rol, "informes"):
                    enlace_menu("Informes", "informes", page)

        if (
            auth.tiene_permiso(rol, "empleados")
            or auth.tiene_permiso(rol, "roles")
            or auth.tiene_permiso(rol, "seguridad")
        ):
            with st.expander("SEGURIDAD", expanded=True):
                if auth.tiene_permiso(rol, "empleados"):
                    enlace_menu("Empleados", "empleados", page)
                if auth.tiene_permiso(rol, "roles"):
                    enlace_menu("Roles", "roles", page)
                if auth.tiene_permiso(rol, "seguridad"):
                    enlace_menu("Seguridad", "seguridad", page)

        st.markdown('<div class="separador-sidebar"></div>', unsafe_allow_html=True)
        if st.button("Cerrar sesión", use_container_width=True, key="btn_logout"):
            auth.cerrar_sesion()
            ir_a("inicio")


def _contenido(page, sesion):
    rol = sesion.get("rol")
    solo_lectura = not auth.puede_escribir(rol)

    if page == "inicio":
        inicio.render()
    elif page == "acerca":
        acerca.render()
    elif page == "ayuda":
        ayuda.render()
    elif page == "contacto":
        contacto.render()
    elif page == "clientes":
        clientes.render(solo_lectura=solo_lectura)
    elif page == "productos":
        productos.render(solo_lectura=solo_lectura)
    elif page == "empleados":
        empleados.render(solo_lectura=solo_lectura)
    elif page == "seguridad":
        seguridad.render(sesion)
    else:
        en_construccion.render(NO_FUNCIONALES.get(page, page))


def _footer():
    st.markdown(
        f'<div class="footer">{escapar(config.FOOTER_TEXTO)}</div>',
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title=config.APP_NOMBRE,
        page_icon="🧾",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)

    page = param("page", "inicio")
    if page not in PAGINAS:
        page = "inicio"

    sesion = auth.sesion_actual()

    if sesion is None:
        login.render(page)
        _footer()
        return

    if not auth.tiene_permiso(sesion.get("rol"), page):
        _topbar(page, sesion)
        _sidebar(page, sesion.get("rol"))
        st.error("No tienes permiso para ver esta sección.")
        _footer()
        return

    _topbar(page, sesion)
    _sidebar(page, sesion.get("rol"))
    _contenido(page, sesion)
    _footer()


main()
