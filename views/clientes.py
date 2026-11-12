"""Vista de clientes: lista, nuevo, editar y eliminar (CRUD completo)."""

import streamlit as st

from controllers import clientes_controller as ctrl
from controllers.comun import ErrorBD
from views.componentes import (
    enlace,
    flash,
    ir_a,
    mostrar_flash,
    param,
    tabla,
    tabla_detalle,
    texto_campo,
    titulo,
    unir_html,
    url,
    well_nuevo,
)


def render(solo_lectura=False):
    accion = param("accion", "lista")
    id_param = param("id")

    if solo_lectura and accion != "lista":
        st.error(
            "Tu rol solo permite consultar. No puedes crear, editar ni eliminar."
        )
        _lista(solo_lectura=True)
        return

    if accion == "nuevo":
        _formulario()
    elif accion == "editar":
        id_cliente = _leer_id(id_param)
        if id_cliente is None:
            _no_encontrado()
        else:
            _formulario(id_cliente)
    elif accion == "eliminar":
        id_cliente = _leer_id(id_param)
        if id_cliente is None:
            _no_encontrado()
        else:
            _confirmar(id_cliente)
    else:
        _lista(solo_lectura)


def _leer_id(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _no_encontrado():
    st.error("Cliente no encontrado.")
    st.markdown(
        enlace("Volver a la lista", url("clientes"), "btn btn-secondary"),
        unsafe_allow_html=True,
    )


def _lista(solo_lectura=False):
    mostrar_flash()
    titulo("Lista de Clientes")
    if solo_lectura:
        st.info("Modo consulta: tu rol no puede modificar registros.")
    else:
        well_nuevo("NUEVO", "clientes")

    try:
        clientes = ctrl.listar_clientes()
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not clientes:
        st.info("No hay clientes registrados.")
        return

    filas = []
    for cliente in clientes:
        if solo_lectura:
            acciones = ""
        else:
            acciones = unir_html(
                enlace(
                    "Editar",
                    url("clientes", accion="editar", id=cliente["IdCliente"]),
                    "btn btn-info",
                ),
                " ",
                enlace(
                    "Eliminar",
                    url("clientes", accion="eliminar", id=cliente["IdCliente"]),
                    "btn btn-danger",
                ),
            )
        filas.append(
            [
                cliente["IdCliente"],
                cliente.get("StrNombre"),
                cliente.get("NumDocumento"),
                cliente.get("StrTelefono"),
                cliente.get("StrEmail"),
                acciones,
            ]
        )

    st.markdown(
        tabla(
            ["Id", "Nombre", "Documento", "Teléfono", "Email", "Acciones"],
            filas,
        ),
        unsafe_allow_html=True,
    )


def _formulario(id_cliente=None):
    es_edicion = id_cliente is not None
    registro = None

    if es_edicion:
        try:
            registro = ctrl.obtener_cliente(id_cliente)
        except ErrorBD as exc:
            st.error(str(exc))
            return
        if not registro:
            _no_encontrado()
            return

    titulo("Editar Cliente" if es_edicion else "Nuevo Cliente")
    sufijo = str(id_cliente) if es_edicion else "nuevo"

    with st.form(f"form_cliente_{sufijo}"):
        nombre = st.text_input(
            "Nombre",
            value=texto_campo(registro, "StrNombre"),
            max_chars=55,
            key=f"cli_nombre_{sufijo}",
        )
        err_nombre = st.empty()

        documento = st.text_input(
            "Documento",
            value=texto_campo(registro, "NumDocumento"),
            key=f"cli_documento_{sufijo}",
        )
        err_documento = st.empty()

        direccion = st.text_input(
            "Dirección",
            value=texto_campo(registro, "StrDireccion"),
            max_chars=70,
            key=f"cli_direccion_{sufijo}",
        )

        telefono = st.text_input(
            "Teléfono",
            value=texto_campo(registro, "StrTelefono"),
            max_chars=30,
            key=f"cli_telefono_{sufijo}",
        )

        email = st.text_input(
            "Email",
            value=texto_campo(registro, "StrEmail"),
            max_chars=50,
            key=f"cli_email_{sufijo}",
        )
        err_email = st.empty()

        col_guardar, col_cancelar = st.columns(2)
        with col_guardar:
            guardar = st.form_submit_button(
                "Guardar", type="primary", use_container_width=True
            )
        with col_cancelar:
            cancelar = st.form_submit_button(
                "Cancelar", use_container_width=True
            )

    if cancelar:
        ir_a("clientes")

    if guardar:
        datos = {
            "StrNombre": nombre,
            "NumDocumento": documento,
            "StrDireccion": direccion,
            "StrTelefono": telefono,
            "StrEmail": email,
        }
        errores = ctrl.validar_cliente(datos)

        if errores:
            if "StrNombre" in errores:
                err_nombre.error(errores["StrNombre"])
            if "NumDocumento" in errores:
                err_documento.error(errores["NumDocumento"])
            if "StrEmail" in errores:
                err_email.error(errores["StrEmail"])
        else:
            ok, mensaje = ctrl.guardar_cliente(datos, id_cliente)
            if ok:
                flash("success", mensaje)
                ir_a("clientes")
            else:
                st.error(mensaje)


def _confirmar(id_cliente):
    try:
        registro = ctrl.obtener_cliente(id_cliente)
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not registro:
        _no_encontrado()
        return

    titulo("Eliminar Cliente")
    st.markdown(
        '<div class="aviso-eliminar">¿Está seguro de que desea eliminar '
        "este cliente?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        tabla_detalle(
            [
                ("Nombre", texto_campo(registro, "StrNombre")),
                ("Documento", texto_campo(registro, "NumDocumento")),
                ("Dirección", texto_campo(registro, "StrDireccion")),
                ("Teléfono", texto_campo(registro, "StrTelefono")),
                ("Email", texto_campo(registro, "StrEmail")),
            ]
        ),
        unsafe_allow_html=True,
    )

    col_eliminar, col_cancelar = st.columns(2)
    with col_eliminar:
        st.markdown('<span class="marca-peligro"></span>', unsafe_allow_html=True)
        eliminar = st.button(
            "Eliminar",
            type="primary",
            use_container_width=True,
            key=f"eliminar_cliente_{id_cliente}",
        )
    with col_cancelar:
        st.markdown(
            enlace("Cancelar", url("clientes"), "btn btn-secondary"),
            unsafe_allow_html=True,
        )

    if eliminar:
        ok, mensaje = ctrl.eliminar_cliente(id_cliente)
        if ok:
            flash("success", mensaje)
            ir_a("clientes")
        else:
            st.error(mensaje)
