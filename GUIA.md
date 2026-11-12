# GUÍA DEL PROYECTO — FACTURACION con Python + Streamlit

Esta guía explica **qué se entregó, cómo se instala, qué hace cada archivo y cómo probar cada operación**. Está escrita para alguien que está aprendiendo: primero el paso a paso y después el porqué.

> **Nota de honestidad:** la tarea original era ASP.NET MVC. El profesor autorizó usar otra tecnología, así que aquí está la misma especificación funcional (pantallas, campos, validaciones, tablas y columnas) implementada en Python + Streamlit. Todo lo que no venía en el documento original está marcado como **[COMPLEMENTO]**.

---

## 1. Qué incluye el proyecto

Tres CRUD completos, con **listar, crear, editar y eliminar**:

| CRUD | Tabla real | Dónde aparece en el menú |
|---|---|---|
| Empleados | `TBLEMPLEADO` | SEGURIDAD > Empleados |
| Clientes | `TBLCLIENTES` | TABLAS > Clientes |
| Productos | `TBLPRODUCTOS` | TABLAS > Productos |

Además:

- **Login real con JWT** y permisos por rol (`admin`, `vendedor`, `consulta`).
- Barra superior oscura con **FACTURACION**, Inicio, Acerca, Ayuda, Contacto y el usuario/rol de la sesión.
- Menú lateral con fondo `#345863` y los grupos **TABLAS**, **FACTURAS** y **SEGURIDAD**.
- Pie de página con el texto **Footer Text**.
- Páginas informativas: Inicio, Acerca, Ayuda y Contacto.
- Entradas sin funcionalidad (Categorias, facturas, Informes, Roles) que muestran **“En construcción”**.
- Pantalla **Seguridad** con el estado de la sesión y los controles aplicados.
- Validación del lado del servidor, SQL parametrizado, escape de HTML y confirmación antes de eliminar.

---

## 2. Requisitos

- **Python 3.10 o superior** (probado con Python 3.12.6).
- Acceso a Internet y al servidor MySQL del curso (`virtualaprendo.online`, puerto 3306).
- Terminal de PowerShell (Windows) o la terminal de tu sistema.
- Opcional: VS Code para editar el código.

Para verificar la versión de Python:

```powershell
python --version
```

---

## 3. Instalación paso a paso

### 3.1 Entrar a la carpeta del proyecto

```powershell
cd facturacion_streamlit
```

### 3.2 Crear y activar un entorno virtual

Un entorno virtual es una caja donde se instalan las librerías del proyecto sin ensuciar el Python del sistema.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell muestra un error de “Execution Policy”:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

En macOS/Linux sería:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.3 Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esto instala:

- `streamlit`: la interfaz web.
- `mysql-connector-python`: el conector oficial de MySQL. **[COMPLEMENTO]** Se eligió porque no usa ORM y permite SQL escrito a mano.
- `tomli`: solo para Python 3.10, porque `tomllib` viene incluido desde Python 3.11. **[COMPLEMENTO]**

---

## 4. Configurar la conexión

La contraseña **no** se escribe dentro del código. Se lee de `.streamlit/secrets.toml`.

### 4.1 Copiar la plantilla

```powershell
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

### 4.2 Completar la contraseña

Abre `.streamlit/secrets.toml` y escribe la contraseña real:

```toml
[mysql]
host = "virtualaprendo.online"
port = 3306
database = "dbfacturas"
user = "dbfacturas"
password = "AQUI_VA_LA_CONTRASENA"
```

> **Importante:** `secrets.toml` no se sube a repositorios públicos ni se incluye en el `.zip`. La plantilla que se entrega es `secrets.toml.example`, con la contraseña vacía.

### 4.3 ¿Por qué así?

En ASP.NET la conexión se configuraba en `Web.config` con una `connectionString`. En Python el equivalente es `secrets.toml` + `models/db.py`. **[COMPLEMENTO: equivalencia]**

---

## 5. Probar la conexión antes de arrancar la app

```powershell
python probar_conexion.py
```

El script:

1. Lee `.streamlit/secrets.toml`.
2. Se conecta a MySQL.
3. Muestra las tablas con `SHOW TABLES`.
4. Ejecuta `DESCRIBE` sobre `TBLPRODUCTOS`, `TBLEMPLEADO`, `TBLROLES` y `TBLCLIENTES`.

Si funciona, verás la lista de tablas y columnas. Si falla, revisa la sección 11 (errores frecuentes).

> **Nota:** en el documento original el script de prueba tenía la contraseña escrita. Aquí se cambió para que lea `secrets.toml` y no haya credenciales dentro del código. **[COMPLEMENTO]**

---

## 6. Ejecutar la aplicación

```powershell
streamlit run app.py
```

Streamlit abre el navegador en `http://localhost:8501`. Si el puerto está ocupado:

```powershell
streamlit run app.py --server.port 8502
```

Para detenerla: `Ctrl + C` en la terminal.

---

## 7. Estructura y qué hace cada archivo (en orden M-V-C)

