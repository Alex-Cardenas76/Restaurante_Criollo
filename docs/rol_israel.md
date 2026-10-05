# Rol y Responsabilidades: Israel (Controlador / Lógica y Memoria RAM)

---

## 1. Misión del Rol
Actuar como el núcleo inteligente y orquestador central del sistema "El Rincón Criollo". Israel conecta las pantallas construidas por Bolivar con las funciones de base de datos provistas por Jybran, asegurando cálculos financieros exactos mediante precisión decimal, validaciones rigurosas con expresiones regulares, administración del estado de ocupación de mesas, control del carrito de compras en memoria RAM, orquestación del flujo dual de comandas y cobros, y gestión del ciclo de vida de la carta de platos con protección de la integridad contable.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas Asignadas:
- `main.py` (Punto de entrada, arranque de la aplicación, enlace de vistas y sincronización de controladores).
- `controllers/login_controller.py` (Autenticación y retención de la sesión activa en memoria).
- `controllers/cliente_controller.py` (Validaciones con regex y orquestación del modal de clientes).
- `controllers/producto_controller.py` (CRUD completo de la carta criolla, control de precios en `Decimal`, conmutación de stock y protección contable).
- `controllers/pedido_controller.py` (Gestión del carrito en RAM, sumas financieras en `Decimal`, validación de mesas ocupadas/libres, flujo dual de comandas y cobro de cuentas desde el historial).
- `controllers/__init__.py`

### Pila Tecnológica a su Cargo:
- **`decimal (Decimal)`:** Módulo estándar obligatorio para todo cálculo monetario. Se utiliza para multiplicar cantidades por precios unitarios y acumular el total general de cada orden con exactitud matemática a 2 decimales, evitando las imprecisiones y pérdidas de céntimos de los números en coma flotante (`float`).
- **`re` (Expresiones Regulares):** Módulo estándar para auditar y filtrar cadenas de texto antes de enviarlas al modelo (validar DNI de 8 dígitos numéricos, teléfonos y cadenas sin caracteres prohibidos).
- **`datetime`:** Registro de la marca de tiempo oficial del sistema (`datetime.now()`) al momento de generar cualquier comanda o comprobante.
- **Estructuras Nativas de Python (`list`, `dict`):** Administración del estado volátil en la memoria RAM:
  - Carrito temporal modelado mediante lista de diccionarios `[{"id_producto", "nombre", "cantidad", "precio_unitario", "subtotal", "nota_plato"}]`.
  - Mapeo en memoria de clientes, platos disponibles y estado dinámico de mesas ocupadas.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Orquestación y Gestión de Sesión (`main.py` y `login_controller.py`):**
   - Inicializar la aplicación mostrando la ventana de Login.
   - Validar que los campos de usuario y clave no estén vacíos.
   - Consultar al modelo de Jybran y, si las credenciales son válidas, **retener en memoria la sesión activa**: conservar el `id_usuario`, el nombre de usuario y su `rol`.
   - Inicializar el Dashboard principal inyectando los controladores en cada pestaña y actualizando en el encabezado la identidad del usuario logueado.

2. **Validaciones Estrictas con Expresiones Regulares (`cliente_controller.py`):**
   - Validar que el DNI cumpla rigurosamente con el patrón de 8 dígitos numéricos (`^\d{8}$`).
   - Validar longitud mínima de nombres (al menos 3 caracteres) y formato telefónico.
   - Atender el guardado desde el modal `ModalFormularioCliente`, ordenar el refresco de la tabla `Treeview` y el cierre automático del modal tras el registro exitoso.

3. **Lógica Integral de la Carta y Protección Contable (`producto_controller.py`):**
   - **Registro de Platos:** Validar que el precio ingresado en el modal sea convertible a `Decimal` y estrictamente mayor a `0.00`.
   - **Edición de Platos:** Método `abrir_modal_editar()` para tomar la fila seleccionada en el `Treeview`, extraer sus datos y desplegar el modal de edición precargado. Al confirmar, procesar la actualización mediante `actualizar_producto`.
   - **Conmutación de Disponibilidad:** Método `conmutar_disponibilidad()` para alternar de forma inmediata el estado de un plato entre `Disponible` y `Agotado`.
   - **Eliminación con Protección Contable:** Método `eliminar_producto_seleccionado()`:
     - Consultar primero a `producto_tiene_pedidos()`.
     - Si el plato ya tiene ventas en el historial, **bloquear la eliminación** para no romper la integridad referencial de los balances pasados, orientando a marcarlo como `Agotado`.
     - Si el plato nunca se ha vendido, solicitar confirmación al usuario y proceder al borrado definitivo.

