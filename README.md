# FACTURACION — CRUD con Streamlit + MySQL (patrón MVC)

Proyecto de la tarea **"Aplicación web con acceso a datos (patrón MVC)"**, hecho en Python + Streamlit por autorización del profesor para usar otra tecnología.

Incluye los tres CRUD completos y un módulo de acceso con roles:

- **Empleados** (`TBLEMPLEADO`) — SEGURIDAD > Empleados
- **Clientes** (`TBLCLIENTES`) — TABLAS > Clientes
- **Productos** (`TBLPRODUCTOS`) — TABLAS > Productos
- **Login con JWT** y permisos por rol (`admin`, `vendedor`, `consulta`)

## Inicio rápido

```powershell
cd facturacion_streamlit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# edita .streamlit\secrets.toml y escribe la contraseña de MySQL
python configurar_auth.py init
python probar_conexion.py
streamlit run app.py
```

`configurar_auth.py init` genera el `jwt_secret`, crea el usuario `admin` y muestra su contraseña **una sola vez**. Guárdala y cámbiala antes de publicar la app.

Para agregar usuarios:

```powershell
python configurar_auth.py agregar vendedor vendedor
python configurar_auth.py hash "MiClaveSegura123"
```

Si PowerShell bloquea la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Roles

| Rol | Accesos |
|---|---|
| `admin` | Todo, incluido Empleados, Roles y Seguridad |
| `vendedor` | Inicio, Clientes, Productos, Categorías, Facturas e Informes |
| `consulta` | Inicio, Clientes, Productos e Informes (solo lectura de pantallas) |

Los permisos se comprueban en el servidor en cada recarga (`app.py`), no solo se ocultan en el menú.

## Documentación

- [`GUIA.md`](GUIA.md): paso a paso, qué hace cada archivo, conceptos, cómo probar cada CRUD y errores frecuentes.
- [`CHECKLIST_Y_GUION_VIDEO.md`](CHECKLIST_Y_GUION_VIDEO.md): checklist de entrega y guion del video de sustentación.
- [`probar_conexion.py`](probar_conexion.py): verifica la conexión y muestra la estructura real de las tablas.

## Estructura

```text
facturacion_streamlit/
├─ app.py                  # entrada, layout, login y navegación
├─ config.py               # constantes (usuarios de auditoría, textos)
├─ configurar_auth.py      # genera [auth], hashes y usuarios
├─ models/                 # MODELO: tablas + SQL + usuarios de secrets
├─ controllers/            # CONTROLADOR: validaciones, JWT y permisos
├─ views/                  # VISTA: pantallas Streamlit
├─ tests/                  # pruebas (complemento)
├─ .streamlit/             # tema y plantilla de conexión
├─ requirements.txt
└─ README.md
```

## Seguridad

- **Login:** usuario y contraseña; la contraseña se guarda como hash **PBKDF2-HMAC-SHA256** con sal aleatoria y comparación en tiempo constante.
- **JWT:** token firmado con **HS256**, con expiración (30 min), emisor, `iat`, `nbf`, `jti` y validación en cada recarga. El token vive en `st.session_state`, no en la URL.
- **Roles:** permisos comprobados en el servidor antes de dibujar cada pantalla.
- **SQL injection:** todas las consultas usan `%s` y tuplas; nunca se concatenan valores del usuario. Hay pruebas que lo verifican.
- **XSS:** los textos se escapan y `tabla()` escapa sus celdas por defecto; solo se permite HTML construido por la app.
- **Fuerza bruta:** bloqueo temporal tras varios intentos fallidos.
- **CSRF:** no hay endpoints propios de escritura; las acciones usan formularios/botones de Streamlit con protección XSRF.
- **Secretos:** `secrets.toml` está excluido de Git y del `.zip`. Nunca contiene contraseñas en texto plano, solo hashes.

> Limitación: el bloqueo de intentos vive en memoria del proceso. Para producción con varios servidores conviene Redis o un WAF. Si se necesita “recordarme” entre recargas del navegador, se puede añadir una cookie `HttpOnly`/`Secure`/`SameSite=Strict`; por ahora se prefiere cerrar sesión al recargar.

## Generar el `.zip` de entrega

```powershell
powershell -ExecutionPolicy Bypass -File empaquetar.ps1
```

El script excluye `.venv`, `__pycache__`, `.git` y `.streamlit/secrets.toml`.
