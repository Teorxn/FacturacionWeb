"""Controlador de empleados: valida, normaliza y llama al modelo."""

import mysql.connector

from config import USUARIO_EMPLEADO
from controllers.comun import (
    ErrorBD,
    a_datetime,
    email_valido,
    entero_o_none,
    fecha_hora_actual,
    texto,
)
from models import empleado, rol


def listar_empleados():
    try:
        return empleado.listar()
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar la lista de empleados.") from exc


def obtener_empleado(id_empleado):
    try:
        return empleado.obtener(id_empleado)
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar el empleado.") from exc


def listar_roles():
    try:
        return rol.listar()
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudieron consultar los roles.") from exc


def validar_empleado(datos):
    """Validación del lado del servidor. Devuelve un diccionario de errores."""
    errores = {}

    if texto(datos.get("strNombre")) == "":
        errores["strNombre"] = "El nombre es obligatorio."

    documento = texto(datos.get("NumDocumento"))
    if documento == "":
        errores["NumDocumento"] = "El documento es obligatorio."
    elif not documento.isdigit():
        errores["NumDocumento"] = "El documento debe ser numérico."

    correo = texto(datos.get("StrEmail"))
    if correo and not email_valido(correo):
        errores["StrEmail"] = "El correo no tiene un formato válido."

    return errores


def _normalizar(datos):
    return {
        "strNombre": texto(datos.get("strNombre")),
        "NumDocumento": entero_o_none(datos.get("NumDocumento")),
        "StrDireccion": texto(datos.get("StrDireccion")),
        "StrTelefono": texto(datos.get("StrTelefono")),
        "StrEmail": texto(datos.get("StrEmail")),
        "IdRolEmpleado": entero_o_none(datos.get("IdRolEmpleado")),
        "DtmIngreso": a_datetime(datos.get("DtmIngreso")),
        "DtmRetiro": a_datetime(datos.get("DtmRetiro")),
        "strDatosAdicionales": texto(datos.get("strDatosAdicionales")),
        "DtmFechaModifica": fecha_hora_actual(),
        "StrUsuarioModifico": USUARIO_EMPLEADO,
    }


def guardar_empleado(datos, id_empleado=None):
    """Inserta o actualiza. Devuelve (ok, mensaje)."""
    if validar_empleado(datos):
        return False, "Revisa los datos del formulario."

    datos_bd = _normalizar(datos)

    try:
        if id_empleado is None:
            empleado.insertar(datos_bd)
            return True, "Empleado creado correctamente."

        filas = empleado.actualizar(id_empleado, datos_bd)
        if filas == 0:
            return False, "Empleado no encontrado."
        return True, "Empleado actualizado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se pudo guardar el empleado porque los datos no cumplen "
            "una regla de la base de datos."
        )
    except mysql.connector.Error:
        return False, "No se pudo guardar el empleado. Revisa la conexión a la base de datos."


def eliminar_empleado(id_empleado):
    """Elimina por id. Devuelve (ok, mensaje)."""
    try:
        filas = empleado.eliminar(id_empleado)
        if filas == 0:
            return False, "Empleado no encontrado."
        return True, "Empleado eliminado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se puede eliminar este empleado porque está ligado a una "
            "factura o a un registro de seguridad."
        )
    except mysql.connector.Error:
        return False, "No se pudo eliminar el empleado. Revisa la conexión a la base de datos."