4. **Motor de Pedidos, Control de Mesas y Caja (`pedido_controller.py`):**
   - **Gestión del Carrito en RAM:**
     - Agregar platos al carrito validando que la cantidad sea un entero $\ge 1$.
     - Computar el subtotal exacto con `Decimal` ($\text{Subtotal} = \text{Cantidad} \times \text{Precio}$).
     - Sumar y recalcular el total general en tiempo real en la memoria RAM cada vez que se agregue o elimine un ítem.
   - **Control de Mesas Ocupadas vs Libres:**
     - Consultar periódicamente `obtener_mesas_ocupadas()` y poblar el selector de mesas indicando su estado: `Mesa 01 (Disponible)` o `Mesa 01 (Ocupada - Pedido #X)`.
     - Bloquear la apertura de cualquier pedido si la mesa seleccionada ya tiene una comanda con estado `Pendiente`.
   - **Flujo Dual (Guardar Comanda vs Cobrar al Instante):**
     - `Guardar Comanda (Pendiente)`: Registra el pedido en cocina con estado `Pendiente`. La mesa pasa a estar ocupada para que los comensales disfruten su comida.
     - `Cobrar al Instante (Pagado)`: Registra la venta de inmediato asignando el método de pago seleccionado, dejando la mesa libre.
   - **Módulo Historial de Ventas y Liquidación de Comandas:**
     - Cargar y mostrar todos los pedidos registrados en la tabla de historial.
     - Método `abrir_detalle_pedido()` para consultar en el modelo los platos consumidos y notas de cocina de una comanda y desplegarlos en el modal de detalle.
     - Método `confirmar_cobro_pendiente()`: Captura la modalidad de pago elegida en el modal de cobro, actualiza la orden a `Pagado` y **libera inmediatamente la mesa asociada**, actualizando la disponibilidad tanto en el historial como en la terminal de pedidos.

---

## 4. Lo que NO DEBE hacer (Límites Arquitectónicos)

- **NO ejecutar código SQL directo:** Israel no redacta sentencias SQL; delega todo el acceso a datos a las funciones del modelo de Jybran.
- **NO construir widgets ni maquetar ventanas:** Israel no define botones, geometrías ni estilos de CustomTkinter. Esas responsabilidades pertenecen a Bolivar.
- **NO usar tipos `float` para importes de dinero:** Todo cálculo monetario debe ejecutarse bajo `Decimal`.
- **NO alterar archivos fuera de `controllers/` y `main.py`.**

---

## 5. Contrato de Integración

- **Con Bolivar:** Se suscribe a los eventos de los botones, extrae la información de las cajas de texto mediante getters, invoca los diálogos modales y envía datos tabulares listos para dibujar en los `Treeview`.
- **Con Jybran:** Entrega parámetros validados, tipos de datos estrictos y listas de tuplas limpias para las transacciones en MySQL, y recibe los registros de base de datos para refrescar la interfaz.

---

## 6. Lista de Funciones y Criterios de Éxito al Culminar su Parte

Para considerar su módulo 100% culminado y operativo, Israel debe entregar implementadas y comprobadas las siguientes funciones y controladores:

### 1. Orquestador del Sistema (`main.py`):
* [x] `iniciar_aplicacion()`: Arranca la ventana de Login, conecta callbacks y transiciona al Dashboard sin pérdida de sesión.
* [x] Sincronización cruzada de controladores para recargar datos en caliente al cambiar de pestaña.

### 2. Controlador de Acceso (`controllers/login_controller.py`):
* [x] `manejar_login()`: Valida presencia de datos, consulta credenciales, retiene `sesion_activa` y transiciona al panel principal.
* [x] `cerrar_sesion()`: Limpia la sesión en memoria y devuelve al usuario a la pantalla de Login.

### 3. Controlador de Clientes (`controllers/cliente_controller.py`):
* [x] `cargar_clientes()`: Recupera los clientes desde el modelo y llena el `Treeview`.
* [x] `abrir_modal_nuevo()`: Despliega el formulario emergente para nuevos clientes.
* [x] `procesar_guardar_modal(datos, modal)`: Valida DNI con regex (`^\d{8}$`), nombres y teléfono, invoca a `insertar_cliente` y actualiza la vista.

### 4. Controlador de Productos (`controllers/producto_controller.py`):
* [x] `cargar_productos()`: Recupera la carta completa y actualiza la tabla de productos.
* [x] `abrir_modal_nuevo()` y `procesar_guardar_modal(datos, modal)`: Valida campos y precio en `Decimal`, e inserta el plato.
* [x] `abrir_modal_editar()` y `procesar_editar_modal(datos, modal)`: Precarga datos de la fila seleccionada, valida cambios y actualiza el plato.
* [x] `conmutar_disponibilidad()`: Alterna el estado entre `Disponible` y `Agotado` en tiempo real.
* [x] `eliminar_producto_seleccionado()`: Verifica historial con `producto_tiene_pedidos()`; si tiene ventas, bloquea el borrado; si no tiene, pide confirmación y elimina.

### 5. Controlador de Pedidos, Caja e Historial (`controllers/pedido_controller.py`):
* [x] `cargar_datos_iniciales()`: Carga clientes, platos disponibles y estado en vivo de mesas ocupadas/libres.
* [x] `agregar_plato_carrito()`: Valida cantidad positiva, nota especial, calcula subtotal exacto con `Decimal` y actualiza la tabla del carrito en RAM.
* [x] `quitar_plato_carrito()`: Remueve ítems de la lista en memoria y recalcula el total acumulado.
* [x] `procesar_pedido(estado_deseado)`:
  - Valida que el carrito no esté vacío.
  - Valida que la mesa seleccionada no esté ocupada por otra comanda pendiente.
  - Guarda en MySQL como `Pendiente` (ocupando mesa) o como `Pagado` (venta directa con mesa libre).
* [x] `cargar_historial()`: Puebla la tabla de historial de ventas con todos los comprobantes.
* [x] `abrir_detalle_pedido(info_pedido)`: Consulta los renglones consumidos de una orden y los muestra en el modal de detalle.
* [x] `iniciar_cobro_pedido(info_pedido)` y `confirmar_cobro_pendiente(...)`: Procesa el pago de comandas pendientes, actualiza a `Pagado`, captura método de pago y **libera automáticamente la mesa asociada**.
