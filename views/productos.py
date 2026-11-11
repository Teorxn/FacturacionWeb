"""Vista de productos: lista, nuevo, editar y eliminar (CRUD completo).

Se usan las columnas reales de TBLPRODUCTOS verificadas con DESCRIBE.
"""

import streamlit as st

from controllers import productos_controller as ctrl
from controllers.comun import ErrorBD
from views.componentes import (
    enlace,
    escapar,
    flash,
    formatear_activo,
    formatear_dinero,
    ir_a,
    mostrar_flash,
    param,
    tabla,
    tabla_detalle,
    texto_campo,
    titulo,
    url,
    well_nuevo,
)


def render():
    accion = param("accion", "lista")
    id_param = param("id")

    if accion == "nuevo":
        _formulario()
    elif accion == "editar":
        id_producto = _leer_id(id_param)
        if id_producto is None:
            _no_encontrado()
        else:
            _formulario(id_producto)
    elif accion == "eliminar":
        id_producto = _leer_id(id_param)
        if id_producto is None:
            _no_encontrado()
        else:
            _confirmar(id_producto)
    else:
        _lista()


def _leer_id(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _no_encontrado():
    st.error("Producto no encontrado.")
    st.markdown(
        enlace("Volver a la lista", url("productos"), "btn btn-secondary"),
        unsafe_allow_html=True,
    )


def _lista():
    mostrar_flash()
    titulo("Lista de Productos")
    well_nuevo("NUEVO", "productos")

    try:
        productos = ctrl.listar_productos()
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not productos:
        st.info("No hay productos registrados.")
        return

    filas = []
    for producto in productos:
        acciones = (
            enlace(
                "Editar",
                url("productos", accion="editar", id=producto["IdProducto"]),
                "btn btn-info",
            )
            + " "
            + enlace(
                "Eliminar",
                url("productos", accion="eliminar", id=producto["IdProducto"]),
                "btn btn-danger",
            )
        )
        filas.append(
            [
                escapar(producto["IdProducto"]),
                escapar(producto.get("StrNombreProducto")),
                escapar(producto.get("StrCategoria")),
                formatear_dinero(producto.get("NumPrecio")),
                escapar(producto.get("NumStock")),
                formatear_activo(producto.get("BitActivo")),
                acciones,
            ]
        )

    st.markdown(
        tabla(
            ["Id", "Nombre", "Categoría", "Precio", "Stock", "Activo", "Acciones"],
            filas,
        ),
        unsafe_allow_html=True,
    )


def _formulario(id_producto=None):
    es_edicion = id_producto is not None
    registro = None

    if es_edicion:
        try:
            registro = ctrl.obtener_producto(id_producto)
        except ErrorBD as exc:
            st.error(str(exc))
            return
        if not registro:
            _no_encontrado()
            return

    titulo("Editar Producto" if es_edicion else "Nuevo Producto")
    sufijo = str(id_producto) if es_edicion else "nuevo"

    # None deja el campo vacío y permite guardar NULL, porque la columna
    # admite nulos. Si el registro ya tiene valor, se prellena.
    precio_inicial = None
    if registro and registro.get("NumPrecio") is not None:
        precio_inicial = float(registro["NumPrecio"])

    stock_inicial = None
    if registro and registro.get("NumStock") is not None:
        stock_inicial = int(registro["NumStock"])

    activo_inicial = True
    if registro:
        activo_inicial = bool(registro.get("BitActivo"))

    with st.form(f"form_producto_{sufijo}"):
        nombre = st.text_input(
            "Nombre",
            value=texto_campo(registro, "StrNombreProducto"),
            max_chars=200,
            key=f"pro_nombre_{sufijo}",
        )
        err_nombre = st.empty()

        descripcion = st.text_area(
            "Descripción",
            value=texto_campo(registro, "StrDescripcion"),
            key=f"pro_descripcion_{sufijo}",
        )

        precio = st.number_input(
            "Precio",
            min_value=0.0,
            value=precio_inicial,
            step=0.01,
            format="%.2f",
            placeholder="Opcional",
            key=f"pro_precio_{sufijo}",
        )
        err_precio = st.empty()

        stock = st.number_input(
            "Stock",
            min_value=0,
            value=stock_inicial,
            step=1,
            placeholder="Opcional",
            key=f"pro_stock_{sufijo}",
        )
        err_stock = st.empty()

        categoria = st.text_input(
            "Categoría",
            value=texto_campo(registro, "StrCategoria"),
            max_chars=100,
            key=f"pro_categoria_{sufijo}",
        )

        activo = st.checkbox(
            "Activo",
            value=activo_inicial,
            key=f"pro_activo_{sufijo}",
        )

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
        ir_a("productos")

    if guardar:
        datos = {
            "StrNombreProducto": nombre,
            "StrDescripcion": descripcion,
            "NumPrecio": precio,
            "NumStock": stock,
            "StrCategoria": categoria,
            "BitActivo": activo,
        }
        errores = ctrl.validar_producto(datos)

        if errores:
            if "StrNombreProducto" in errores:
                err_nombre.error(errores["StrNombreProducto"])
            if "NumPrecio" in errores:
                err_precio.error(errores["NumPrecio"])
            if "NumStock" in errores:
                err_stock.error(errores["NumStock"])
        else:
            ok, mensaje = ctrl.guardar_producto(datos, id_producto)
            if ok:
                flash("success", mensaje)
                ir_a("productos")
            else:
                st.error(mensaje)


def _confirmar(id_producto):
    try:
        registro = ctrl.obtener_producto(id_producto)
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not registro:
        _no_encontrado()
        return

    titulo("Eliminar Producto")
    st.markdown(
        '<div class="aviso-eliminar">¿Está seguro de que desea eliminar '
        "este producto?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        tabla_detalle(
            [
                ("Nombre", texto_campo(registro, "StrNombreProducto")),
                ("Descripción", texto_campo(registro, "StrDescripcion")),
                ("Precio", formatear_dinero(registro.get("NumPrecio"))),
                ("Stock", texto_campo(registro, "NumStock")),
                ("Categoría", texto_campo(registro, "StrCategoria")),
                ("Activo", formatear_activo(registro.get("BitActivo"))),
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
            key=f"eliminar_producto_{id_producto}",
        )
    with col_cancelar:
        st.markdown(
            enlace("Cancelar", url("productos"), "btn btn-secondary"),
            unsafe_allow_html=True,
        )

    if eliminar:
        ok, mensaje = ctrl.eliminar_producto(id_producto)
        if ok:
            flash("success", mensaje)
            ir_a("productos")
        else:
            st.error(mensaje)
