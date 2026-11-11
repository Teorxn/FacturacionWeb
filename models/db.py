"""Puerta única de acceso a MySQL.

Todos los modelos piden la conexión aquí. Así, si algún día cambia el
servidor o la contraseña, se modifica un solo archivo.
"""

import mysql.connector
import streamlit as st


class ErrorBD(Exception):
    """Error controlado de conexión o configuración de la base de datos."""


def get_connection():
    """Crea y devuelve una conexión nueva a MySQL.

    La configuración se lee de .streamlit/secrets.toml para no escribir
    credenciales dentro del código.
    """
    try:
        cfg = st.secrets["mysql"]
    except Exception as exc:  # Streamlit lanza una excepción propia si falta el archivo
        raise ErrorBD(
            "Falta la configuración [mysql] en .streamlit/secrets.toml. "
            "Copia secrets.toml.example y completa la contraseña."
        ) from exc

    try:
        return mysql.connector.connect(
            host=cfg["host"],
            port=int(cfg["port"]),
            database=cfg["database"],
            user=cfg["user"],
            password=cfg["password"],
            connection_timeout=10,
            # FOUND_ROWS hace que UPDATE devuelva las filas encontradas,
            # aunque los valores enviados sean iguales a los que ya había.
            client_flags=[mysql.connector.constants.ClientFlag.FOUND_ROWS],
        )
    except mysql.connector.Error as exc:
        raise ErrorBD(
            "No se pudo conectar a MySQL. Revisa la configuración de "
            ".streamlit/secrets.toml, tu red y que el puerto 3306 esté abierto."
        ) from exc
