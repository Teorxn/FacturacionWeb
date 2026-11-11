# FACTURACION — CRUD con Streamlit + MySQL (patrón MVC)

Proyecto de la tarea **"Aplicación web con acceso a datos (patrón MVC)"**, hecho en Python + Streamlit por autorización del profesor para usar otra tecnología.

Incluye los tres CRUD completos:

- **Empleados** (`TBLEMPLEADO`) — SEGURIDAD > Empleados
- **Clientes** (`TBLCLIENTES`) — TABLAS > Clientes
- **Productos** (`TBLPRODUCTOS`) — TABLAS > Productos

## Inicio rápido

```powershell
cd facturacion_streamlit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# edita .streamlit\secrets.toml y escribe la contraseña
python probar_conexion.py
streamlit run app.py
```

Si PowerShell bloquea la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Documentación

- [`GUIA.md`](GUIA.md): paso a paso, qué hace cada archivo, conceptos, cómo probar cada CRUD y errores frecuentes.
- [`CHECKLIST_Y_GUION_VIDEO.md`](CHECKLIST_Y_GUION_VIDEO.md): checklist de entrega y guion del video de sustentación.
- [`probar_conexion.py`](probar_conexion.py): verifica la conexión y muestra la estructura real de las tablas.

## Estructura

```text
facturacion_streamlit/
├─ app.py                  # entrada, layout y navegación
├─ config.py               # constantes (usuarios de auditoría, textos)
├─ models/                 # MODELO: tablas + SQL
├─ controllers/            # CONTROLADOR: validaciones y lógica
├─ views/                  # VISTA: pantallas Streamlit
├─ tests/                  # pruebas (complemento)
├─ .streamlit/             # tema y plantilla de conexión
├─ requirements.txt
└─ README.md
```

## Seguridad

- Las consultas usan `%s` y tuplas: no se concatenan valores del usuario.
- `UPDATE` y `DELETE` siempre llevan `WHERE` por id.
- La contraseña vive en `.streamlit/secrets.toml`, que **no** se incluye en el `.zip`.
- Antes de borrar se muestra una pantalla de confirmación.

## Generar el `.zip` de entrega

```powershell
powershell -ExecutionPolicy Bypass -File empaquetar.ps1
```

El script excluye `.venv`, `__pycache__`, `.git` y `.streamlit/secrets.toml`.