```text
facturacion_streamlit/
├─ app.py
├─ config.py
├─ configurar_auth.py
├─ probar_conexion.py
├─ requirements.txt
├─ README.md
├─ GUIA.md
├─ CHECKLIST_Y_GUION_VIDEO.md
├─ empaquetar.ps1
├─ .streamlit/
│   ├─ config.toml
│   ├─ secrets.toml.example
│   └─ secrets.toml          (local, no se entrega)
├─ models/
│   ├─ db.py
│   ├─ usuario.py
│   ├─ cliente.py
│   ├─ producto.py
│   ├─ empleado.py
│   └─ rol.py
├─ controllers/
│   ├─ comun.py
│   ├─ auth_controller.py
│   ├─ clientes_controller.py
│   ├─ productos_controller.py
│   └─ empleados_controller.py
├─ views/
│   ├─ estilos.py
│   ├─ componentes.py
│   ├─ login.py
│   ├─ seguridad.py
│   ├─ inicio.py
│   ├─ acerca.py
│   ├─ ayuda.py
│   ├─ contacto.py
│   ├─ en_construccion.py
│   ├─ clientes.py
│   ├─ productos.py
│   └─ empleados.py
└─ tests/
    ├─ test_validaciones.py
    ├─ test_modelos_bd.py
    ├─ test_seguridad.py
    └─ test_app.py
```

### 7.1 `app.py` — la entrada y el layout

Es lo primero que corre. Hace cinco cosas:

1. Configura la página (`st.set_page_config`).
2. Inyecta el CSS de `views/estilos.py`.
3. Valida el JWT de la sesión; si no hay sesión, muestra el login y se detiene.
4. Dibuja la barra superior, el menú lateral (según el rol) y el pie.
5. Decide qué vista mostrar según el parámetro `page` de la URL y comprueba el permiso del rol.

La navegación usa enlaces como `?page=clientes` y `?page=empleados`. **[COMPLEMENTO]** Se eligió así en lugar de `st.navigation` porque permite controlar el HTML del menú y los colores con más libertad.

### 7.2 `config.py` — constantes

Guarda el nombre de la app, el texto del pie y los usuarios de auditoría:

- Clientes: `"Sistema"`.
- Empleados: `"javier"` (como en el PDF).
- Productos: `"Sistema"`.

Se pueden cambiar con variables de entorno (`USUARIO_EMPLEADO`, etc.) sin tocar el código. **[COMPLEMENTO]**

### 7.3 `models/` — el MODELO

El modelo es la parte que **conoce la estructura de la tabla y habla con MySQL**. No sabe nada de botones ni de pantallas.

#### `models/db.py` — la puerta única

Todas las consultas piden la conexión aquí. La analogía: en un edificio hay una sola puerta de entrada; si cambia la cerradura, se cambia en un solo lugar.

```python
def get_connection():
    cfg = st.secrets["mysql"]
    return mysql.connector.connect(...)
```

Si falta `secrets.toml`, lanza un error claro (`ErrorBD`) en vez de un error técnico raro.

#### `models/cliente.py`, `producto.py`, `empleado.py`, `rol.py`

Cada archivo tiene las operaciones del CRUD:

| Función | Qué hace | SQL |
|---|---|---|
| `listar()` | Trae todos los registros | `SELECT` con columnas explícitas |
| `obtener(id)` | Trae uno por id | `SELECT ... WHERE id = %s` |
| `insertar(datos)` | Crea | `INSERT INTO ... VALUES (%s, ...)` |
| `actualizar(id, datos)` | Modifica | `UPDATE ... WHERE id = %s` |
| `eliminar(id)` | Borra | `DELETE ... WHERE id = %s` |

Reglas que se cumplen:

- **Nunca** `SELECT *`: se listan las columnas explícitas.
- Los valores van con `%s` y una tupla, nunca concatenados.
- `UPDATE` y `DELETE` **siempre** llevan `WHERE` por id.
- La conexión se cierra en `finally`.
- `commit()` después de `INSERT`, `UPDATE` y `DELETE`.

`models/empleado.py` hace un `LEFT JOIN` con `TBLROLES` para traer la descripción del rol. `models/rol.py` solo se usa para llenar el combo de roles.

### 7.4 `controllers/` — el CONTROLADOR

El controlador es el **mesero**: recibe el pedido de la vista, revisa que esté bien, y solo entonces se lo pasa a la cocina (el modelo). Si algo falta, devuelve el plato con un mensaje claro.

#### `controllers/comun.py`

Utilidades compartidas: convertir `None` a `""`, validar correo, convertir números y fechas, y reexportar `ErrorBD`. **[COMPLEMENTO]** Se agregó para no repetir código en los tres controladores.

#### `controllers/clientes_controller.py`, `productos_controller.py`, `empleados_controller.py`

Cada uno tiene:

