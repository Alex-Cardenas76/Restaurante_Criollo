# Reglas de Negocio: El Rincón Criollo

Este documento establece las **reglas operativas y de validación obligatorias** para todo el equipo de desarrollo (Jybran, Bolivar, Israel y Alex). Su objetivo es garantizar que la vista, el controlador y la base de datos se comporten de forma idéntica y sin ambigüedades.

---

## 1. Módulo de Acceso y Seguridad (`USUARIOS`)

* **RN-ACC-01 (Campos obligatorios):** El campo `usuario` y el campo `clave` son estrictamente obligatorios. No se permite intentar ingresar con campos en blanco o solo espacios.
* **RN-ACC-02 (Validación de credenciales):** El acceso se concede únicamente si existe coincidencia exacta entre el usuario y la clave registrada en la base de datos.
* **RN-ACC-03 (Trazabilidad de sesión):** Una vez autenticado, el sistema debe retener en memoria el `id_usuario`, el nombre de usuario y su `rol`. Este identificador se vinculará obligatoriamente a cada venta que se procese durante el turno.
* **RN-ACC-04 (Manejo de errores):** Si las credenciales no coinciden, se muestra un mensaje claro: *"Usuario o contraseña incorrectos"*, limpiando el campo de contraseña pero conservando el nombre de usuario escrito.

---

## 2. Módulo de Clientes (`CLIENTES`)

* **RN-CLI-01 (Formato estricto del DNI):** El `dni` debe constar exactamente de **8 dígitos numéricos**. No se permiten letras, espacios, guiones ni longitudes distintas de 8.
* **RN-CLI-02 (Unicidad de cliente):** No pueden existir dos clientes registrados con el mismo DNI en el sistema. Si se intenta registrar un DNI ya existente, el sistema debe avisar: *"El DNI ya se encuentra registrado"*.
* **RN-CLI-03 (Nombres obligatorios):** El campo `nombres` debe tener al menos 3 caracteres y no puede contener únicamente números o espacios vacíos.
* **RN-CLI-04 (Teléfono):** Debe ser numérico y contar con **9 dígitos** (estándar móvil).
* **RN-CLI-05 (Cliente Genérico / Venta Rápida):** En la base de datos debe existir un cliente por defecto para ventas al paso (ej. DNI: `00000000`, Nombres: `Clientes Varios / Público General`), para permitir despachos sin obligar a registrar a un cliente nuevo si no lo desea.

---

## 3. Módulo de Productos Criollos (`PRODUCTOS`)

* **RN-PRO-01 (Nombre único y obligatorio):** Cada plato de la carta debe contar con un nombre descriptivo no vacío y no repetido (ej. "Lomo Saltado", "Ají de Gallina", "Ceviche Mixto").
* **RN-PRO-02 (Precio positivo):** El campo `precio` debe ser numérico decimal, mayor a cero (`precio > 0.00`). No se permiten platos con precio S/ 0.00 ni valores negativos.
* **RN-PRO-03 (Categorías definidas):** Todo producto debe pertenecer a una de las categorías fijas de la carta criolla:
  - *Entradas*
  - *Platos de Fondo*
  - *Guarniciones*
  - *Bebidas*
  - *Postres*
* **RN-PRO-04 (Regla de Disponibilidad en Carta):**
  - Todo producto tiene un estado `disponible` (Sí / No).
  - **Solo los platos con disponibilidad activa (`disponible = True`) aparecen en la pantalla de pedidos** para ser seleccionados por el cajero.
  - Si un plato se agota en cocina, se cambia su estado a no disponible; el plato no se borra de la base de datos (para no romper el historial de ventas anteriores), pero queda bloqueado para nuevas ventas.

---

## 4. Módulo de Pedidos y Caja (`PEDIDOS` y `DETALLE_PEDIDOS`)

Este es el **núcleo operativo del restaurante** y debe cumplir las siguientes directrices:

