"""Componentes reutilizables de las vistas.

[COMPLEMENTO] Archivo agregado para que las tres pantallas CRUD compartan
la misma tabla, los mismos botones y el mismo manejo de mensajes.
"""

import html
from datetime import date, datetime
from urllib.parse import urlencode

import streamlit as st


def escapar(valor):
    """Escapa texto para que se pueda insertar con seguridad en HTML."""
    if valor is None:
        return ""
    return html.escape(str(valor), quote=True)


def url(page, **params):
    """Construye una URL interna, por ejemplo ?page=clientes&accion=editar&id=5."""
    datos = {"page": page}
    datos.update({clave: valor for clave, valor in params.items() if valor is not None})
    return "?" + urlencode(datos)


def param(nombre, defecto=None):
    """Lee un parámetro de la URL.

    Si la app se está ejecutando con parámetros (navegación real), manda la URL.
    Si no hay parámetros, se usa session_state, lo que permite probar las
    pantallas con AppTest.
    """
    if st.query_params:
        return st.query_params.get(nombre, defecto)
    return st.session_state.get(nombre, defecto)


def ir_a(page, **params):
    """Redirige a otra pantalla y limpia los parámetros de la anterior."""
    for clave in ("page", "accion", "id"):
        st.session_state.pop(clave, None)

    st.query_params.clear()
    st.query_params["page"] = page
    for clave, valor in params.items():
        if valor is not None:
            st.query_params[clave] = str(valor)
    st.rerun()


def flash(tipo, mensaje):
    """Guarda un mensaje para mostrarlo después de redirigir."""
    st.session_state["_flash"] = (tipo, mensaje)


def mostrar_flash():
    """Muestra y borra el mensaje pendiente."""
    dato = st.session_state.pop("_flash", None)
    if not dato:
        return
    tipo, mensaje = dato
    if tipo == "success":
        st.success(mensaje)
    elif tipo == "error":
        st.error(mensaje)
    else:
        st.info(mensaje)


def titulo(texto):
    st.markdown(
        f'<h2 class="titulo-pagina">{escapar(texto)}</h2>',
        unsafe_allow_html=True,
    )


def enlace(texto, href, clase="btn btn-secondary"):
    """Devuelve un enlace con apariencia de botón."""
    return (
        f'<a class="{clase}" href="{html.escape(href, quote=True)}" '
        f'target="_self">{escapar(texto)}</a>'
    )


def enlace_menu(texto, page, page_actual):
    """Enlace del menú lateral, resaltando la página actual."""
    clase = "menu-link activo" if page == page_actual else "menu-link"
    st.markdown(
        f'<a class="{clase}" href="{html.escape(url(page), quote=True)}" '
        f'target="_self">{escapar(texto)}</a>',
        unsafe_allow_html=True,
    )


def well_nuevo(texto, page):
    """Caja gris con el botón para crear un registro."""
    st.markdown(
        f'<div class="well">{enlace(texto, url(page, accion="nuevo"), "btn btn-primary")}</div>',
        unsafe_allow_html=True,
    )


def tabla(columnas, filas):
    """Tabla HTML. Cada celda de `filas` ya debe venir escapada o ser HTML seguro."""
    encabezado = "".join(f"<th>{escapar(columna)}</th>" for columna in columnas)
    cuerpo = []
    for fila in filas:
        celdas = "".join(f"<td>{celda}</td>" for celda in fila)
        cuerpo.append(f"<tr>{celdas}</tr>")
    return (
        '<table class="tabla-datos"><thead><tr>'
        f"{encabezado}</tr></thead><tbody>{''.join(cuerpo)}</tbody></table>"
    )


def tabla_detalle(campos):
    """Tabla de dos columnas para mostrar datos sin permitir editarlos."""
    filas = "".join(
        f"<tr><th>{escapar(etiqueta)}</th><td>{escapar(valor)}</td></tr>"
        for etiqueta, valor in campos
    )
    return f'<table class="tabla-detalle">{filas}</table>'


def texto_campo(registro, campo):
    """Devuelve el valor de un campo como texto, convirtiendo None en ''."""
    if not registro:
        return ""
    valor = registro.get(campo)
    return "" if valor is None else str(valor)


def fecha_campo(registro, campo):
    """Devuelve una fecha lista para st.date_input, o None."""
    valor = registro.get(campo) if registro else None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    return None


def formatear_fecha(valor):
    if valor is None:
        return ""
    if isinstance(valor, datetime):
        return valor.strftime("%Y-%m-%d %H:%M")
    if isinstance(valor, date):
        return valor.strftime("%Y-%m-%d")
    return str(valor)


def formatear_dinero(valor):
    if valor is None or valor == "":
        return ""
    return f"{float(valor):,.2f}"


def formatear_activo(valor):
    return "Sí" if valor else "No"
