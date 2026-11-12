"""Configura la autenticación en .streamlit/secrets.toml.

Uso:
    python configurar_auth.py init
    python configurar_auth.py init --usuario admin --password "MiClaveSegura123"
    python configurar_auth.py agregar vendedor vendedor
    python configurar_auth.py hash "MiClaveSegura123"
    python configurar_auth.py validar

Nunca escribe contraseñas en texto plano: guarda un hash PBKDF2.
"""

import argparse
import re
import secrets
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from models.usuario import generar_hash

RAIZ = Path(__file__).resolve().parent
SECRETS = RAIZ / ".streamlit" / "secrets.toml"
USUARIO_VALIDO = re.compile(r"^[a-zA-Z0-9_.-]{1,50}$")
ROLES = ("admin", "vendedor", "consulta")
LARGO_MINIMO_PASSWORD = 12


def _leer_secrets():
    if not SECRETS.exists():
        print(f"No existe {SECRETS}.")
        print("Copia .streamlit/secrets.toml.example y completa la conexión.")
        sys.exit(1)

    with SECRETS.open("rb") as archivo:
        return tomllib.load(archivo)


def _cita(valor):
    """Convierte un valor en cadena TOML entre comillas."""
    limpio = str(valor).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{limpio}"'


def _validar_password(password):
    if len(password) < LARGO_MINIMO_PASSWORD:
        print(
            f"La contraseña debe tener al menos {LARGO_MINIMO_PASSWORD} "
            "caracteres."
        )
        sys.exit(1)


def _bloque_usuario(usuario, nombre, rol, password):
    return f"""
[auth.users.{_cita(usuario)}]
nombre = {_cita(nombre)}
rol = {_cita(rol)}
activo = true
password_hash = {_cita(generar_hash(password))}
"""


def init(args):
    datos = _leer_secrets()
    if "auth" in datos:
        print("Ya existe la sección [auth]. No se modificó nada.")
        print("Para agregar otro usuario: python configurar_auth.py agregar ...")
        return

    password = args.password or secrets.token_urlsafe(12)
    _validar_password(password)

    bloque = f"""
[auth]
jwt_secret = {_cita(secrets.token_urlsafe(48))}
token_minutos = 30
max_intentos = 5
bloqueo_minutos = 5
issuer = "facturacion-streamlit"
""" + _bloque_usuario(args.usuario, args.nombre, args.rol, password)

    with SECRETS.open("a", encoding="utf-8") as archivo:
        archivo.write(bloque)

    print("Configuración [auth] creada correctamente.")
    print(f"Usuario:    {args.usuario}")
    print(f"Contraseña: {password}")
    print("Guarda esa contraseña y cámbiala antes de publicar la app.")


def agregar(args):
    datos = _leer_secrets()
    if "auth" not in datos:
        print("Primero ejecuta: python configurar_auth.py init")
        sys.exit(1)

    usuario = str(args.usuario).strip().lower()
    if not USUARIO_VALIDO.match(usuario):
        print("El usuario solo admite letras, números, punto, guion y guion bajo.")
        sys.exit(1)

    usuarios = (datos.get("auth") or {}).get("users") or {}
    if usuario in {str(clave).lower() for clave in usuarios}:
        print(f"El usuario {usuario} ya existe.")
        sys.exit(1)

    password = args.password or secrets.token_urlsafe(12)
    _validar_password(password)
    nombre = args.nombre or usuario

    with SECRETS.open("a", encoding="utf-8") as archivo:
        archivo.write(_bloque_usuario(usuario, nombre, args.rol, password))

    print(f"Usuario {usuario} agregado con rol {args.rol}.")
    print(f"Contraseña: {password}")
    print("Guárdala y cámbiala antes de publicar la app.")


def hash_password(args):
    print(generar_hash(args.password))


def validar(args):
    """Revisa la estructura de [auth] sin mostrar secretos."""
    datos = _leer_secrets()
    auth = datos.get("auth")
    if not auth:
        print("Falta la sección [auth]. Ejecuta: python configurar_auth.py init")
        sys.exit(1)

    if len(str(auth.get("jwt_secret") or "")) < 32:
        print("El jwt_secret debe tener al menos 32 caracteres.")
        sys.exit(1)

    usuarios = auth.get("users") or {}
    if not usuarios:
        print("No hay usuarios en [auth.users]. Agrega uno con `agregar`.")
        sys.exit(1)

    errores = []
    for nombre, info in usuarios.items():
        info = info or {}
        if str(info.get("rol") or "") not in ROLES:
            errores.append(f"{nombre}: rol inválido")
        if not str(info.get("password_hash") or "").startswith(
            "pbkdf2_sha256$"
        ):
            errores.append(f"{nombre}: password_hash inválido")

    if errores:
        print("Errores encontrados:")
        for error in errores:
            print(" -", error)
        sys.exit(1)

    print(f"Configuración [auth] correcta. Usuarios: {', '.join(usuarios)}")


def main():
    parser = argparse.ArgumentParser(
        description="Configura usuarios y JWT para FACTURACION."
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_init = sub.add_parser("init", help="Crea [auth] y el primer usuario.")
    p_init.add_argument("--usuario", default="admin")
    p_init.add_argument("--nombre", default="Administrador")
    p_init.add_argument("--rol", default="admin", choices=ROLES)
    p_init.add_argument("--password")
    p_init.set_defaults(func=init)

    p_add = sub.add_parser("agregar", help="Agrega otro usuario.")
    p_add.add_argument("usuario")
    p_add.add_argument("rol", choices=ROLES)
    p_add.add_argument("--nombre")
    p_add.add_argument("--password")
    p_add.set_defaults(func=agregar)

    p_hash = sub.add_parser("hash", help="Genera un hash para secrets.toml.")
    p_hash.add_argument("password")
    p_hash.set_defaults(func=hash_password)

    p_validar = sub.add_parser("validar", help="Revisa la sección [auth].")
    p_validar.set_defaults(func=validar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
