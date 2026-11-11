"""Aplicación FACTURACION - entrada, layout general y navegación.

El flujo MVC se ve así:
usuario -> app.py (navegación) -> vista -> controlador -> modelo -> MySQL
"""

import streamlit as st

import config
from views import (
    acerca,
    ayuda,
    clientes,
    contacto,
    empleados,
    en_construccion,
    inicio,
    productos,
)
from views.componentes import enlace_menu, param
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
    "seguridad": "Seguridad",
}


def _topbar(page):
    def link(texto, destino):
        clase = "activo" if page == destino else ""
        return (
            f'<a class="{clase}" href="?page={destino}" '
            f'target="_self">{texto}</a>'
        )

    return f"""
    <div class="topbar">
        <div class="marca">{config.APP_NOMBRE}</div>
        <div class="enlaces">
            {link("Inicio", "inicio")}
            {link("Acerca", "acerca")}
            {link("Ayuda", "ayuda")}
            {link("Contacto", "contacto")}
            <span class="login">Login</span>
        </div>
    </div>
    """


def _sidebar(page):
    with st.sidebar:
        st.markdown(
            f'<div class="marca-sidebar">{config.APP_NOMBRE}</div>',
            unsafe_allow_html=True,
        )

        with st.expander("TABLAS", expanded=True):
            enlace_menu("Clientes", "clientes", page)
            enlace_menu("Productos", "productos", page)
            enlace_menu("Categorias", "categorias", page)

        with st.expander("FACTURAS", expanded=True):
            enlace_menu("facturas", "facturas", page)
            enlace_menu("Informes", "informes", page)

        with st.expander("SEGURIDAD", expanded=True):
            enlace_menu("Empleados", "empleados", page)
            enlace_menu("Roles", "roles", page)
            enlace_menu("Seguridad", "seguridad", page)


def _contenido(page):
    if page == "inicio":
        inicio.render()
    elif page == "acerca":
        acerca.render()
    elif page == "ayuda":
        ayuda.render()
    elif page == "contacto":
        contacto.render()
    elif page == "clientes":
        clientes.render()
    elif page == "productos":
        productos.render()
    elif page == "empleados":
        empleados.render()
    else:
        en_construccion.render(NO_FUNCIONALES.get(page, page))


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

    st.markdown(_topbar(page), unsafe_allow_html=True)
    _sidebar(page)
    _contenido(page)
    st.markdown(
        f'<div class="footer">{config.FOOTER_TEXTO}</div>',
        unsafe_allow_html=True,
    )


main()
