"""Modelo de TBLEMPLEADO: estructura de la tabla y acceso a MySQL.

Ojo con los nombres exactos de las columnas:
strNombre y strDatosAdicionales empiezan con minúscula, y el usuario de
auditoría es StrUsuarioModifico (con "o"), distinto a TBLCLIENTES.
"""

from models.db import get_connection

COLUMNAS = (
    "e.IdEmpleado, e.strNombre, e.NumDocumento, e.StrDireccion, "
    "e.StrTelefono, e.StrEmail, e.IdRolEmpleado, "
    "r.StrDescripcion AS StrDescripcionRol, e.DtmIngreso, e.DtmRetiro, "
    "e.strDatosAdicionales, e.DtmFechaModifica, e.StrUsuarioModifico"
)

DESDE = "FROM TBLEMPLEADO e LEFT JOIN TBLROLES r ON r.IdRolEmpleado = e.IdRolEmpleado"


def listar():
    """Devuelve todos los empleados con la descripción de su rol."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(f"SELECT {COLUMNAS} {DESDE} ORDER BY e.IdEmpleado")
        return cur.fetchall()
    finally:
        con.close()


def obtener(id_empleado):
    """Devuelve un empleado por su id o None si no existe."""
    con = get_connection()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(
            f"SELECT {COLUMNAS} {DESDE} WHERE e.IdEmpleado = %s",
            (id_empleado,),
        )
        return cur.fetchone()
    finally:
        con.close()


def insertar(datos):
    """Inserta un empleado y devuelve el id generado."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO TBLEMPLEADO "
            "(strNombre, NumDocumento, StrDireccion, StrTelefono, StrEmail, "
            " IdRolEmpleado, DtmIngreso, DtmRetiro, strDatosAdicionales, "
            " DtmFechaModifica, StrUsuarioModifico) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                datos["strNombre"],
                datos["NumDocumento"],
                datos["StrDireccion"],
                datos["StrTelefono"],
                datos["StrEmail"],
                datos["IdRolEmpleado"],
                datos["DtmIngreso"],
                datos["DtmRetiro"],
                datos["strDatosAdicionales"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifico"],
            ),
        )
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def actualizar(id_empleado, datos):
    """Actualiza un empleado por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "UPDATE TBLEMPLEADO SET strNombre = %s, NumDocumento = %s, "
            "StrDireccion = %s, StrTelefono = %s, StrEmail = %s, "
            "IdRolEmpleado = %s, DtmIngreso = %s, DtmRetiro = %s, "
            "strDatosAdicionales = %s, DtmFechaModifica = %s, "
            "StrUsuarioModifico = %s "
            "WHERE IdEmpleado = %s",
            (
                datos["strNombre"],
                datos["NumDocumento"],
                datos["StrDireccion"],
                datos["StrTelefono"],
                datos["StrEmail"],
                datos["IdRolEmpleado"],
                datos["DtmIngreso"],
                datos["DtmRetiro"],
                datos["strDatosAdicionales"],
                datos["DtmFechaModifica"],
                datos["StrUsuarioModifico"],
                id_empleado,
            ),
        )
        con.commit()
        return cur.rowcount
    finally:
        con.close()


def eliminar(id_empleado):
    """Elimina un empleado por id. Devuelve la cantidad de filas afectadas."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM TBLEMPLEADO WHERE IdEmpleado = %s", (id_empleado,))
        con.commit()
        return cur.rowcount
    finally:
        con.close()
