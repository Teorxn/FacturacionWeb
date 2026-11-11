"""Modelo de TBLPRODUCTOS: estructura de la tabla y acceso a MySQL.

Columnas reales verificadas con DESCRIBE TBLPRODUCTOS:
IdProducto, StrNombreProducto, StrDescripcion, NumPrecio, NumStock,
StrCategoria, BitActivo, DtmFechaModifica, StrUsuarioModifica.
"""

from models.db import get_connection

COLUMNAS = (
    "IdProducto, StrNombreProducto, StrDescripcion, NumPrecio, NumStock, "
    "StrCategoria, BitActivo, DtmFechaModifica, StrUsuarioModifica"
)


def listar():
    """Devuelve todos los productos ordenados por IdProducto."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(f"SELECT {COLUMNAS} FROM TBLPRODUCTOS ORDER BY IdProducto")
        return cur.fetchall()
    finally:
        con.close()


def obtener(id_producto):
    """Devuelve un producto por su id o None si no existe."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(
            f"SELECT {COLUMNAS} FROM TBLPRODUCTOS WHERE IdProducto = %s",
            (id_producto,),
        )
        return cur.fetchone()
    finally:
        con.close()


def insertar(datos):
    """Inserta un producto y devuelve el id generado."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO TBLPRODUCTOS "
            "(StrNombreProducto, StrDescripcion, NumPrecio, NumStock, "
            " StrCategoria, BitActivo, DtmFechaModifica, StrUsuarioModifica) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                datos["StrNombreProducto"],
                datos["StrDescripcion"],
                datos["NumPrecio"],
                datos["NumStock"],
                datos["StrCategoria"],
                datos["BitActivo"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifica"],
            ),
        )
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def actualizar(id_producto, datos):
    """Actualiza un producto por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "UPDATE TBLPRODUCTOS SET StrNombreProducto = %s, StrDescripcion = %s, "
            "NumPrecio = %s, NumStock = %s, StrCategoria = %s, BitActivo = %s, "
            "DtmFechaModifica = %s, StrUsuarioModifica = %s "
            "WHERE IdProducto = %s",
            (
                datos["StrNombreProducto"],
                datos["StrDescripcion"],
                datos["NumPrecio"],
                datos["NumStock"],
                datos["StrCategoria"],
                datos["BitActivo"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifica"],
                id_producto,
            ),
        )
        con.commit()
        return cur.rowcount
    finally:
        con.close()


def eliminar(id_producto):
    """Elimina un producto por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM TBLPRODUCTOS WHERE IdProducto = %s", (id_producto,))
        con.commit()
        return cur.rowcount
    finally:
        con.close()