- `listar_*()` y `obtener_*()`: envuelven al modelo y traducen errores de MySQL a `ErrorBD`.
- `validar_*()`: **validación del lado del servidor**, antes de tocar la base de datos.
- `_normalizar()`: aplica las reglas del manual (texto `None` → `""`, documento vacío → `NULL`, fecha de modificación → ahora, usuario → constante).
- `guardar_*()`: decide si es `INSERT` o `UPDATE` y devuelve `(ok, mensaje)`.
- `eliminar_*()`: borra por id y devuelve `(ok, mensaje)`.

Ejemplo del flujo de validación de clientes:

```python
def validar_cliente(datos):
    errores = {}
    if texto(datos.get("StrNombre")) == "":
        errores["StrNombre"] = "El nombre es obligatorio."
    correo = texto(datos.get("StrEmail"))
    if correo and not email_valido(correo):
        errores["StrEmail"] = "El correo no tiene un formato válido."
    return errores
```

### 7.5 `views/` — la VISTA

La vista es lo que el usuario ve. **No escribe SQL**: pide datos al controlador y dibuja.

#### `views/estilos.py`

Todo el CSS: barra superior oscura, menú lateral `#345863`, tablas, botones por color, pie, etc. **[COMPLEMENTO]**

#### `views/componentes.py`

Funciones reutilizables:

- `titulo()`: título de cada pantalla.
- `tabla()`: tabla HTML con acciones.
- `tabla_detalle()`: datos de solo lectura para la confirmación de borrado.
- `enlace()`: botón con apariencia de enlace.
- `url()` y `param()`: navegación por parámetros.
- `flash()` y `mostrar_flash()`: mensaje de “guardado correctamente” después de redirigir.

#### `views/clientes.py`, `productos.py`, `empleados.py`

Cada uno tiene una función `render()` que decide entre cuatro pantallas:

1. **Lista**: título, caja gris con el botón de nuevo y tabla con acciones.
2. **Nuevo**: formulario vacío.
3. **Editar**: formulario prellenado con el registro elegido.
4. **Eliminar**: confirmación con los datos en solo lectura.

#### Páginas informativas

`inicio.py`, `acerca.py`, `ayuda.py` y `contacto.py` solo muestran el título, como en el PDF. `en_construccion.py` muestra “En construcción” para las entradas que no tienen funcionalidad. **[COMPLEMENTO]**

### 7.6 `tests/` — pruebas

**[COMPLEMENTO]** No venían en el PDF, pero ayudan a comprobar que todo sigue funcionando:

- `test_validaciones.py`: 18 pruebas de validaciones, conversiones y normalización, sin base de datos.
- `test_modelos_bd.py`: prueba INSERT, UPDATE, DELETE y SELECT reales contra MySQL, pero dentro de una transacción con **rollback**, así no deja datos.
- `test_seguridad.py`: 27 pruebas de contraseñas, JWT, permisos, XSS, SQL injection y bloqueo por intentos.
- `test_app.py`: 14 pruebas con Streamlit `AppTest` para el login, las pantallas y el modo solo lectura, verificando que no haya excepciones.

Para correrlas:

```powershell
python -m unittest discover -s tests -v
```

### 7.7 Login, JWT y seguridad

**[COMPLEMENTO]** El PDF no pedía login, pero se agregó para proteger los CRUD y demostrar buenas prácticas.

| Archivo | Responsabilidad |
|---|---|
| `models/usuario.py` | Lee `[auth.users.*]` de `secrets.toml`; genera y verifica hashes PBKDF2. |
| `controllers/auth_controller.py` | Crea/valida el JWT, bloquea intentos fallidos y define los permisos por rol. |
| `views/login.py` | Formulario de usuario y contraseña. |
| `views/seguridad.py` | Muestra la sesión activa, el rol y los controles aplicados. |
| `configurar_auth.py` | Crea `[auth]`, agrega usuarios y genera hashes. |

#### Configurar el primer usuario

```powershell
python configurar_auth.py init
```

Eso agrega a `secrets.toml`:

```toml
[auth]
jwt_secret = "..."
token_minutos = 30
max_intentos = 5
bloqueo_minutos = 5
issuer = "facturacion-streamlit"

[auth.users."admin"]
nombre = "Administrador"
rol = "admin"
activo = true
password_hash = "pbkdf2_sha256$600000$...$..."
```

La contraseña se muestra **una sola vez** en la terminal. No se guarda en texto plano.

Para agregar otro usuario:

```powershell
python configurar_auth.py agregar vendedor vendedor
python configurar_auth.py hash "MiClaveSegura123"
```

#### Cómo funciona el JWT

1. El usuario escribe sus credenciales en `views/login.py`.
2. `auth_controller.iniciar_sesion()` busca el usuario y verifica el hash.
3. Si es correcto, `crear_token()` firma un JWT con HS256 y lo guarda en `st.session_state`.
4. En cada recarga, `sesion_actual()` valida firma, expiración, emisor, `iat`, `nbf` y que el usuario siga activo con el mismo rol.
5. Si el token no sirve, se borra la sesión y se vuelve al login.

