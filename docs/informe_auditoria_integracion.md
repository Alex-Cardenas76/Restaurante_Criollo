# Informe de Aseguramiento de Calidad y Certificación Funcional (QA)

**Proyecto:** El Rincón Criollo - Sistema de Gestión de Salón y Ventas (MVP)  
**Líder / Auditor de Calidad (QA):** Alex Cárdenas  
**Fecha de Certificación:** Octubre de 2026  
**Entorno de Pruebas:** Python 3.10+, CustomTkinter, MySQL 8.0 (XAMPP), Windows 11  

---

## 1. Resumen Ejecutivo
El presente informe formaliza los resultados de la auditoría técnica y funcional de extremo a extremo (End-to-End) realizada sobre el **Producto Mínimo Viable (MVP)** del sistema de restaurante **"El Rincón Criollo"**. 

La evaluación certifica que la arquitectura **Modelo - Vista - Controlador (MVC)** se encuentra implementada con total separación de responsabilidades entre los módulos de **Jybran** (Base de Datos / Modelos), **Bolivar** (Vistas / Interfaz Gráfica) e **Israel** (Controladores / Lógica y RAM), cumpliendo cabalmente con todos los requerimientos funcionales establecidos para el MVP.

---

## 2. Matriz de Auditoría y Verificación por Módulos

### A. Módulo de Acceso, Seguridad y Sesión
* **Alcance auditado:** Validación de credenciales, control de errores y trazabilidad de sesión activa.
* **Pruebas ejecutadas:**
  - Intento de ingreso con campos vacíos $\rightarrow$ **Bloqueado** con alerta nativa clara.
  - Ingreso con contraseña errónea $\rightarrow$ **Rechazado** limpiando la clave y conservando el usuario.
  - Ingreso exitoso con perfiles `admin` (rol Administrador) y `cajero1` (rol Vendedor) $\rightarrow$ **Aprobado**.
* **Resultado:** La sesión activa retiene en memoria `{id_usuario, usuario, rol}` y el encabezado del Dashboard refleja la identidad del usuario en tiempo real. Cada pedido registrado asocia el `usuario_id` del cajero responsable.

### B. Módulo de Clientes (Directorio y Ventas Rápidas)
* **Alcance auditado:** Validación de formatos mediante expresiones regulares (`re`), prevención de duplicidad y soporte de cliente genérico.
* **Pruebas ejecutadas:**
  - Ingreso de DNI con letras, espacios o longitud distinta a 8 dígitos $\rightarrow$ **Bloqueado** por regex (`^\d{8}$`).
  - Intento de registrar un DNI ya existente en MySQL $\rightarrow$ **Rechazado** capturando el error de clave única.
  - Apertura del modal `ModalFormularioCliente` $\rightarrow$ Ventana emergente centrada con botones ergonómicos (`height=44`). Al guardar, se refresca la tabla automáticamente y el modal se cierra de forma limpia.
  - Cliente genérico `Público General` (DNI: `00000000`) $\rightarrow$ Disponible por defecto para despachos rápidos.
* **Resultado:** Cumplimiento total de las reglas `RN-CLI-01` a `RN-CLI-05`.

### C. Módulo de Carta Gastronómica y Productos Criollos (CRUD Completo)
* **Alcance auditado:** Ciclo de vida completo de platos criollos, precisión de precios con `Decimal` y protección de integridad contable.
* **Pruebas ejecutadas:**
  - **Creación (`+ Nuevo Plato`):** Validación de precio strictly $> 0.00$ y asignación de categoría fija.
  - **Edición (`✏️ Editar Plato`):** Selección de plato en el `Treeview` y apertura del modal con datos precargados. Modificación exitosa de nombre y precio en MySQL.
  - **Conmutación de Stock (`🔄 Disponibilidad`):** Alternancia en caliente entre `Disponible` y `Agotado`. Los platos agotados quedan automáticamente excluidos del selector de toma de pedidos en caja.
  - **Eliminación con Protección Contable (`🗑️ Eliminar`):**
    - Plato sin ventas previas $\rightarrow$ Confirmación mediante `askyesno` y borrado físico definitivo.
    - Plato con comandas o pedidos registrados en el historial $\rightarrow$ **Bloqueo preventivo** informando al usuario que no se puede eliminar para no romper los reportes contables, recomendando marcarlo como `Agotado`.
