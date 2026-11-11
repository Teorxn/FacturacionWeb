"""Constantes de configuración de la aplicación.

[COMPLEMENTO] Este archivo no viene en el PDF del profesor. Se agregó para
tener en un solo lugar los textos y usuarios de auditoría, y para que se
puedan cambiar sin tocar la lógica.
"""

import os

APP_NOMBRE = "FACTURACION"
FOOTER_TEXTO = "Footer Text"

# Usuarios de auditoría tal como los pide el documento de la tarea.
# Se pueden cambiar con variables de entorno sin editar el código.
USUARIO_CLIENTE = os.getenv("USUARIO_CLIENTE", "Sistema")
USUARIO_EMPLEADO = os.getenv("USUARIO_EMPLEADO", "javier")
USUARIO_PRODUCTO = os.getenv("USUARIO_PRODUCTO", "Sistema")