El token **no** se guarda en la URL ni en una cookie legible por JavaScript. Al recargar el navegador se pierde la sesión, lo cual es intencional.

#### Roles y permisos

| Rol | Páginas |
|---|---|
| `admin` | Todas |
| `vendedor` | Inicio, Acerca, Ayuda, Contacto, Clientes, Productos, Categorías, Facturas, Informes |
| `consulta` | Inicio, Acerca, Ayuda, Contacto, Clientes, Productos, Informes |

`app.py` comprueba `auth.tiene_permiso(rol, page)` **antes** de dibujar la vista. Si alguien escribe `?page=empleados` con rol `consulta`, recibe “No tienes permiso para ver esta sección.”, aunque oculte el enlace del menú.

#### Defensas aplicadas

- **SQL injection:** `%s` + tuplas en todos los modelos; hay pruebas con un payload `1 OR 1=1; DROP TABLE ...`.
- **XSS:** `escapar()` usa `html.escape`; `tabla()` escapa celdas por defecto y solo respeta `HTMLSeguro` creado por la app.
- **Fuerza bruta:** tras `max_intentos` fallos se bloquea el usuario `bloqueo_minutos` minutos.
- **Contraseñas:** PBKDF2-HMAC-SHA256 con 600 000 iteraciones, sal aleatoria y `hmac.compare_digest`.
- **CSRF:** no hay endpoints HTTP propios de escritura; las acciones pasan por formularios y botones de Streamlit con XSRF activo.
- **Secretos:** `secrets.toml` está en `.gitignore` y `empaquetar.ps1` lo excluye.
- **Entradas:** se eliminan caracteres de control y se valida el largo máximo en el servidor.

> El bloqueo de intentos es memoria del proceso. Para un despliegue con varios servidores haría falta Redis o un WAF.

---

## 8. El flujo MVC con un ejemplo concreto

Supongamos que el usuario crea un cliente:

```text
1. Usuario hace clic en NUEVO
        ↓
2. app.py cambia a ?page=clientes&accion=nuevo
        ↓
3. views/clientes.py dibuja el formulario
        ↓
4. Usuario escribe los datos y hace clic en Guardar
        ↓
5. controllers/clientes_controller.py valida (servidor)
        ↓  si hay errores, vuelve al formulario con mensajes en rojo
        ↓  si está bien...
6. models/cliente.py ejecuta INSERT con %s
        ↓
7. MySQL guarda el registro
        ↓
8. El controlador devuelve (True, "Cliente creado correctamente.")
        ↓
9. La vista guarda un mensaje flash y redirige a la lista
        ↓
10. La lista vuelve a pedir los datos al modelo y los muestra
```

Analogía completa: el **usuario** pide un plato (crear), el **mesero** (controlador) revisa el pedido, la **cocina** (modelo) lo prepara consultando la **despensa** (MySQL), y el **mesero** lleva el plato a la **mesa** (vista).

---

## 9. Cómo probar cada operación de cada CRUD

Antes de probar, arranca la app con `streamlit run app.py` y verifica que la conexión funcione.

### 9.1 Clientes (TABLAS > Clientes)

**Consulta**

1. En el menú lateral, entra a **TABLAS > Clientes**.
2. Debe aparecer el título **“Lista de Clientes”**.
3. La tabla muestra **Id, Nombre, Documento, Teléfono, Email, Acciones**.
4. Si la tabla está vacía, debe decir **“No hay clientes registrados.”**

**Ingreso**

1. Haz clic en **NUEVO** (caja gris).
2. Se abre **“Nuevo Cliente”**.
3. Deja el nombre vacío y pulsa **Guardar**: debe aparecer en rojo **“El nombre es obligatorio.”**
4. Escribe un correo inválido (por ejemplo `ana@`) y pulsa **Guardar**: debe aparecer **“El correo no tiene un formato válido.”**
5. Completa un nombre válido, por ejemplo `Cliente de prueba`, y guarda.
6. Debe volver a la lista y mostrar **“Cliente creado correctamente.”**
7. El documento es opcional; si lo escribes, debe ser numérico. La dirección y el teléfono también son opcionales.

**Modificación**

1. En la fila del cliente, haz clic en **Editar** (botón celeste).
2. El formulario debe venir **prellenado** con los datos actuales.
3. Cambia el nombre y guarda.
4. Debe volver a la lista y mostrar **“Cliente actualizado correctamente.”**
5. El `IdCliente` viaja oculto en la URL; sin él, el `UPDATE` no afectaría el registro correcto.

**Retiro**

1. En la fila, haz clic en **Eliminar** (botón rojo).
2. Se abre **“Eliminar Cliente”** con el texto **“¿Está seguro de que desea eliminar este cliente?”** y los datos en solo lectura.
3. Pulsa **Cancelar**: debe volver a la lista sin borrar nada.
4. Vuelve a entrar y pulsa **Eliminar**: solo ahí se ejecuta el `DELETE`.
5. Si el cliente tiene facturas asociadas, MySQL no deja borrarlo y la app muestra un mensaje claro, no un error técnico.

