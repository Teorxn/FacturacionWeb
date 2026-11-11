"""Modelo de TBLROLES: solo se usa para llenar el combo de empleados."""

from models.db import get_connection


def listar():
    """Devuelve los roles ordenados por descripción."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT IdRolEmpleado, StrDescripcion "
            "FROM TBLROLES ORDER BY StrDescripcion"
        )
        return cur.fetchall()
    finally:
        con.close()