* **Resultado:** Cumplimiento total de las reglas `RN-PRO-01` a `RN-PRO-06`.

### D. Módulo de Terminal de Pedidos, Salón y Mesas
* **Alcance auditado:** Carrito en RAM con precisión matemática, control de rotación de mesas y flujo dual comanda/pago.
* **Pruebas ejecutadas:**
  - **Cálculos en RAM con `Decimal`:** Adición de múltiples unidades de platos con subtotales y notas especiales de cocina. Discrepancia aritmética: **S/. 0.00** (cero pérdida de céntimos).
  - **Validación de Mesas Ocupadas vs Libres:**
    - Registro de comanda mediante `📝 Guardar Comanda (Pendiente)`.
    - La mesa asignada cambia su estado a `(Ocupada - Pedido #ID)`.
    - Intento de abrir un nuevo pedido en dicha mesa $\rightarrow$ **Bloqueado** con alerta informativa de comanda activa.
    - Las órdenes para despacho rápido (`Para Llevar`) no generan bloqueo de salón.
  - **Cobro Inmediato (`💳 Cobrar al Instante`):** Registro de venta liquidada en el acto, dejando la mesa libre.
  - **Transaccionalidad en MySQL:** Verificación en base de datos de que cabecera (`pedidos`) y detalle (`detalle_pedidos`) se guarden bajo bloque atómico (`commit`/`rollback`).
* **Resultado:** Cumplimiento total de las reglas `RN-PED-01` a `RN-PED-10`.

### E. Módulo Historial de Ventas ("Ver Pedidos") y Cierre de Cuentas
* **Alcance auditado:** Auditoría general de ventas y liquidación de comandas pendientes.
* **Pruebas ejecutadas:**
  - Visualización completa de todos los comprobantes emitidos con fecha, mesa, cliente, total y estado (`Pagado` / `Pendiente`).
  - Botón `🔍 Ver Detalle de Comanda`: Despliegue del modal `ModalDetalleComanda` con los platos consumidos y notas de cocina de la orden.
  - Botón `💳 Cobrar Pedido Pendiente`: Despliegue del modal `ModalCobrarPedido`, selección de forma de pago (*Efectivo, Yape, Tarjeta*) y confirmación de cobro.
  - **Liberación de Mesa en Tiempo Real:** Al cobrarse la comanda, el pedido pasa a `Pagado` y la mesa asociada queda **inmediatamente disponible** para recibir nuevos comensales.
* **Resultado:** Cumplimiento total de las reglas `RN-PED-11` y `RN-PED-12`.

---

## 3. Estado de Certificación del Sistema

| Criterio de Calidad | Estado | Observación Técnica |
| :--- | :---: | :--- |
| **Separación de Responsabilidades MVC** | ✅ CONFORME | Vistas sin SQL, Modelos sin GUI, Controladores orquestando lógica y RAM. |
| **Integridad de Base de Datos** | ✅ CONFORME | Sentencias preparadas (`%s`), transacciones atómicas y protección referencial. |
| **Precisión Financiera** | ✅ CONFORME | Uso riguroso de `decimal.Decimal` en todas las operaciones monetarias. |
| **Usabilidad y Ergonomía** | ✅ CONFORME | Modales flotantes desacoplados, botones grandes (`height=44`) y textos nítidos. |
| **Flujo Comercial Completo** | ✅ CONFORME | Ciclo cerrado de salón: Comanda $\rightarrow$ Cocina $\rightarrow$ Mesa Ocupada $\rightarrow$ Cobro $\rightarrow$ Mesa Libre. |
| **Compilación y Ejecución** | ✅ CONFORME | 0 errores de sintaxis en `py_compile`, arranque limpio con `python main.py`. |

---

## 4. Dictamen Final de QA
Se certifica la **Aprobación Formal del Producto Mínimo Viable (MVP)** del sistema "El Rincón Criollo". La solución se encuentra estable, documentada y lista para su sustentación y pruebas de validación con usuarios.
