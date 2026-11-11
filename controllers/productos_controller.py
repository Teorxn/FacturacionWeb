"""Controlador de productos: valida, normaliza y llama al modelo."""

import mysql.connector

from config import USUARIO_PRODUCTO
from controllers.comun import (
    ErrorBD,
    decimal_o_none,
    entero_o_none,
    fecha_hora_actual,
    texto,
)
from models import producto


def listar_productos():
    try:
        return producto.listar()
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar la lista de productos.") from exc


def obtener_producto(id_producto):
    try:
        return producto.obtener(id_producto)
    except ErrorBD:
        raise
    except mysql.connector.Error as exc:
        raise ErrorBD("No se pudo consultar el producto.") from exc


def validar_producto(datos):
    """Validación del lado del servidor. Devuelve un diccionario de errores."""
    errores = {}

    if texto(datos.get("StrNombreProducto")) == "":
        errores["StrNombreProducto"] = "El nombre es obligatorio."

    precio = datos.get("NumPrecio")
    if precio not in (None, ""):
        try:
            if float(precio) < 0:
                errores["NumPrecio"] = "El precio no puede ser negativo."
        except (TypeError, ValueError):
            errores["NumPrecio"] = "El precio debe ser un número válido."

    stock = datos.get("NumStock")
    if stock not in (None, ""):
        try:
            if int(stock) < 0:
                errores["NumStock"] = "El stock no puede ser negativo."
        except (TypeError, ValueError):
            errores["NumStock"] = "El stock debe ser un número entero."

    return errores


def _normalizar(datos):
    return {
        "StrNombreProducto": texto(datos.get("StrNombreProducto")),
        "StrDescripcion": texto(datos.get("StrDescripcion")),
        "NumPrecio": decimal_o_none(datos.get("NumPrecio")),
        "NumStock": entero_o_none(datos.get("NumStock")),
        "StrCategoria": texto(datos.get("StrCategoria")),
        "BitActivo": 1 if datos.get("BitActivo") else 0,
        "DtmFechaModifica": fecha_hora_actual(),
        "StrUsuarioModifica": USUARIO_PRODUCTO,
    }


def guardar_producto(datos, id_producto=None):
    """Inserta o actualiza. Devuelve (ok, mensaje)."""
    if validar_producto(datos):
        return False, "Revisa los datos del formulario."

    datos_bd = _normalizar(datos)

    try:
        if id_producto is None:
            producto.insertar(datos_bd)
            return True, "Producto creado correctamente."

        filas = producto.actualizar(id_producto, datos_bd)
        if filas == 0:
            return False, "Producto no encontrado."
        return True, "Producto actualizado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se pudo guardar el producto porque los datos no cumplen "
            "una regla de la base de datos."
        )
    except mysql.connector.Error:
        return False, "No se pudo guardar el producto. Revisa la conexión a la base de datos."


def eliminar_producto(id_producto):
    """Elimina por id. Devuelve (ok, mensaje)."""
    try:
        filas = producto.eliminar(id_producto)
        if filas == 0:
            return False, "Producto no encontrado."
        return True, "Producto eliminado correctamente."
    except ErrorBD as exc:
        return False, str(exc)
    except mysql.connector.IntegrityError:
        return False, (
            "No se puede eliminar este producto porque está ligado a otros registros."
        )
    except mysql.connector.Error:
        return False, "No se pudo eliminar el producto. Revisa la conexión a la base de datos."
