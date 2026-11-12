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

# Se eliminan caracteres de control (incluido el byte nulo) para evitar
# entradas raras que luego se muestren en HTML o lleguen al driver de MySQL.
CARACTERES_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def texto(valor):
    """Convierte None a '' y recorta espacios (equivale al null-coalescing)."""
    if valor is None:
        return ""
    limpio = CARACTERES_CONTROL.sub("", str(valor))
    return limpio.strip()


def demasiado_largo(valor, maximo):
    """True si el texto supera el largo permitido por la columna."""
    return len(texto(valor)) > int(maximo)


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
    "CARACTERES_CONTROL",
    "texto",
    "demasiado_largo",
    "email_valido",
    "es_entero",
    "entero_o_none",
    "decimal_o_none",
    "a_datetime",
    "fecha_hora_actual",
]
