# Rol y Responsabilidades: Jybran (Modelo / Base de Datos)

---

## 1. Misión del Rol
Garantizar la persistencia, integridad referencial y seguridad de la información del restaurante "El Rincón Criollo". Jybran es el responsable técnico de la administración del servidor de base de datos local y de la implementación de la capa de acceso a datos utilizando el driver oficial de MySQL para Python.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas:
- `database/schema.sql` (Script DDL y datos iniciales de prueba).
- `database/conexion.py` (Módulo de conexión y gestión de sesiones con la base de datos).
- `models/usuario_model.py` (Consultas preparadas para la entidad `USUARIOS`).
- `models/cliente_model.py` (Consultas preparadas para la entidad `CLIENTES`).
- `models/producto_model.py` (Consultas preparadas para la entidad `PRODUCTOS`).
- `models/pedido_model.py` (Transacciones atómicas para `PEDIDOS` y `DETALLE_PEDIDOS`).
- `models/__init__.py`

### Pila Tecnológica a su Cargo:
- **`mysql-connector-python`:** Conector oficial para gestionar la conexión (`connect`), la creación de cursores para ejecución de sentencias SQL preparadas usando marcadores de posición seguros (`%s`), y la confirmación o reversión de transacciones (`commit()` y `rollback()`).
- **`mysql.connector.errors`:** Submódulo para atrapar y gestionar excepciones nativas del motor (por ejemplo: interrupción del servicio en XAMPP, error de autenticación, o violación de clave única en caso de DNI duplicado).
- **`MySQL Server` (Servicio local vía XAMPP):** Motor relacional donde se ejecutan y almacenan físicamente las tablas del restaurante.
- **`MySQL Workbench` / `phpMyAdmin`:** Plataformas visuales para la ejecución del script `schema.sql`, verificación de llaves foráneas y auditoría de los datos insertados.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Administración y Creación del Esquema Relacional (`schema.sql`):**
   - Ejecutar y auditar en `phpMyAdmin` o `MySQL Workbench` la creación de las 5 tablas relacionales:
     - `USUARIOS`: `id_usuario`, `usuario`, `clave`, `rol`.
     - `CLIENTES`: `id_cliente`, `dni`, `nombres`, `telefono`.
     - `PRODUCTOS`: `id_producto`, `nombre`, `categoria`, `precio` (tipo decimal), `disponible` (tipo boolean/tinyint).
     - `PEDIDOS`: `id_pedido`, `fecha` (datetime), `id_cliente`, `id_usuario`, `numero_mesa`, `total` (decimal), `metodo_pago`, `estado`.
     - `DETALLE_PEDIDOS`: `id_detalle`, `id_pedido`, `id_producto`, `cantidad`, `precio_unitario` (decimal), `subtotal` (decimal), `nota_plato`.
   - Incorporar datos de prueba iniciales (un usuario cajero/administrador, clientes y platos tradicionales con disponibilidad activa).

2. **Gestión de la Conexión y Control de Fallas (`conexion.py`):**
   - Centralizar los parámetros de conexión hacia el MySQL local de XAMPP (host, puerto, usuario, clave y base de datos).
   - Utilizar `mysql.connector.errors` para atrapar caídas de XAMPP y retornar mensajes descriptivos si el servicio no está levantado, evitando que la aplicación se cierre abruptamente.

3. **Desarrollo de Modelos con Consultas Preparadas (`models/`):**
   - **Uso estricto de consultas preparadas (`%s`):** Ninguna sentencia SQL debe concatenar cadenas de texto; todos los parámetros que provengan del exterior deben ser inyectados mediante tuplas a través de los marcadores `%s` del cursor.
   - **`usuario_model.py`:** Consulta que valide credenciales y retorne los datos del usuario (`id_usuario`, `usuario`, `rol`).
   - **`cliente_model.py`:** Inserción y consulta de clientes; atrapar excepciones de DNI duplicado para alertar a la capa superior.
   - **`producto_model.py`:** Consulta de la carta general y consulta filtrada de platos con `disponible = True` para abastecer la toma de comandas.
   - **`pedido_model.py` (Manejo Transaccional):**
     - Iniciar la transacción para registrar el pedido.
     - Insertar la cabecera en `PEDIDOS`, recuperar el `id_pedido` autogenerado.
     - Insertar los ítems en `DETALLE_PEDIDOS` vinculados al pedido.
     - Aplicar `commit()` si todas las operaciones resultan exitosas, o ejecutar `rollback()` inmediato si ocurre algún error para evitar datos huérfanos o inconsistencias.

---

## 4. Lo que NO DEBE hacer (Límites para no chocar con el equipo)

- **NO utilizar CustomTkinter ni librerías gráficas:** Jybran no crea ventanas ni importa componentes visuales.
- **NO calcular los importes:** Los valores de `subtotal` y `total` deben venir ya calculados con precisión desde el controlador de Israel.
- **NO hacer validaciones de interfaz:** La verificación de si una caja de texto está vacía o si el formato del DNI es correcto es labor de Israel antes de tocar el modelo.
- **NO alterar archivos fuera de `database/` y `models/`.**

---

## 5. Contrato de Integración con el Controlador (Israel)
- Jybran recibe parámetros empaquetados y limpios desde el controlador.
- Devuelve datos limpios (listas de diccionarios o tuplas) o indicadores booleanos de éxito/fracaso, reportando errores capturados desde `mysql.connector.errors`.
