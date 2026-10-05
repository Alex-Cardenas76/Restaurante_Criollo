# Rol y Responsabilidades: Bolivar (Vista / Interfaz Gráfica)

---

## 1. Misión del Rol
Construir una interfaz de usuario visualmente moderna, intuitiva y ergonómica para "El Rincón Criollo". Bolivar es el responsable exclusivo de la apariencia estética del sistema, maquetando las pantallas, formularios modales independientes, tablas interactivas y cuadros de diálogo utilizando el ecosistema de **CustomTkinter** y los componentes visuales nativos de Python, garantizando un flujo de trabajo ágil tanto para la atención en salón como para el despacho rápido en caja.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas Asignadas:
- `views/login_view.py` (Pantalla de acceso y autenticación).
- `views/dashboard_view.py` (Marco contenedor con menú lateral de navegación y encabezado de usuario activo).
- `views/clientes_view.py` (Tabla interactiva de clientes y ventana modal `ModalFormularioCliente`).
- `views/productos_view.py` (Catálogo de la carta, barra de herramientas CRUD y modal `ModalFormularioProducto`).
- `views/pedidos_view.py` (Punto de venta y comanda: carrito en RAM, selector de mesas con estado y acciones duales).
- `views/historial_pedidos_view.py` (Módulo de historial de ventas, modal de auditoría de comanda y modal de cobro).
- `views/__init__.py`

### Pila Tecnológica a su Cargo:
- **`customtkinter`:** Motor visual principal para crear ventanas modernas con soporte de temas claro/oscuro:
  - `CTkFrame`: Para agrupar paneles, barras de herramientas y contenedores modulares.
  - `CTkToplevel`: Para la construcción de formularios modales emergentes y centrados sobre la ventana principal (`grab_set`, `transient`).
  - `CTkEntry`: Cajas de texto con placeholder para captura de datos y contraseñas ocultas.
  - `CTkButton`: Botones ergonómicos de gran escala (`height=44`), con tipografía destacada y código de colores semántico (verde para guardar/cobrar, naranja/amarillo para comanda/disponibilidad, azul para editar, rojo para eliminar/cerrar sesión y gris para cancelar).
  - `CTkComboBox`: Desplegables para selección de mesas con estado en tiempo real, categorías de platos y modalidades de pago.
  - `CTkSwitch`: Interruptor interactivo para activar o desactivar la disponibilidad de platos.
- **`tkinter.ttk (Treeview)`:** Tablas con encabezados de columna y barras de desplazamiento (`Scrollbar`) para clientes, productos criollos, carrito de compras e historial general de ventas.
- **`tkinter.messagebox`:** Diálogos nativos de información, advertencia, error y confirmación (`askyesno`).

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Diseño de Formularios Modales Desacoplados (`CTkToplevel`):**
   - Evitar saturar las pantallas principales amontonando cajas de texto junto a las tablas.
   - Construir ventanas emergentes modales independientes, centradas con respecto a la ventana padre y con bloqueo modal (`grab_set`):
     - `ModalFormularioCliente`: Para registrar nuevos comensales con campos de DNI, Nombres, Teléfono y botones de acción cómodos.
     - `ModalFormularioProducto`: Modal reutilizable para registrar y **editar platos existentes**, precargando automáticamente nombre, categoría, precio y switch de disponibilidad cuando se trate de una edición.
     - `ModalCobrarPedido`: Modal que exhibe el número de comanda, mesa, cliente y monto total a pagar, solicitando el método de pago para confirmar la liquidación.
     - `ModalDetalleComanda`: Modal con tabla que exhibe los platos consumidos y observaciones especiales de cocina de una orden seleccionada.

2. **Maquetación de Pantallas Principales con CustomTkinter:**
   - **Login (`login_view.py`):** Tarjeta centralizada con campos de usuario, contraseña enmascarada y botón de ingreso.
   - **Dashboard (`dashboard_view.py`):** Panel lateral con accesos directos (*Caja*, *Historial de Ventas*, *Clientes*, *Productos*, *Cerrar Sesión*) y cabecera que refleje dinámicamente el usuario y rol en sesión.
   - **Clientes (`clientes_view.py`):** Vista despejada con barra superior, botón `+ Nuevo Cliente` y grilla completa `Treeview` para visualizar a los clientes.
   - **Productos (`productos_view.py`):** Vista de catálogo con tabla amplia y barra superior de herramientas con acciones completas: `+ Nuevo Plato`, `✏️ Editar Plato`, `🔄 Disponibilidad` y `🗑️ Eliminar`.
   - **Pedidos / Caja (`pedidos_view.py`):**
     - Selector de mesas amplio (210 px) que muestre la disponibilidad en vivo (`Mesa 01 (Disponible)` vs `Mesa 01 (Ocupada - Pedido #X)`).
     - Desplegables de clientes y métodos de pago.
     - Selector de platos disponibles, cantidad y campo para notas de cocina (`nota_plato`).
     - Grilla `Treeview` para visualizar el carrito temporal con botón para remover platos seleccionados.
     - Etiqueta de total destacado y botonera de doble acción:
       - Botón `📝 Guardar Comanda (Pendiente)` para enviar la orden a cocina y ocupar la mesa.
       - Botón `💳 Cobrar al Instante (Pagado)` para ventas de paso o cobro inmediato.
   - **Historial de Ventas (`historial_pedidos_view.py`):** Grilla completa de ventas con botón para ver el detalle de consumo y botón para cobrar comandas pendientes.

