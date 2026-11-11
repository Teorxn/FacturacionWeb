"""Vista de empleados: lista, nuevo, editar y eliminar (CRUD completo)."""

import streamlit as st

from controllers import empleados_controller as ctrl
from controllers.comun import ErrorBD
from views.componentes import (
    enlace,
    escapar,
    fecha_campo,
    flash,
    formatear_fecha,
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
        id_empleado = _leer_id(id_param)
        if id_empleado is None:
            _no_encontrado()
        else:
            _formulario(id_empleado)
    elif accion == "eliminar":
        id_empleado = _leer_id(id_param)
        if id_empleado is None:
            _no_encontrado()
        else:
            _confirmar(id_empleado)
    else:
        _lista()


def _leer_id(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _no_encontrado():
    st.error("Empleado no encontrado.")
    st.markdown(
        enlace("Volver a la lista", url("empleados"), "btn btn-secondary"),
        unsafe_allow_html=True,
    )


def _lista():
    mostrar_flash()
    titulo("ADMON EMPLEADOS")
    well_nuevo("+Nuevo", "empleados")

    try:
        empleados = ctrl.listar_empleados()
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not empleados:
        st.info("No hay empleados registrados.")
        return

    filas = []
    for empleado in empleados:
        acciones = (
            enlace(
                "Editar",
                url("empleados", accion="editar", id=empleado["IdEmpleado"]),
                "btn btn-info",
            )
            + " "
            + enlace(
                "Borrar",
                url("empleados", accion="eliminar", id=empleado["IdEmpleado"]),
                "btn btn-danger",
            )
        )
        filas.append(
            [
                escapar(empleado.get("strNombre")),
                escapar(empleado.get("NumDocumento")),
                escapar(empleado.get("StrTelefono")),
                escapar(empleado.get("StrEmail")),
                acciones,
            ]
        )

    st.markdown(
        tabla(
            ["Nombre", "Documento", "Telefono", "Correo", "ACCIONES"],
            filas,
        ),
        unsafe_allow_html=True,
    )


def _formulario(id_empleado=None):
    es_edicion = id_empleado is not None
    registro = None

    if es_edicion:
        try:
            registro = ctrl.obtener_empleado(id_empleado)
        except ErrorBD as exc:
            st.error(str(exc))
            return
        if not registro:
            _no_encontrado()
            return

    try:
        roles = ctrl.listar_roles()
    except ErrorBD as exc:
        st.error(str(exc))
        return

    titulo("Editar" if es_edicion else "Ingreso Empleado")
    sufijo = str(id_empleado) if es_edicion else "nuevo"

    roles_por_id = {
        rol["IdRolEmpleado"]: rol["StrDescripcion"] for rol in roles
    }
    opciones_rol = [None] + list(roles_por_id.keys())
    rol_actual = registro.get("IdRolEmpleado") if registro else None
    indice_rol = opciones_rol.index(rol_actual) if rol_actual in opciones_rol else 0

    def etiqueta_rol(valor):
        if valor is None:
            return "(Sin rol)"
        return roles_por_id.get(valor) or f"Rol {valor}"

    with st.form(f"form_empleado_{sufijo}"):
        nombre = st.text_input(
            "Nombre",
            value=texto_campo(registro, "strNombre"),
            max_chars=50,
            key=f"emp_nombre_{sufijo}",
        )
        err_nombre = st.empty()

        documento = st.text_input(
            "Nro Documento",
            value=texto_campo(registro, "NumDocumento"),
            key=f"emp_documento_{sufijo}",
        )
        err_documento = st.empty()

        direccion = st.text_input(
            "Direccion",
            value=texto_campo(registro, "StrDireccion"),
            max_chars=100,
            key=f"emp_direccion_{sufijo}",
        )

        telefono = st.text_input(
            "Telefono",
            value=texto_campo(registro, "StrTelefono"),
            max_chars=50,
            key=f"emp_telefono_{sufijo}",
        )

        correo = st.text_input(
            "Correo",
            value=texto_campo(registro, "StrEmail"),
            max_chars=50,
            key=f"emp_correo_{sufijo}",
        )
        err_correo = st.empty()

        rol = st.selectbox(
            "ROL",
            options=opciones_rol,
            index=indice_rol,
            format_func=etiqueta_rol,
            key=f"emp_rol_{sufijo}",
        )

        fecha_ingreso = st.date_input(
            "Fecha Ingreso",
            value=fecha_campo(registro, "DtmIngreso"),
            format="YYYY-MM-DD",
            key=f"emp_ingreso_{sufijo}",
        )

        fecha_retiro = st.date_input(
            "Fecha retiro",
            value=fecha_campo(registro, "DtmRetiro"),
            format="YYYY-MM-DD",
            key=f"emp_retiro_{sufijo}",
        )

        datos_adicionales = st.text_area(
            "Datos adicionales",
            value=texto_campo(registro, "strDatosAdicionales"),
            key=f"emp_datos_{sufijo}",
        )

        col_guardar, col_retornar = st.columns(2)
        with col_guardar:
            guardar = st.form_submit_button(
                "Guardar", type="primary", use_container_width=True
            )
        with col_retornar:
            retornar = st.form_submit_button(
                "Retornar", use_container_width=True
            )

    if retornar:
        ir_a("empleados")

    if guardar:
        datos = {
            "strNombre": nombre,
            "NumDocumento": documento,
            "StrDireccion": direccion,
            "StrTelefono": telefono,
            "StrEmail": correo,
            "IdRolEmpleado": rol,
            "DtmIngreso": fecha_ingreso,
            "DtmRetiro": fecha_retiro,
            "strDatosAdicionales": datos_adicionales,
        }
        errores = ctrl.validar_empleado(datos)

        if errores:
            if "strNombre" in errores:
                err_nombre.error(errores["strNombre"])
            if "NumDocumento" in errores:
                err_documento.error(errores["NumDocumento"])
            if "StrEmail" in errores:
                err_correo.error(errores["StrEmail"])
        else:
            ok, mensaje = ctrl.guardar_empleado(datos, id_empleado)
            if ok:
                flash("success", mensaje)
                ir_a("empleados")
            else:
                st.error(mensaje)


def _confirmar(id_empleado):
    try:
        registro = ctrl.obtener_empleado(id_empleado)
    except ErrorBD as exc:
        st.error(str(exc))
        return

    if not registro:
        _no_encontrado()
        return

    titulo("Eliminar Empleado")
    st.markdown(
        '<div class="aviso-eliminar">¿Está seguro de que desea eliminar '
        "este empleado?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        tabla_detalle(
            [
                ("Nombre", texto_campo(registro, "strNombre")),
                ("Documento", texto_campo(registro, "NumDocumento")),
                ("Dirección", texto_campo(registro, "StrDireccion")),
                ("Teléfono", texto_campo(registro, "StrTelefono")),
                ("Correo", texto_campo(registro, "StrEmail")),
                ("Rol", texto_campo(registro, "StrDescripcionRol")),
                ("Fecha Ingreso", formatear_fecha(registro.get("DtmIngreso"))),
                ("Fecha retiro", formatear_fecha(registro.get("DtmRetiro"))),
                (
                    "Datos adicionales",
                    texto_campo(registro, "strDatosAdicionales"),
                ),
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
            key=f"eliminar_empleado_{id_empleado}",
        )
    with col_cancelar:
        st.markdown(
            enlace("Cancelar", url("empleados"), "btn btn-secondary"),
            unsafe_allow_html=True,
        )

    if eliminar:
        ok, mensaje = ctrl.eliminar_empleado(id_empleado)
        if ok:
            flash("success", mensaje)
            ir_a("empleados")
        else:
            st.error(mensaje)
