# Rol y Responsabilidades: Israel (Controlador / Lógica y Memoria RAM)

---

## 1. Misión del Rol
Actuar como el núcleo inteligente y orquestador central del sistema "El Rincón Criollo". Israel conecta las pantallas construidas por Bolivar con las funciones de base de datos provistas por Jybran, asegurando cálculos financieros exactos mediante precisión decimal, validaciones estrictas con expresiones regulares y la gestión eficiente del pedido en memoria RAM.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas:
- `main.py` (Punto de entrada que arranca la aplicación e inicializa el ciclo de vida).
- `controllers/login_controller.py` (Gestión de autenticación y sesión activa en memoria).
- `controllers/cliente_controller.py` (Validaciones con expresiones regulares y flujo de clientes).
- `controllers/producto_controller.py` (Validación de reglas comerciales y carta criolla).
- `controllers/pedido_controller.py` (Manejo del carrito en RAM, sumas financieras y persistencia).
- `controllers/__init__.py`

### Pila Tecnológica a su Cargo:
- **`decimal (Decimal)`:** Módulo estándar indispensable para el procesamiento de importes monetarios. Se utiliza para multiplicar cantidades por precios unitarios y acumular el total general de cada comanda con exactitud aritmética absoluta, evitando los errores de redondeo y pérdida de céntimos propios de los números en coma flotante (`float`).
- **`re` (Expresiones Regulares):** Módulo estándar para auditar y filtrar cadenas de texto antes de transferirlas a la base de datos (por ejemplo: comprobar que el DNI conste rigurosamente de 8 caracteres numéricos, verificar formatos de números telefónicos y corroborar que los precios introducidos posean estructura numérica válida).
- **`datetime`:** Módulo estándar para registrar la marca temporal exacta del sistema (`datetime.now()`) al momento en que un pedido se consolida y cobra formalmente en caja.
- **Estructuras Nativas de Python (`list`, `dict`):** Administración del estado volátil del pedido en la memoria RAM. Modela el carrito temporal mediante listas de diccionarios donde cada elemento encapsula los datos del plato seleccionado, su cantidad, su nota especial y su subtotal computado.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Orquestación y Gestión de Sesión (`main.py` y `login_controller.py`):**
   - Arrancar la ventana de Login de Bolivar.
   - Validar que usuario y contraseña no estén vacíos.
   - Consultar al modelo de Jybran y, si las credenciales son válidas, **almacenar en memoria la sesión activa**: conservar el `id_usuario`, el nombre de usuario y su `rol`.
   - Inicializar el Dashboard y transferir a la vista la identidad del usuario para exhibirla en el encabezado.

2. **Validaciones Estrictas con Expresiones Regulares (`cliente_controller.py`):**
   - Utilizar el módulo `re` para garantizar que el DNI cumpla estrictamente con el patrón de 8 dígitos numéricos sin letras ni espacios.
   - Validar que el nombre no contenga caracteres inválidos y que el teléfono cuente con un formato reconocible.
   - En caso de anomalía, ordenar a la vista desplegar un cuadro emergente de error (`messagebox`).
   - En caso favorable, enviar los datos al modelo de Jybran y ordenar a la vista refrescar su tabla `Treeview`.

3. **Control Financiero de la Carta (`producto_controller.py`):**
   - Convertir y validar los precios usando el módulo `Decimal`.
   - Rechazar de forma preventiva cualquier valor menor o igual a cero.
   - Enviar al modelo el plato con su nombre, categoría, precio exacto y estado de disponibilidad.

4. **Motor de Comandas y Gestión en Memoria RAM (`pedido_controller.py`):**
   - **Administración del Carrito Temporal en RAM:**
     - Mantener una estructura de lista (`list`) de diccionarios (`dict`) que represente los ítems de la orden en curso.
     - Cada vez que el cajero añade un plato:
       - Validar que la cantidad sea un entero positivo.
       - Capturar la observación de cocina (`nota_plato`).
       - Multiplicar con `Decimal` la cantidad por el precio unitario para obtener el `subtotal` exacto.
       - Incorporar el diccionario al listado en RAM.
       - Recalcular el `total` sumando los subtotales de la lista con `Decimal`.
       - Enviar el detalle actualizado a la vista de Bolivar para renderizar la grilla `Treeview` y actualizar la etiqueta de cobro.
     - Al retirar un ítem del carrito: actualizar la lista en RAM, restar el subtotal y actualizar la interfaz.
   - **Consolidación y Cierre de la Transacción:**
     - Validar que el carrito cuente con productos, que se haya asignado el cliente, seleccionado el número de mesa y definido el método de pago.
     - Capturar la estampa de tiempo actual con `datetime.now()`.
     - Ensamblar la cabecera del pedido (incluyendo el `id_usuario` activo obtenido en el Login) y la lista detallada de platos.
     - Entregar la estructura a `pedido_model.py` para su guardado transaccional atómico en MySQL.
     - Al confirmarse el éxito, limpiar la lista en RAM, reiniciar los controles visuales e instruir a la vista la exhibición de un diálogo de confirmación de cobro.

---

## 4. Lo que NO DEBE hacer (Límites para no chocar con el equipo)

- **NO ejecutar código SQL directo:** Israel no redacta sentencias a MySQL; delega todo el acceso a datos a las funciones del modelo de Jybran.
- **NO construir widgets ni ventanas:** Israel no define botones, geometrías ni estilos de CustomTkinter. Esas responsabilidades pertenecen a Bolivar.
- **NO usar tipos `float` para dinero:** Todo cálculo de importes debe ejecutarse bajo `Decimal` para evitar discrepancias contables.
- **NO alterar archivos fuera de `controllers/` y `main.py`.**

---

## 5. Contrato de Integración
- **Con Bolivar:** Se conecta a los eventos de la interfaz, lee la información ingresada, invoca los diálogos de alerta (`messagebox`) y entrega los datos tabulares listos para dibujar en los `Treeview`.
- **Con Jybran:** Provee estructuras de datos consistentes y limpias para persistir en MySQL, y recibe los registros de base de datos para nutrir la navegación del sistema.
