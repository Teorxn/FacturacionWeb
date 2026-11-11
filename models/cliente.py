"""Modelo de TBLCLIENTES: estructura de la tabla y acceso a MySQL."""

from models.db import get_connection

# Columnas explícitas: el manual del profesor pide evitar SELECT *.
COLUMNAS = (
    "IdCliente, StrNombre, NumDocumento, StrDireccion, StrTelefono, "
    "StrEmail, DtmFechaModifica, StrUsuarioModifica"
)


def listar():
    """Devuelve todos los clientes ordenados por IdCliente."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(f"SELECT {COLUMNAS} FROM TBLCLIENTES ORDER BY IdCliente")
        return cur.fetchall()
    finally:
        con.close()


def obtener(id_cliente):
    """Devuelve un cliente por su id o None si no existe."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(
            f"SELECT {COLUMNAS} FROM TBLCLIENTES WHERE IdCliente = %s",
            (id_cliente,),
        )
        return cur.fetchone()
    finally:
        con.close()


def insertar(datos):
    """Inserta un cliente y devuelve el id generado."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO TBLCLIENTES "
            "(StrNombre, NumDocumento, StrDireccion, StrTelefono, StrEmail, "
            " DtmFechaModifica, StrUsuarioModifica) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                datos["StrNombre"],
                datos["NumDocumento"],
                datos["StrDireccion"],
                datos["StrTelefono"],
                datos["StrEmail"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifica"],
            ),
        )
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def actualizar(id_cliente, datos):
    """Actualiza un cliente por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "UPDATE TBLCLIENTES SET StrNombre = %s, NumDocumento = %s, "
            "StrDireccion = %s, StrTelefono = %s, StrEmail = %s, "
            "DtmFechaModifica = %s, StrUsuarioModifica = %s "
            "WHERE IdCliente = %s",
            (
                datos["StrNombre"],
                datos["NumDocumento"],
                datos["StrDireccion"],
                datos["StrTelefono"],
                datos["StrEmail"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifica"],
                id_cliente,
            ),
        )
        con.commit()
        return cur.rowcount
    finally:
        con.close()


def eliminar(id_cliente):
    """Elimina un cliente por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM TBLCLIENTES WHERE IdCliente = %s", (id_cliente,))
        con.commit()
        return cur.rowcount
    finally:
        con.close()
