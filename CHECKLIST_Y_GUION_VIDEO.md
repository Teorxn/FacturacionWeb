# CHECKLIST DE ENTREGA + GUION DEL VIDEO

## Parte A — Checklist de entrega

Marca cada punto antes de enviar.

### Proyecto

- [ ] `python probar_conexion.py` conecta y muestra las tablas.
- [ ] `python configurar_auth.py validar` confirma que `[auth]` está bien.
- [ ] `streamlit run app.py` abre la app sin errores.
- [ ] Sin sesión, la app muestra el **login** y no deja ver los CRUD.
- [ ] La barra superior muestra **FACTURACION**, Inicio, Acerca, Ayuda, Contacto y el usuario/rol de la sesión.
- [ ] El menú lateral tiene los grupos **TABLAS**, **FACTURAS** y **SEGURIDAD**.
- [ ] El pie muestra **Footer Text**.
- [ ] Clientes: lista, nuevo, editar y eliminar funcionan.
- [ ] Empleados: lista, nuevo, editar y borrar funcionan.
- [ ] Productos: lista, nuevo, editar y eliminar funcionan.
- [ ] Las validaciones muestran mensajes en rojo.
- [ ] La confirmación de borrado aparece antes de eliminar.
- [ ] Las páginas Inicio, Acerca, Ayuda y Contacto abren.
- [ ] Categorias, facturas, Informes y Roles muestran “En construcción”.
- [ ] La pantalla **Seguridad** muestra la sesión, el rol y los controles aplicados.
- [ ] Un usuario con rol `consulta` recibe “No tienes permiso” al abrir Empleados.

### Archivo `.zip`

- [ ] Se generó con `powershell -ExecutionPolicy Bypass -File empaquetar.ps1`.
- [ ] **No** contiene `.streamlit/secrets.toml`.
- [ ] **No** contiene `.venv`, `venv` ni `__pycache__`.
- [ ] Sí contiene `README.md`, `GUIA.md`, `CHECKLIST_Y_GUION_VIDEO.md`, `requirements.txt` y `secrets.toml.example`.
- [ ] Se subió a una carpeta de Drive y la carpeta está compartida con permiso de lectura.

Comprobación rápida del zip:

```powershell
python -c "import zipfile; print([n for n in zipfile.ZipFile('facturacion_streamlit.zip').namelist() if 'secrets' in n])"
```

Debe aparecer solo `secrets.toml.example`.

### Video

- [ ] Está publicado en YouTube (público o no listado, pero accesible con el link).
- [ ] Se ve la **consulta, el ingreso, la modificación y el retiro** de Empleados.
- [ ] Se ve la **consulta, el ingreso, la modificación y el retiro** de Clientes.
- [ ] Se ve la **consulta, el ingreso, la modificación y el retiro** de Productos.
- [ ] Se explica el código en orden **Modelo → Controlador → Vista**.
- [ ] Se menciona que se usó Python + Streamlit con autorización del profesor.
- [ ] Se muestra el login, el cierre de sesión y la pantalla de Seguridad.
- [ ] No se muestra la contraseña de la base de datos ni la contraseña del usuario.
- [ ] El link del video quedó en el formulario de entrega.

### Recomendaciones de grabación

El profesor recomienda:

- **Atube Catcher** (grabador de pantalla).
- Extensión de Chrome **“Live Screen Recorder”**.

También sirven OBS Studio, Xbox Game Bar (`Win + G`) o la grabadora de pantalla de Windows 11. Antes de grabar:

- Cierra notificaciones y pestañas que no uses.
- Sube el zoom del navegador si el texto se ve pequeño.
- Ten la app ya abierta y con la conexión probada.
- Crea datos de prueba con nombres como “Cliente video”, “Empleado video” y “Producto video”; bórralos al final si quieres dejar limpio.

---

## Parte B — Guion del video (10 minutos aproximados)

> Ajusta los tiempos a lo que pida el profesor. La idea es mostrar **funcionalidad + código**, no leer todo el proyecto.

### 0:00 – 0:30 | Presentación

Di algo como:

> “Buenos días. Soy [tu nombre]. Voy a presentar la tarea de aplicación web con acceso a datos aplicando el patrón MVC. La hice en Python con Streamlit, una tecnología autorizada por el profesor. El proyecto tiene los CRUD de Empleados, Clientes y Productos, con conexión a MySQL.”

