"""Controlador de clientes: valida, normaliza y llama al modelo.

El controlador es el "mesero": recibe lo que pide la vista, revisa que los
datos estén bien y solo entonces le pide al modelo que toque la base de datos.
"""

import mysql.connector

from config import USUARIO_CLIENTE
from controllers.comun import (
    ErrorBD,
    email_valido,
    entero_o_none,
    fecha_hora_actual,
    texto,
)
from models import cliente


def listar_clientes():
    try:
        return cliente.listar()
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar la lista de clientes.") from exc


def obtener_cliente(id_cliente):
    try:
        return cliente.obtener(id_cliente)
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar el cliente.") from exc


def validar_cliente(datos):
    """Validación del lado del servidor. Devuelve un diccionario de errores."""
    errores = {}

    if texto(datos.get("StrNombre")) == "":
        errores["StrNombre"] = "El nombre es obligatorio."

    correo = texto(datos.get("StrEmail"))
    if correo and not email_valido(correo):
        errores["StrEmail"] = "El correo no tiene un formato válido."

    documento = texto(datos.get("NumDocumento"))
    if documento and not documento.isdigit():
        errores["NumDocumento"] = "El documento debe ser numérico."

    return errores


def _normalizar(datos):
    """Aplica las reglas de valores del manual antes de insertar/actualizar."""
    return {
        "StrNombre": texto(datos.get("StrNombre")),
        "NumDocumento": entero_o_none(datos.get("NumDocumento")),
        "StrDireccion": texto(datos.get("StrDireccion")),
        "StrTelefono": texto(datos.get("StrTelefono")),
        "StrEmail": texto(datos.get("StrEmail")),
        "DtmFechaModifica": fecha_hora_actual(),
        "StrUsuarioModifica": USUARIO_CLIENTE,
    }


def guardar_cliente(datos, id_cliente=None):
    """Inserta o actualiza. Devuelve (ok, mensaje)."""
    if validar_cliente(datos):
        return False, "Revisa los datos del formulario."

    datos_bd = _normalizar(datos)

    try:
        if id_cliente is None:
            cliente.insertar(datos_bd)
            return True, "Cliente creado correctamente."

        filas = cliente.actualizar(id_cliente, datos_bd)
        if filas == 0:
            return False, "Cliente no encontrado."
        return True, "Cliente actualizado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se pudo guardar el cliente porque los datos no cumplen "
            "una regla de la base de datos."
        )
    except mysql.connector.Error:
        return False, "No se pudo guardar el cliente. Revisa la conexión a la base de datos."


def eliminar_cliente(id_cliente):
    """Elimina por id. Devuelve (ok, mensaje)."""
    try:
        filas = cliente.eliminar(id_cliente)
        if filas == 0:
            return False, "Cliente no encontrado."
        return True, "Cliente eliminado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se puede eliminar este cliente porque tiene facturas asociadas."
        )
    except mysql.connector.Error:
        return False, "No se pudo eliminar el cliente. Revisa la conexión a la base de datos."