3. **Exposición de Métodos Limpios para el Controlador:**
   - Implementar métodos de lectura (`get_cliente_seleccionado()`, `get_mesa()`, `get_producto_seleccionado()`), métodos de llenado de tablas (`poblar_tabla()`, `poblar_carrito()`, `poblar_mesas()`) y métodos de notificación (`mostrar_error()`, `mostrar_exito()`, `confirmar_accion()`).

---

## 4. Lo que NO DEBE hacer (Límites Arquitectónicos)

- **NO importar conectores de base de datos ni escribir SQL:** Prohibido importar `mysql.connector` o invocar directamente a los modelos.
- **NO realizar cálculos matemáticos:** No debe calcular multiplicaciones de precios, subtotales ni acumulación de totales; todos los números deben provenir calculados desde el controlador de Israel.
- **NO escribir lógica de validación de negocio:** La comprobación de DNI de 8 dígitos, el formato de precio o la verificación de mesas ocupadas es labor de Israel.
- **NO alterar archivos fuera de `views/`.**

---

## 5. Contrato de Integración con el Controlador (Israel)

- Bolivar diseña los componentes y asigna callbacks o eventos en los botones para que el controlador los escuche.
- La vista recibe colecciones formateadas listas para llenar los `Treeview` y cadenas de texto listas para mostrar en los diálogos `messagebox`.

---

## 6. Lista de Vistas, Componentes y Criterios de Éxito al Culminar su Parte

Para considerar su módulo 100% culminado y operativo, Bolivar debe entregar implementados y comprobados los siguientes componentes:

### 1. Módulo de Autenticación (`views/login_view.py`):
* [x] Formulario de login centrado con título, campos de texto estilizados (`usuario`, `contrasena` oculta) y botón de acceso.
* [x] Métodos `get_usuario()`, `get_password()`, `limpiar()`, `mostrar_error()`.

### 2. Estructura Principal (`views/dashboard_view.py`):
* [x] Menú lateral de navegación con botones para alternar entre Caja, Historial, Clientes, Productos y Cerrar Sesión.
* [x] Encabezado superior con etiqueta dinámica para exhibir usuario y rol autenticado.
* [x] Contenedor principal adaptable para hospedar las diferentes vistas sin parpadeos.

### 3. Módulo de Clientes (`views/clientes_view.py`):
* [x] Tabla `Treeview` con scrollbar para visualizar ID, Nombres, DNI y Teléfono.
* [x] Botón `+ Nuevo Cliente` que abre la ventana modal.
* [x] Modal `ModalFormularioCliente` (`CTkToplevel`) centrado con campos amplios y botones grandes (`Cancelar` y `Guardar Cliente`).

### 4. Módulo de Carta y Catálogo (`views/productos_view.py`):
* [x] Tabla `Treeview` con columnas para ID, Plato, Categoría, Precio y Disponibilidad.
* [x] Barra de herramientas superior con botones: `+ Nuevo Plato`, `✏️ Editar Plato`, `🔄 Disponibilidad` y `🗑️ Eliminar`.
* [x] Modal `ModalFormularioProducto` (`CTkToplevel`) con soporte dual: creación y edición precargada de datos.
* [x] Diálogos nativos de confirmación para eliminación y alertas de estado.

### 5. Terminal de Pedidos y Caja (`views/pedidos_view.py`):
* [x] Selector desplegable de mesas de 210 px de ancho con formato de estado libre/ocupado.
* [x] Selectores de clientes y método de pago.
* [x] Selector de platos disponibles, campo de cantidad y entrada para notas especiales de cocina.
* [x] Grilla `Treeview` para el carrito temporal (Plato, Cantidad, Nota, P. Unitario, Subtotal) con botón para quitar platos.
* [x] Etiqueta destacada de Total a pagar.
* [x] Botones de acción duales: `📝 Guardar Comanda (Pendiente)` y `💳 Cobrar al Instante (Pagado)`.

### 6. Módulo Historial de Ventas (`views/historial_pedidos_view.py`):
* [x] Tabla `Treeview` con todos los pedidos (N° Pedido, Fecha, Mesa, Cliente, Cajero, Total, Método de Pago, Estado).
* [x] Botón `🔍 Ver Detalle de Comanda` que despliega el modal `ModalDetalleComanda` con los platos y notas de cocina de la orden.
* [x] Botón `💳 Cobrar Pedido Pendiente` que despliega el modal `ModalCobrarPedido` para seleccionar método de pago y liquidar la comanda.