### A. Condiciones previas para armar el pedido
* **RN-PED-01 (Asignación de Mesa/Ubicación):** Es obligatorio seleccionar o escribir el `numero_mesa` (ej. "Mesa 01", "Mesa 05", "Barra", "Para Llevar"). No se puede procesar una venta sin mesa.
* **RN-PED-02 (Asignación de Cliente):** Es obligatorio seleccionar un cliente del directorio (puede ser un cliente frecuente o el cliente genérico "Público General").
* **RN-PED-03 (Método de Pago):** Es obligatorio seleccionar la modalidad de cobro antes de confirmar:
  - *Efectivo*
  - *Yape / Plin*
  - *Tarjeta (Débito / Crédito)*

### B. Gestión del Carrito Temporal (Memoria RAM)
* **RN-PED-04 (Cantidad mínima):** La cantidad de platos a agregar debe ser un número entero mayor o igual a 1 (`cantidad >= 1`). No se permiten cantidades en cero, negativas o decimales.
* **RN-PED-05 (Cálculo del Subtotal por plato):**
  $$\text{Subtotal} = \text{Cantidad} \times \text{Precio Unitario}$$
  El cálculo debe ejecutarse utilizando el módulo `Decimal` a 2 posiciones decimales.
* **RN-PED-06 (Observaciones de Cocina `nota_plato`):** El campo es opcional y permite registrar instrucciones personalizadas para la cocina (ej. "sin cebolla", "término 3/4", "ají aparte", "sin hielo").
* **RN-PED-07 (Cálculo del Total Acumulado en RAM):**
  $$\text{Total} = \sum \text{Subtotales del Carrito}$$
  El total debe recalcularse en tiempo real en la memoria RAM cada vez que:
  - Se añade un nuevo plato al pedido.
  - Se modifica la cantidad de un plato existente.
  - Se elimina un plato de la lista temporal.
* **RN-PED-08 (Validación de Carrito Vacío):** El botón "Registrar Pedido / Cobrar" debe estar bloqueado o rechazar la acción si el carrito no tiene al menos un ítem agregado.

### C. Persistencia Atómica en MySQL
* **RN-PED-09 (Transacción Atómica - Todo o Nada):** Al confirmar el pedido:
  1. Se registra la cabecera en `PEDIDOS` con fecha y hora actual del sistema (`datetime.now()`), asignando el cliente, mesa, cajero logueado (`id_usuario`), método de pago, total y estado `Pagado`.
  2. Se obtiene el `id_pedido` generado.
  3. Se inserta cada renglón del pedido en `DETALLE_PEDIDOS` vinculado a dicho `id_pedido`.
  4. Si ocurre cualquier error durante este proceso, se ejecuta `rollback()`, evitando que queden cobros sin detalle o platos sueltos en la base de datos.
* **RN-PED-10 (Limpieza y Restablecimiento):** Una vez confirmado el guardado exitoso en base de datos:
  - Se vacía la lista temporal del carrito en la memoria RAM.
  - Se reinician los campos de mesa, notas y cliente en pantalla.
  - El total visual vuelve a `S/ 0.00`.
  - Se despliega un cuadro emergente de éxito: *"¡Pedido registrado y cobrado con éxito!"*.

---

## 5. Resumen de Responsabilidades ante las Reglas

| Integrante | Lo que debe asegurar con respecto a estas reglas |
| :--- | :--- |
| **Bolivar (Vista)** | Que los campos visuales faciliten el cumplimiento de las reglas (ej. dropdowns con las categorías fijas, interruptores para disponibilidad y cuadros `messagebox` informativos). |
| **Israel (Controlador)** | Que el código valide cada regla con `re` y `Decimal` antes de llamar a la base de datos, manteniendo los cálculos en RAM exactos. |
| **Jybran (Modelo / BD)** | Que la base de datos tenga restricciones acordes (`UNIQUE` en DNI, tipos `DECIMAL(10,2)`, llaves foráneas y transacciones con `commit`/`rollback`). |
| **Alex (Líder / QA)** | Que la aplicación respete cada una de estas reglas al probar el flujo de inicio a fin. |
