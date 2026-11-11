"""Pantalla para las entradas del menú que todavía no tienen funcionalidad.

[COMPLEMENTO] El PDF deja Categorias, facturas, Informes, Roles y Seguridad
como entradas sin pantalla. Aquí se muestra un aviso simple para que el
usuario no vea una página en blanco.
"""

import streamlit as st

from views.componentes import titulo


def render(nombre):
    titulo(nombre)
    st.info("En construcción")
