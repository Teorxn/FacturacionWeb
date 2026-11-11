"""Utilidades compartidas por los controladores.

[COMPLEMENTO] Archivo agregado para no repetir la validación de correo,
la conversión de números y el manejo del error de conexión en los tres
controladores.
"""

import re
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation

from models.db import ErrorBD

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def texto(valor):
    """Convierte None a '' y recorta espacios (equivale al null-coalescing)."""
    if valor is None:
        return ""
    return str(valor).strip()


def email_valido(valor):
    return bool(PATRON_EMAIL.match(texto(valor)))


def es_entero(valor):
    """True si está vacío o si todos sus caracteres son dígitos."""
    valor = texto(valor)
    return valor == "" or valor.isdigit()


def entero_o_none(valor):
    """Convierte a int; vacío o None se guarda como NULL."""
    valor = texto(valor)
    if valor == "":
        return None
    return int(valor)


def decimal_o_none(valor):
    """Convierte a Decimal; vacío o None se guarda como NULL."""
    if valor is None:
        return None
    valor = texto(valor)
    if valor == "":
        return None
    try:
        return Decimal(valor)
    except InvalidOperation:
        return None


def a_datetime(valor):
    """Convierte date a datetime para las columnas DATETIME de MySQL."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, date):
        return datetime.combine(valor, time.min)
    return valor


def fecha_hora_actual():
    return datetime.now()


__all__ = [
    "ErrorBD",
    "PATRON_EMAIL",
    "texto",
    "email_valido",
    "es_entero",
    "entero_o_none",
    "decimal_o_none",
    "a_datetime",
    "fecha_hora_actual",
]
