# Rol y Responsabilidades: Jybran (Modelo / Base de Datos)

---

## 1. Misión del Rol
Garantizar la persistencia, integridad referencial y seguridad de la información del restaurante "El Rincón Criollo". Jybran es el responsable técnico de la administración del servidor de base de datos local y de la implementación de la capa de acceso a datos utilizando el driver oficial de MySQL para Python, proveyendo a las capas superiores métodos seguros, parametrizados y transaccionales para soportar todo el ciclo de comandas, catálogo de platos, auditoría de mesas y liquidación de ventas.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas Asignadas:
- `database/schema.sql` (Script DDL y datos iniciales de prueba).
- `database/conexion.py` (Módulo de conexión y gestión de sesiones con la base de datos mediante contexto seguro).
- `models/usuario_model.py` (Consultas preparadas para la entidad `USUARIOS`).
- `models/cliente_model.py` (Consultas preparadas para la entidad `CLIENTES`).
- `models/producto_model.py` (CRUD completo y verificación referencial de la entidad `PRODUCTOS`).
- `models/pedido_model.py` (Transacciones atómicas, consultas de historial, cobro y estado de mesas para `PEDIDOS` y `DETALLE_PEDIDOS`).
- `models/__init__.py`

### Pila Tecnológica a su Cargo:
- **`mysql-connector-python`:** Conector oficial para gestionar la conexión (`connect`), la creación de cursores para ejecución de sentencias SQL preparadas usando marcadores de posición seguros (`%s`), y la confirmación o reversión de transacciones (`commit()` y `rollback()`).
- **`mysql.connector.errors`:** Submódulo para atrapar y gestionar excepciones nativas del motor (interrupción del servicio en XAMPP, error de autenticación, o violación de clave única en caso de DNI duplicado).
- **`MySQL Server` (Servicio local vía XAMPP):** Motor relacional donde se ejecutan y almacenan físicamente las tablas del restaurante.
- **`phpMyAdmin` / `MySQL Workbench`:** Plataformas visuales para la ejecución del script `schema.sql`, verificación de llaves foráneas y auditoría de los datos insertados.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Administración y Creación del Esquema Relacional (`schema.sql`):**
   - Diseñar y auditar la creación de las 5 tablas relacionales del negocio:
     - `usuarios`: `id`, `nombre` (VARCHAR UNIQUE), `contrasena`, `rol` ('administrador', 'vendedor').
     - `clientes`: `id`, `nombre`, `dni` (VARCHAR(8) UNIQUE), `telefono`.
     - `productos`: `id`, `nombre` (VARCHAR UNIQUE), `categoria`, `precio` (DECIMAL(10,2)), `disponible` (BOOLEAN).
     - `pedidos`: `id`, `fecha` (DATETIME), `cliente_id` (FK), `usuario_id` (FK), `mesa` (VARCHAR(20)), `total` (DECIMAL(10,2)), `metodo_pago` (VARCHAR(20)), `estado` ('Pendiente', 'Pagado').
     - `detalle_pedidos`: `id`, `pedido_id` (FK), `producto_id` (FK), `cantidad` (INT), `precio_unitario` (DECIMAL(10,2)), `subtotal` (DECIMAL(10,2)), `nota_plato` (VARCHAR(150)).
   - Incorporar datos iniciales de prueba (usuarios administrador y vendedor, cliente genérico y platos criollos base).

2. **Gestión de la Conexión y Control de Fallas (`conexion.py`):**
   - Centralizar los parámetros de conexión hacia el MySQL local de XAMPP (host, puerto, usuario, clave y base de datos) usando un administrador de contexto seguro (`with conexion_segura() as conexion:`).
   - Manejar excepciones de conexión atrapando caídas de XAMPP para retornar mensajes descriptivos y evitar cierres abruptos de la aplicación.

3. **Desarrollo de Modelos con Consultas Parametrizadas (`models/`):**
   - **Uso estricto de consultas preparadas (`%s`):** Prohibida la concatenación de texto para prevenir inyecciones SQL.
   - **`usuario_model.py`:** Autenticación de credenciales y consulta de usuarios.
   - **`cliente_model.py`:** Registro y listado de clientes, controlando la restricción de DNI único.
   - **`producto_model.py` (Gestión Integral de Carta):**
     - Inserción de platos con categoría, precio decimal y disponibilidad.
     - Listado completo de la carta y listado filtrado de solo disponibles para caja.
     - Modificación de disponibilidad interactiva (`disponible = True/False`).
     - Actualización dinámica de platos (nombre, categoría, precio).
     - Eliminación física de platos y función de protección referencial que consulte si el plato existe en `detalle_pedidos`.
   - **`pedido_model.py` (Transaccionalidad, Mesas e Historial):**
     - Registro atómico de comanda: inserción de cabecera (`pedidos`) y detalle (`detalle_pedidos`) bajo transacción (`commit`/`rollback`), soportando tanto estado `Pendiente` (comanda de cocina) como `Pagado` (venta directa).
     - Consulta de historial general de pedidos vinculando nombres de cliente y cajero.
     - Consulta del detalle de platos y notas de cocina de un pedido específico.
     - Función para cobrar comandas pendientes registrando el método de pago y cambiando el estado a `Pagado`.
     - Consulta relacional de mesas ocupadas para informar al controlador qué mesas tienen pedidos pendientes activos.