### 9.2 Empleados (SEGURIDAD > Empleados)

**Consulta**

1. Entra a **SEGURIDAD > Empleados**.
2. Debe aparecer **“ADMON EMPLEADOS”**.
3. La tabla muestra **Nombre, Documento, Telefono, Correo, ACCIONES**.

**Ingreso**

1. Haz clic en **+Nuevo**.
2. Se abre **“Ingreso Empleado”** con los campos en este orden:
   Nombre, Nro Documento, Direccion, Telefono, Correo, **ROL**, Fecha Ingreso, Fecha retiro, Datos adicionales.
3. El combo **ROL** se carga desde `TBLROLES` (Gerente, Secretaria, Operario, Administrativo, programador). También existe la opción **(Sin rol)**, porque la columna admite NULL. **[COMPLEMENTO]**
4. Las fechas son opcionales: si se dejan vacías, se guarda `NULL`.
5. Nombre y Nro Documento son obligatorios. El documento debe ser numérico.
6. Al guardar, la app asigna `DtmFechaModifica = ahora` y `StrUsuarioModifico = "javier"`.
7. Debe volver a la lista y mostrar **“Empleado creado correctamente.”**

**Modificación**

1. Haz clic en **Editar**.
2. Se abre **“Editar”** con el formulario prellenado y el rol actual seleccionado.
3. Cambia un dato y guarda. Debe volver a la lista con **“Empleado actualizado correctamente.”**

**Retiro**

1. Haz clic en **Borrar**.
2. Se abre **“Eliminar Empleado”** con la confirmación.
3. **Cancelar** vuelve a la lista; **Eliminar** borra.
4. Si el empleado está ligado a una factura o a un registro de seguridad, la base de datos no deja borrarlo y la app muestra: “No se puede eliminar este empleado porque está ligado a una factura o a un registro de seguridad.”
5. Para probar el borrado sin problemas, crea primero un empleado nuevo (sin facturas) y bórralo.

> **Ojo con los nombres exactos:** `strNombre` y `strDatosAdicionales` empiezan con minúscula; el usuario de auditoría es `StrUsuarioModifico` (con “o”), distinto de `StrUsuarioModifica` en clientes.

### 9.3 Productos (TABLAS > Productos)

**Consulta**

1. Entra a **TABLAS > Productos**.
2. Debe aparecer **“Lista de Productos”**.
3. La tabla muestra **Id, Nombre, Categoría, Precio, Stock, Activo, Acciones**.
4. Si no hay registros: **“No hay productos registrados.”**

**Ingreso**

1. Haz clic en **NUEVO**.
2. Se abre **“Nuevo Producto”** con: Nombre, Descripción, Precio, Stock, Categoría y Activo.
3. El nombre es obligatorio. Precio y Stock son opcionales: si se dejan vacíos se guarda `NULL`, y si se escriben no pueden ser negativos.
4. Al guardar, la app asigna fecha y usuario de modificación.
5. Debe volver a la lista con **“Producto creado correctamente.”**

**Modificación**

1. Haz clic en **Editar**.
2. El formulario viene prellenado.
3. Cambia el precio o el stock y guarda.
4. Debe volver a la lista con **“Producto actualizado correctamente.”**

**Retiro**

1. Haz clic en **Eliminar**.
2. Se abre **“Eliminar Producto”** con la confirmación y los datos en solo lectura.
3. **Cancelar** no borra; **Eliminar** sí.
4. `TBLPRODUCTOS` no tiene llaves foráneas, así que normalmente el borrado no falla por vínculos.

### 9.4 Páginas informativas y entradas sin funcionalidad

- **Inicio, Acerca, Ayuda y Contacto** muestran solo su título, como en el PDF.
- **Categorias, facturas, Informes, Roles y Seguridad** muestran **“En construcción”**. **[COMPLEMENTO]**
- **Login** es solo visual, sin funcionalidad, como en el PDF.

---

## 10. Conceptos de la materia explicados con analogías

### Páginas estáticas vs dinámicas

- **Estática:** es un archivo que siempre muestra lo mismo; no consulta una base de datos.
- **Dinámica:** ejecuta código en el servidor y puede consultar la base de datos para armar la página.

Tu app es **dinámica**: cada vez que entras a Clientes, el modelo consulta MySQL y la tabla se arma con lo que hay en ese momento.

### Patrón de diseño MVC

MVC es una **plantilla de solución probada** para no empezar de cero. Separa tres responsabilidades:

| Capa | Qué hace | En este proyecto |
|---|---|---|
| **Modelo** | Conoce las tablas y habla con la base de datos | `models/` |
| **Vista** | Presenta la información al usuario | `views/` |
| **Controlador** | Es el intermediario: recibe, valida y decide | `controllers/` |

Analogía del restaurante:

- **Vista** = el menú y el plato que ve el cliente.
- **Controlador** = el mesero que toma el pedido y lo revisa.
- **Modelo** = la cocina y la despensa, que preparan y guardan.

