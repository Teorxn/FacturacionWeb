"""Prueba de conexión y estructura de las tablas.

Uso:
    python probar_conexion.py

Lee la configuración de .streamlit/secrets.toml, igual que la aplicación.
Los nombres de las tablas salen de una lista fija escrita aquí; nunca se
concatenan datos escritos por un usuario.
"""

import sys
from pathlib import Path

import mysql.connector

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

SECRETS = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
TABLAS = ("TBLPRODUCTOS", "TBLEMPLEADO", "TBLROLES", "TBLCLIENTES")


def cargar_config():
    if not SECRETS.exists():
        print(f"No existe {SECRETS}.")
        print("Copia .streamlit/secrets.toml.example y completa la contraseña.")
        sys.exit(1)

    with SECRETS.open("rb") as archivo:
        return tomllib.load(archivo)["mysql"]


def main():
    cfg = cargar_config()

    try:
        con = mysql.connector.connect(
            host=cfg["host"],
            port=int(cfg["port"]),
            database=cfg["database"],
            user=cfg["user"],
            password=cfg["password"],
            connection_timeout=10,
        )
    except mysql.connector.Error as exc:
        print("ERROR DE CONEXIÓN:", exc)
        print("Revisa servidor, puerto 3306, usuario, contraseña y firewall.")
        sys.exit(1)

    try:
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        print("Tablas encontradas:")
        for (tabla,) in cur.fetchall():
            print(" -", tabla)

        for tabla in TABLAS:
            print(f"\nDESCRIBE {tabla}:")
            cur.execute(f"DESCRIBE {tabla}")
            for columna in cur.fetchall():
                print("  ", columna)
    finally:
        con.close()


if __name__ == "__main__":
    main()