---

## 4. Lo que NO DEBE hacer (Límites Arquitectónicos)

- **NO utilizar CustomTkinter ni librerías de interfaz:** Jybran no crea ventanas, marcos, botones ni importa widgets.
- **NO calcular subtotales ni totales financieros:** Los importes numéricos deben venir ya procesados con `Decimal` desde el controlador de Israel.
- **NO hacer validaciones de formato de interfaz:** Validar si un DNI tiene 8 números o si una caja de texto está vacía es labor de Israel antes de invocar al modelo.
- **NO alterar archivos fuera de `database/` y `models/`.**

---

## 5. Contrato de Integración con el Controlador (Israel)

- Jybran recibe parámetros desempaquetados, validados y limpios desde el controlador.
- Devuelve tuplas o listas de tuplas directamente consumibles por los controladores, o valores booleanos/IDs autogenerados en operaciones de escritura.
- En caso de error de MySQL (como clave duplicada o desconexión), captura la excepción y la comunica limpiamente al controlador sin detener el programa.

---

## 6. Lista de Funciones y Criterios de Éxito al Culminar su Parte

Para considerar su módulo 100% culminado y operativo, Jybran debe entregar implementadas y comprobadas las siguientes funciones:

### Módulo de Conexión (`database/conexion.py`):
* [x] `conexion_segura()`: Context manager que abre la conexión con MySQL, la entrega al bloque `with` y garantiza el cierre seguro del cursor y la conexión al terminar o ante cualquier error.

### Módulo de Usuarios (`models/usuario_model.py`):
* [x] `obtener_usuario_por_nombre(nombre)`: Retorna `(id, nombre, contrasena, rol)` para el login o `None` si no existe.
* [x] `insertar_usuario(nombre, contrasena, rol)`: Inserta un nuevo usuario en la base de datos.
* [x] `listar_usuarios()`: Devuelve el listado de usuarios del personal con sus roles.

### Módulo de Clientes (`models/cliente_model.py`):
* [x] `insertar_cliente(nombre, dni, telefono)`: Registra un cliente retornando su `id` generado o controlando error de duplicidad.
* [x] `listar_clientes()`: Retorna todos los clientes registrados ordenados alfabéticamente.
* [x] `obtener_cliente_por_dni(dni)`: Busca y devuelve los datos de un cliente dado su DNI de 8 dígitos.

### Módulo de Productos (`models/producto_model.py`):
* [x] `insertar_producto(nombre, categoria, precio, disponible)`: Inserta un nuevo plato criollo y devuelve su `id`.
* [x] `listar_productos()`: Retorna todo el catálogo de platos (para la vista de administración de productos).
* [x] `listar_productos_disponibles()`: Retorna únicamente los platos con `disponible = TRUE` (para la vista de pedidos/caja).
* [x] `actualizar_disponibilidad(producto_id, disponible)`: Cambia el estado de un plato entre disponible y agotado.
* [x] `actualizar_producto(producto_id, nombre, categoria, precio, disponible)`: Modifica datos o precios de un plato existente.
* [x] `eliminar_producto(producto_id)`: Elimina el registro del plato de la base de datos.
* [x] `producto_tiene_pedidos(producto_id)`: Consulta si el plato está registrado en `detalle_pedidos` para proteger la integridad contable antes de borrarlo.

### Módulo de Pedidos y Caja (`models/pedido_model.py`):
* [x] `insertar_pedido(cliente_id, usuario_id, mesa, metodo_pago, total, detalles, estado)`: Transacción atómica todo o nada con `commit()` y `rollback()`, soportando estados `'Pendiente'` y `'Pagado'`.
* [x] `listar_pedidos()`: Devuelve el historial general de comprobantes con fecha, mesa, cliente, total, método de pago y estado.
* [x] `listar_detalle_pedido(pedido_id)`: Retorna los renglones consumidos de un pedido (nombre plato, cantidad, precio, subtotal, nota de cocina).
* [x] `pagar_pedido(pedido_id, metodo_pago)`: Actualiza una comanda pendiente a `'Pagado'` y asocia la modalidad de cobro.
* [x] `obtener_mesas_ocupadas()`: Devuelve un diccionario `{mesa: id_pedido}` de todas las mesas que tienen una comanda en estado `'Pendiente'`.