### CRUD

**C**rear, **L**eer (leer/consultar), **U**pdate (actualizar) y **D**elete (eliminar). En la app: Nuevo, Lista, Editar y Eliminar.

### Validación (DataAnnotations en .NET)

En ASP.NET se usan atributos como `[Required]` o `[RegularExpression]`. Aquí la validación se hace en el controlador, antes de tocar la base de datos. **[COMPLEMENTO: equivalencia]**

| .NET | Equivalente en este proyecto |
|---|---|
| `Required` | `if texto(nombre) == "": errores[...] = "..."` |
| `Range` | `min_value` en `number_input` + validación de negativos |
| `StringLength` | `max_chars` en los `text_input` |
| `RegularExpression` | `PATRON_EMAIL` en `controllers/comun.py` |
| `DataType` | `date_input` para fechas, `number_input` para números |
| `CustomValidation` | funciones `validar_cliente`, `validar_empleado`, `validar_producto` |

### ORM, Entity Framework, LINQ, Razor y Helpers

Son tecnologías del enfoque .NET original:

- **Entity Framework / ORM:** traduce tablas a clases y evita escribir SQL.
- **LINQ:** un lenguaje de consulta común sobre colecciones.
- **Razor:** mezcla C# con HTML.
- **Helpers:** generan controles HTML.

Aquí se reemplazan por:

- **SQL parametrizado** escrito a mano en los modelos.
- **Diccionarios y funciones de Python** en vez de clases mapeadas.
- **Widgets de Streamlit** (`text_input`, `date_input`, `selectbox`, etc.) en vez de Razor/Helpers.

Se usó otra tecnología porque el profesor lo autorizó. **[COMPLEMENTO: equivalencia]**

### Seguridad básica

- **Autenticación:** login obligatorio antes de ver cualquier pantalla; el JWT se valida en cada recarga.
- **Autorización:** cada rol tiene una lista de páginas permitidas y se comprueba en el servidor.
- **Inyección SQL:** se evita con consultas parametrizadas (`%s` + tupla).
- **XSS:** todo texto que llega a HTML se escapa; las tablas escapan sus celdas por defecto.
- **CSRF:** las acciones de escritura usan formularios/botones de Streamlit con XSRF activo, no enlaces GET.
- **Fuerza bruta:** bloqueo temporal después de varios intentos fallidos.
- **Contraseñas:** solo se guardan hashes PBKDF2 con sal; nunca texto plano.
- **Borrado accidental:** se evita con pantalla de confirmación.
- **Credenciales:** viven en `secrets.toml`, fuera del código y del `.zip`.
- **`UPDATE`/`DELETE` sin `WHERE`:** aquí siempre llevan el id.

---

## 11. Errores frecuentes y cómo resolverlos

| Error o situación | Causa posible | Solución |
|---|---|---|
| Error de conexión al servidor | Servidor, puerto, usuario, contraseña o BD incorrectos | Revisar `secrets.toml` y probar con `python probar_conexion.py` |
| `Access denied for user` | Usuario sin permisos o sin acceso remoto | Pedir permisos o acceso desde la IP |
| `Can't connect to MySQL server` | Servidor caído, puerto 3306 cerrado o firewall | Verificar red/firewall (probar otra red) |
| `Unknown column` / `KeyError` al leer una columna | El nombre no coincide con el de la BD | Verificar nombres exactos con `DESCRIBE` |
| Errores por valores `NULL` | Se asume que el campo siempre trae valor | Convertir `None` antes de mostrar/guardar (helpers de `views/componentes.py`) |
| El `UPDATE`/`DELETE` no afecta registros | Falta el id o el `WHERE` | Verificar que el id viaje al controlador |
| No deja borrar un empleado | Está ligado a una factura o a seguridad | Mensaje claro; borrar uno sin vínculos |
| `ModuleNotFoundError: No module named 'streamlit'` | No se activó el entorno o no se instalaron dependencias | Activar `.venv` y `pip install -r requirements.txt` |
| `StreamlitSecretNotFoundError` o “Falta la configuración [mysql]” | No existe `.streamlit/secrets.toml` | Copiar `secrets.toml.example` y completar la contraseña |
| “Falta la sección [auth]” | No se ejecutó la configuración del login | `python configurar_auth.py init` |
| “Usuario o contraseña incorrectos” | Credenciales mal escritas | Revisar usuario y contraseña; el mensaje no revela si el usuario existe |
| “Demasiados intentos fallidos” | Se superó `max_intentos` | Esperar `bloqueo_minutos` o reiniciar la app para limpiar la memoria |
| El login no aparece / la app se queda en blanco | Error al leer `[auth]` o JWT inválido | Revisar la terminal y ejecutar `python configurar_auth.py validar` |
| “No tienes permiso para ver esta sección” | El rol no tiene esa página | Entrar con un rol adecuado o ajustar `PERMISOS` en `auth_controller.py` |
| `No se pudo conectar a MySQL` | Red, firewall, servidor o contraseña | Revisar `probar_conexion.py`, la red y el puerto 3306 |
| `No module named 'tomli'` en Python 3.10 | Faltan dependencias | `pip install -r requirements.txt` |
| El puerto 8501 está ocupado | Otra app usa el puerto | `streamlit run app.py --server.port 8502` |
| PowerShell no deja activar `.venv` | Política de ejecución | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| El correo se guarda vacío | Es opcional | Es correcto: si no se escribe, se guarda `""`; si se escribe, se valida el formato |
| El documento vacío no se guarda como 0 | Es opcional | Es correcto: se guarda `NULL`, no `0` |