Muestra la app abierta en el navegador.

### 0:30 – 1:15 | Recorrido general

Muestra:

- Barra superior con **FACTURACION**, Inicio, Acerca, Ayuda, Contacto y Login.
- Menú lateral con **TABLAS**, **FACTURAS** y **SEGURIDAD**.
- Pie de página **Footer Text**.
- Entra a **Inicio**, **Acerca**, **Ayuda** y **Contacto** (son informativas).
- Entra a **Categorias** y muestra “En construcción”.

Frase sugerida:

> “El layout sigue el diseño del PDF: barra superior oscura, menú lateral con los tres grupos y pie de página. Las páginas informativas solo muestran el título y las entradas que no tienen funcionalidad muestran un aviso.”

### 1:15 – 3:30 | CRUD Empleados (SEGURIDAD > Empleados)

1. Entra a **Empleados**. Muestra la lista **“ADMON EMPLEADOS”** y la tabla con Nombre, Documento, Telefono, Correo y ACCIONES.
2. **Consulta:** señala que los datos vienen de `TBLEMPLEADO` y que el rol se une con `TBLROLES`.
3. **Ingreso:** pulsa **+Nuevo**. Muestra el formulario en orden: Nombre, Nro Documento, Direccion, Telefono, Correo, ROL, Fecha Ingreso, Fecha retiro, Datos adicionales.
   - Deja el nombre vacío y pulsa **Guardar** para mostrar el mensaje rojo.
   - Completa los datos, elige un rol y guarda. Muestra el mensaje “Empleado creado correctamente.”
4. **Modificación:** pulsa **Editar** en el empleado nuevo, cambia el teléfono y guarda. Muestra “Empleado actualizado correctamente.”
5. **Retiro:** pulsa **Borrar**. Muestra la confirmación y los datos en solo lectura.
   - Primero pulsa **Cancelar** para demostrar que no borra.
   - Vuelve a entrar y pulsa **Eliminar** para borrar el empleado de prueba.

Frase sugerida:

> “El controlador valida en el servidor: nombre y documento obligatorios, documento numérico y correo con formato válido. Las fechas son opcionales y se guardan como NULL si se dejan vacías. Al guardar se actualiza la fecha y el usuario de auditoría ‘javier’.”

### 3:30 – 5:30 | CRUD Clientes (TABLAS > Clientes)

1. Entra a **Clientes**. Muestra **“Lista de Clientes”** y las columnas Id, Nombre, Documento, Teléfono, Email, Acciones.
2. **Consulta:** muestra la tabla. Si está vacía, aparece “No hay clientes registrados.”
3. **Ingreso:** pulsa **NUEVO**.
   - Pulsa **Guardar** sin nombre: aparece “El nombre es obligatorio.”
   - Escribe un correo inválido: aparece “El correo no tiene un formato válido.”
   - Corrige y guarda: “Cliente creado correctamente.”
4. **Modificación:** pulsa **Editar**, muestra que el formulario viene prellenado, cambia la dirección y guarda.
5. **Retiro:** pulsa **Eliminar**. Muestra el texto **“¿Está seguro de que desea eliminar este cliente?”** y los datos en solo lectura.
   - Pulsa **Cancelar**.
   - Vuelve y pulsa **Eliminar** para confirmar.

Frase sugerida:

> “El id del cliente viaja en la URL. Sin ese id, el UPDATE no sabría qué registro modificar. El DELETE solo se ejecuta después de la confirmación. Si el cliente tiene facturas, MySQL no deja borrarlo y la app muestra un mensaje claro.”

### 5:30 – 7:15 | CRUD Productos (TABLAS > Productos)

1. Entra a **Productos**. Muestra **“Lista de Productos”** y las columnas Id, Nombre, Categoría, Precio, Stock, Activo, Acciones.
2. **Consulta:** señala que se usa la tabla real `TBLPRODUCTOS`, no la tabla singular `TBLPRODUCTO`.
3. **Ingreso:** pulsa **NUEVO**, completa Nombre, Descripción, Precio, Stock, Categoría y Activo. Guarda.
4. **Modificación:** pulsa **Editar**, cambia el precio o el stock y guarda.
5. **Retiro:** pulsa **Eliminar**, muestra la confirmación, pulsa **Cancelar** y luego confirma el borrado.

Frase sugerida:

> “La tabla TBLPRODUCTOS tiene IdProducto, StrNombreProducto, StrDescripcion, NumPrecio, NumStock, StrCategoria, BitActivo y los campos de auditoría. El precio se maneja como decimal y el stock como entero. El nombre es obligatorio.”

### 7:15 – 9:15 | Explicación del código (orden M-V-C)

Abre el proyecto en VS Code y muestra estos archivos en este orden. No leas todo: explica para qué sirve cada uno.

#### 1. Modelo — `models/`

- `models/db.py`: “es la puerta única a MySQL; lee la configuración de `secrets.toml`”.
- `models/cliente.py`, `producto.py`, `empleado.py`: “cada uno conoce su tabla y tiene listar, obtener, insertar, actualizar y eliminar”.
- Señala una consulta y di: “uso `%s` y una tupla para evitar inyección SQL; nunca concateno valores”.
- Señala el `WHERE IdCliente = %s` y di: “sin el WHERE se modificarían o borrarían todos los registros”.
- `models/rol.py`: “solo llena el combo de roles”.

#### 2. Controlador — `controllers/`

- `controllers/clientes_controller.py`: “recibe los datos de la vista, valida en el servidor y decide si inserta o actualiza”.
- Muestra `validar_cliente` y explica las reglas: nombre obligatorio, correo con formato, documento numérico.
- Muestra `_normalizar`: “texto None se guarda como cadena vacía, documento vacío como NULL, fecha de modificación como ahora y usuario ‘Sistema’”.
- Muestra `guardar_cliente`: “devuelve (ok, mensaje) y captura errores de MySQL para mostrarlos en lenguaje claro”.
- Menciona `controllers/comun.py`: “utilidades compartidas para no repetir código”.

#### 3. Vista — `views/`

- `views/clientes.py`: “dibuja la lista, el formulario, la edición y la confirmación de borrado”.
- Muestra cómo se arma la tabla y cómo los botones Editar/Eliminar llevan `accion` e `id` en la URL.
- `views/componentes.py`: “tablas, botones y mensajes reutilizables”.
- `views/estilos.py`: “CSS para la barra oscura, el menú `#345863` y los botones por color”.
- `app.py`: “entrada, layout y navegación; decide qué vista mostrar según `page`”.

Frase sugerida:

> “El flujo es: el usuario hace clic, la vista dibuja, el controlador valida y llama al modelo, el modelo consulta MySQL, y la respuesta vuelve a la vista. Eso es MVC: cada capa tiene una responsabilidad.”

### 9:15 – 9:45 | Seguridad y detalles

Menciona:

- Consultas parametrizadas.
- `UPDATE` y `DELETE` con `WHERE` por id.
- Confirmación antes de eliminar.
- Contraseña en `secrets.toml`, fuera del código y del zip.
- Validación del lado del servidor.
- Manejo de `NULL`.

### 9:45 – 10:00 | Cierre

Di algo como:

> “Eso es todo. El proyecto incluye los tres CRUD, la guía de instalación, las pruebas y el checklist de entrega. Muchas gracias.”

---

## Parte C — Frases útiles si te preguntan

- **¿Por qué Streamlit y no ASP.NET?** “El profesor autorizó usar cualquier tecnología. La especificación funcional es la misma; cambié la tecnología, no los requisitos.”
- **¿Dónde está el MVC?** “En las carpetas `models`, `controllers` y `views`; `app.py` es la entrada y la navegación.”
- **¿Cómo evitas inyección SQL?** “Con consultas parametrizadas: `%s` y una tupla; nunca concateno valores.”
- **¿Qué pasa si se cae la base de datos?** “El modelo lanza un error controlado y la vista muestra un mensaje claro, no un error técnico.”
- **¿Por qué pides confirmación para borrar?** “Para evitar borrados accidentales; el PDF de empleados borra directo, pero el manual de clientes pide confirmación y lo apliqué a los tres.”
- **¿Qué pasa con los campos opcionales?** “Si están vacíos se guarda NULL en números y fechas, y cadena vacía en textos, siguiendo las reglas del manual.”
- **¿Por qué no usaste un ORM?** “El manual del profesor pide SQL escrito a mano y parametrizado; por eso usé `mysql-connector-python` sin ORM.”
- **¿Qué tabla usaste para productos?** “`TBLPRODUCTOS`, que es la que pide la tarea. Existe otra tabla `TBLPRODUCTO` en singular, pero es distinta y no se usó.”
