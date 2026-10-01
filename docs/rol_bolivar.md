# Rol y Responsabilidades: Bolivar (Vista / Interfaz Gráfica)

---

## 1. Misión del Rol
Construir una interfaz de usuario visualmente moderna, intuitiva y ergonómica para "El Rincón Criollo". Bolivar es el responsable exclusivo de la apariencia estética del sistema, maquetando las pantallas, formularios, tablas interactivas y cuadros de diálogo utilizando el ecosistema de **CustomTkinter** y los componentes visuales nativos de Python.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas:
- `views/login_view.py` (Pantalla de inicio de sesión con branding).
- `views/dashboard_view.py` (Panel de navegación lateral/superior).
- `views/clientes_view.py` (Formulario y tabla interactiva de clientes).
- `views/productos_view.py` (Formulario de platos e inventario de la carta).
- `views/pedidos_view.py` (Terminal de caja, carrito temporal y cobranza).
- `views/__init__.py`

### Pila Tecnológica a su Cargo:
- **`customtkinter`:** Motor visual principal para crear ventanas modernas con soporte de temas claro/oscuro. Uso de:
  - `CTkFrame`: Para crear tarjetas y contenedores modulares ordenados.
  - `CTkEntry`: Para cajas de texto de captura de datos (con soporte de ocultamiento para contraseñas).
  - Botones estilizados (`CTkButton`) con colores representativos (acciones primarias, advertencias y cancelaciones).
  - `CTkOptionMenu` / `CTkComboBox`: Para menús desplegables de categorías de platos, selección de mesas y métodos de pago.
  - `CTkSwitch` / `CTkCheckBox`: Para alternar visualmente la disponibilidad de los platos de la carta.
- **`tkinter.ttk (Treeview)`:** Módulo nativo fundamental para construir grillas y tablas de datos con encabezados de columna y barras de desplazamiento (`Scrollbar`), indispensable para:
  - Visualizar la tabla de clientes frecuentes.
  - Visualizar la tabla de la carta criolla y su disponibilidad.
  - Renderizar el carrito de compras en la pantalla de pedidos (columnas: Plato, Cantidad, Nota/Instrucción, Precio Unitario y Subtotal).
- **`tkinter.messagebox`:** Módulo nativo para desplegar ventanas emergentes modales:
  - Notificaciones de error (campos incompletos, credenciales inválidas).
  - Diálogos de confirmación (preguntar antes de anular o retirar un ítem del pedido).
  - Avisos de éxito (confirmación de cliente guardado o pedido registrado en caja).
- **`Pillow / PIL` (Opcional):** Librería para procesar y renderizar imágenes con `CTkImage`, orientada a integrar el logotipo de "El Rincón Criollo" en el Login y logos/iconos en los accesos del menú lateral.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Maquetación Visual de Pantallas con CustomTkinter:**
   - **Login (`login_view.py`):** Integrar opcionalmente el logotipo mediante `Pillow / CTkImage`, campos de usuario y contraseña enmascarada, y botón de acceso.
   - **Dashboard (`dashboard_view.py`):** Estructurar un contenedor principal con menú lateral para navegar entre secciones y un encabezado que reserve el espacio visual para mostrar el usuario y rol activo.
   - **Clientes (`clientes_view.py`):** Formulario con `CTkEntry` para DNI, Nombres y Teléfono; junto a una tabla `ttk.Treeview` con scrollbar para listar los clientes registrados.
   - **Productos (`productos_view.py`):** Campos para nombre del plato, selector `CTkComboBox` de categoría, campo para el precio e interruptor `CTkSwitch` para el estado de disponibilidad; complementado con una tabla `ttk.Treeview` que liste toda la carta.
   - **Pedidos y Caja (`pedidos_view.py`):**
     - Selectores desplegables (`CTkOptionMenu`) para el cliente, el número de mesa y el método de pago (Efectivo, Yape, Tarjeta).
     - Selectores de platos y campo para notas especiales de cocina (`CTkEntry` para `nota_plato`).
     - Grilla `ttk.Treeview` que modele visualmente el carrito temporal con todas sus columnas.
     - Etiqueta de texto de alto contraste para el total a pagar y botón principal de cobranza.

2. **Manejo de Diálogos Emergentes (`tkinter.messagebox`):**
   - Implementar métodos dentro de las vistas para desplegar cuadros de alerta cuando el controlador se lo indique (por ejemplo: `mostrar_error(mensaje)`, `mostrar_exito(mensaje)`).

3. **Exposición de Métodos para el Controlador:**
   - Dejar métodos accesibles para que Israel pueda leer los valores ingresados, limpiar los formularios, poblar las tablas `Treeview` con nuevas filas y actualizar los valores numéricos de las etiquetas.

---

## 4. Lo que NO DEBE hacer (Límites para no chocar con el equipo)

- **NO importar conectores de base de datos ni escribir SQL:** La capa de vistas es totalmente ajena a MySQL y a los modelos.
- **NO realizar cálculos matemáticos:** No debe calcular multiplicaciones de precios ni sumas de subtotales en la vista. Los importes a mostrar en el `Treeview` o en el Total deben venir listos desde el controlador de Israel.
- **NO escribir lógica de validación:** La vista no decide si un DNI tiene 8 números o si un precio es inválido; esa labor le corresponde a las expresiones regulares y lógica de Israel.
- **NO modificar archivos fuera de `views/`.**

---

## 5. Contrato de Integración con el Controlador (Israel)
- Bolivar suministra las interfaces gráficas y los eventos de clic en los botones.
- La vista recibe listas de datos formateados para poblar los `Treeview` y textos listos para los cuadros de diálogo `messagebox`.