---

## 12. Todo lo marcado como [COMPLEMENTO]

| Elemento | Por qué se agregó |
|---|---|
| Python + Streamlit + `mysql-connector-python` | Tecnología autorizada por el profesor; sin ORM, con SQL a mano |
| Navegación por `?page=...` en vez de `st.navigation` | Permite controlar el HTML del menú y los colores con más libertad |
| CSS en `views/estilos.py` | Streamlit no permite elegir por sí solo el color del menú lateral ni de cada botón |
| `config.py` | Centraliza textos y usuarios de auditoría configurables |
| `controllers/comun.py` | Evita repetir validaciones y conversiones |
| `views/componentes.py` | Evita repetir tablas, botones y mensajes |
| `views/en_construccion.py` | Las entradas sin funcionalidad muestran un aviso en vez de una página vacía |
| `tests/` | Pruebas de validaciones, modelos y pantallas |
| Confirmación antes de borrar en Empleados | El PDF borra directo, pero el manual de clientes pide confirmar; se aplicó a los tres CRUD |
| Opción **(Sin rol)** | `IdRolEmpleado` admite `NULL` |
| `max_chars` según la longitud real de la BD | Evita errores de “Data too long” |
| Documento como texto numérico | `bigint` puede ser más grande que un `int` normal |
| Mensajes de “guardado correctamente” | Mejora la experiencia; se muestran después de redirigir |
| Validación de correo en Empleados | Coherencia con la validación de Clientes |
| Mensajes de precio/stock inválidos | Validación del lado del servidor para Productos |
| Mensajes no definidos en el PDF: “El documento es obligatorio.”, “El documento debe ser numérico.”, “El precio no puede ser negativo.”, “El stock no puede ser negativo.”, “No hay empleados registrados.” y las confirmaciones de borrado de Empleados/Productos | El PDF no trae esos textos; se usan mensajes claros en español, coherentes con los de Clientes |
| Bandera `FOUND_ROWS` en MySQL | Permite que un `UPDATE` sin cambios reales siga contando como registro encontrado |
| `probar_conexion.py` lee `secrets.toml` | Evita credenciales escritas en el código |
| `models/usuario.py`, `controllers/auth_controller.py`, `views/login.py` y `views/seguridad.py` | Login con JWT, contraseñas con hash y permisos por rol |
| `configurar_auth.py` | Genera `[auth]`, hashes y usuarios sin editar TOML a mano |
| `PyJWT` en `requirements.txt` | Firma y validación del token JWT |
| `tests/test_seguridad.py` | Pruebas de contraseñas, JWT, permisos, XSS y SQL injection |
| Textos y etiquetas de Productos | El PDF no los define; se usan textos en español coherentes |
| Páginas “En construcción” | El PDF deja esas entradas sin pantalla |

---

## 13. Lo que se verificó en la base de datos real

Se ejecutó `DESCRIBE` contra `virtualaprendo.online` y se encontró lo siguiente.

### 13.1 Tablas existentes

```text
TBLCATEGORIA_PROD
TBLCLIENTES
TBLDETALLE_FACTURA
TBLEMPLEADO
TBLESTADO_FACTURA
TBLFACTURA
TBLPRODUCTO
TBLPRODUCTOS
TBLROLES
TBLSEGURIDAD
```

### 13.2 Estructura real de TBLPRODUCTOS

| Columna | Tipo | Nulo | Llave | Extra |
|---|---|---|---|---|
| `IdProducto` | `int(11)` | NO | PRI | auto_increment |
| `StrNombreProducto` | `varchar(200)` | NO | | |
| `StrDescripcion` | `text` | YES | | |
| `NumPrecio` | `decimal(18,2)` | YES | | |
| `NumStock` | `int(11)` | YES | | default 0 |
| `StrCategoria` | `varchar(100)` | YES | | |
| `BitActivo` | `tinyint(1)` | NO | | default 1 |
| `DtmFechaModifica` | `datetime` | YES | | |
| `StrUsuarioModifica` | `varchar(100)` | YES | | |

### 13.3 Diferencia importante: TBLPRODUCTO vs TBLPRODUCTOS

Existen **dos tablas distintas**:

- `TBLPRODUCTOS` (plural): la que pide la tarea y la que usa este proyecto.
- `TBLPRODUCTO` (singular): otra tabla, con columnas diferentes (`StrCodigo`, `NumPrecioCompra`, `NumPrecioVenta`, `IdCategoria`, etc.) y con llave foránea a `TBLCATEGORIA_PROD`.

**No se mezclaron.** El CRUD de Productos usa `TBLPRODUCTOS` tal como dice el enunciado.

### 13.4 Otros datos verificados

- `TBLROLES` tiene 5 filas: Gerente, Secretaria, Operario, Administrativo, programador.
- Al momento de la revisión: 18 clientes, 18 empleados, 4 productos, 5 roles y 10 facturas.
- `TBLFACTURA` tiene llaves foráneas hacia `TBLCLIENTES`, `TBLEMPLEADO` y `TBLESTADO_FACTURA`.
- `TBLSEGURIDAD` tiene llave foránea hacia `TBLEMPLEADO`.
- `TBLDETALLE_FACTURA` tiene llaves foráneas hacia `TBLFACTURA` y `TBLPRODUCTO` (singular).
- En la base, `TBLCLIENTES.StrNombre` admite `NULL`, pero la app lo exige obligatorio porque así lo pide el PDF. La validación del controlador manda.

---

## 14. Qué se probó y qué no

### Probado

- Conexión real a MySQL y `DESCRIBE` de `TBLPRODUCTOS`, `TBLEMPLEADO`, `TBLROLES` y `TBLCLIENTES`.
- Compilación de todos los archivos Python (`python -m compileall`).
- **18 pruebas de validaciones** (`tests/test_validaciones.py`): nombre obligatorio, correo, documento numérico, precio/stock, conversiones y normalización de datos (usuario de auditoría, fechas y valores NULL).
- **3 pruebas de CRUD real contra MySQL** (`tests/test_modelos_bd.py`): INSERT, SELECT, UPDATE y DELETE de clientes, empleados y productos. Se hicieron dentro de una transacción con **rollback**, así que no quedaron datos de prueba. Se verificó que los conteos seguían en 18/18/4 y que no había registros `ZZ ...`.
- **27 pruebas de seguridad** (`tests/test_seguridad.py`): hashes, JWT alterado/expirado, algoritmo `none`, permisos por rol, XSS, SQL injection y bloqueo por intentos.
- **14 pruebas de pantallas** (`tests/test_app.py`): login sin sesión, token inválido, Inicio, listas, formularios de nuevo, confirmación de eliminación, validación de nombre obligatorio, pantalla de Seguridad y modo solo lectura, sin excepciones.
- La app carga con `AppTest` usando la conexión real.
- El servidor Streamlit arrancó con `streamlit run app.py --server.headless true --server.port 8502`; `/_stcore/health` respondió **200 ok** y la página principal respondió **200**.
- Se probó el flujo completo de login, cierre de sesión y rechazo de una página sin permiso (`consulta` intentando abrir Empleados).

### No probado

- No se dejaron INSERT/UPDATE/DELETE guardados en la base del curso: se probaron con rollback para no alterar los datos de la clase.
- No se revisó el diseño píxel por píxel en un navegador con capturas; el CSS se escribió para Streamlit 1.36 y la app carga sin errores, pero conviene abrirla y ajustar si el profesor pide otro detalle visual.
- No se probó contra otra versión de MySQL distinta a la del servidor del curso.
- No se subió el `.zip` a Drive ni el video a YouTube: eso lo haces tú con el checklist.

---

## 15. Generar el `.zip` de entrega

Desde la carpeta del proyecto:

```powershell
powershell -ExecutionPolicy Bypass -File empaquetar.ps1
```

El script:

1. Copia el proyecto a una carpeta temporal.
2. Excluye `.venv`, `venv`, `__pycache__`, `.git`, `.pytest_cache` y `*.pyc`.
3. Elimina cualquier `secrets.toml` de la copia.
4. Genera `facturacion_streamlit.zip`.

Antes de subirlo, revisa que el `.zip` **no** contenga `.streamlit/secrets.toml`. Puedes comprobarlo abriendo el zip o con:

```powershell
python -c "import zipfile; print([n for n in zipfile.ZipFile('facturacion_streamlit.zip').namelist() if 'secrets' in n])"
```

Debe mostrar solo `secrets.toml.example` (o nada más que eso).

---

## 16. Checklist rápido antes de entregar

- [ ] `python probar_conexion.py` funciona.
- [ ] `streamlit run app.py` abre la app.
- [ ] Clientes: consulta, ingreso, modificación y retiro funcionan.
- [ ] Empleados: consulta, ingreso, modificación y retiro funcionan.
- [ ] Productos: consulta, ingreso, modificación y retiro funcionan.
- [ ] El `.zip` no incluye `secrets.toml` ni `.venv`.
- [ ] El video muestra los tres CRUD y la explicación del código.
- [ ] El link del video está en el formulario de entrega.

El guion del video y el checklist completo están en [`CHECKLIST_Y_GUION_VIDEO.md`](CHECKLIST_Y_GUION_VIDEO.md).
