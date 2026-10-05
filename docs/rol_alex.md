# Rol y Responsabilidades: Alex (Líder de Proyecto / QA y Documentación)

---

## 1. Misión del Rol
Asegurar la calidad, estabilidad técnica, coherencia arquitectónica y formalización documental integral de "El Rincón Criollo". Alex es el líder del proyecto y responsable de certificar que el sistema cumpla al 100% con los requerimientos operativos de un restaurante comercial, auditando que la interfaz de Bolivar sea intuitiva y ergonómica, que la lógica financiera y transaccional de Israel en memoria RAM sea exacta, que la persistencia en MySQL gestionada por Jybran preserve la integridad referencial de los datos, y redactando el manual técnico oficial que guiará el despliegue del software.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas Asignadas:
- `docs/reglas_negocio.md` (Custodia, redacción y verificación del cumplimiento de todas las reglas operativas).
- `docs/manual_tecnico.md` (Manual oficial de arquitectura MVC, diagrama E-R, diccionario de datos, guía de despliegue y manual de usuario).
- `docs/informe_auditoria_integracion.md` (Bitácora de auditoría técnica y aseguramiento de la integridad del repositorio).
- `docs/El_proyecto.md` (Especificación de objetivos y alcance general del sistema).
- `docs/rol_*.md` (Documentación formal de funciones y responsabilidades del equipo).

### Herramientas y Aspectos Técnicos a Auditar:
- **Auditoría de Componentes Visuales:** Verificar la adecuada jerarquía visual con `customtkinter`, la presencia de formularios modales desacoplados (`CTkToplevel`) para evitar el amontonamiento de datos, la legibilidad de botones (`height=44`) y el correcto desplazamiento en tablas `ttk.Treeview`.
- **Auditoría de Precisión Financiera en RAM:** Probar que las operaciones de multiplicación (cantidad $\times$ precio) y suma acumulada del total utilicen con rigor el módulo `Decimal`, garantizando discrepancia cero ($S/. 0.00$ de error) por redondeo de coma flotante.
- **Auditoría de Integridad Contable y Validaciones:** Introducir datos no válidos a propósito (DNIs con letras o longitudes distintas a 8 dígitos, precios negativos) para verificar que sean bloqueados antes de tocar MySQL, y validar que ningún plato con ventas registradas pueda ser eliminado físicamente.
- **Auditoría de Transaccionalidad en Base de Datos:** Comprobar en `phpMyAdmin` que los pedidos y sus detalles se inserten en bloque atómico (`commit`), y que ante un fallo no queden registros huérfanos (`rollback`).
- **Auditoría de Gestión de Salón:** Verificar que las mesas con comandas pendientes queden bloqueadas como ocupadas y que se liberen de forma inmediata al confirmarse el cobro.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Auditoría Integral de Reglas de Negocio (`reglas_negocio.md`):**
   - Verificar de forma exhaustiva cada directriz operativa del restaurante:
     - **Módulo de Acceso (RN-ACC-01 a 04):** Validación de credenciales, bloqueo ante clave errónea y retención en sesión del `id_usuario`, nombre y rol para trazabilidad.
     - **Módulo de Clientes (RN-CLI-01 a 05):** Validación estricta de DNI de 8 dígitos numéricos, nombres obligatorios y disponibilidad del cliente genérico para ventas al paso.
     - **Módulo de Carta y Productos (RN-PRO-01 a 06):** Categorías oficiales, visualización en caja de solo platos disponibles, edición dinámica de la carta, conmutación de stock (`Disponible` / `Agotado`) y bloqueo de borrado de platos con ventas históricas.
     - **Módulo de Caja, Mesas y Comandas (RN-PED-01 a 12):**
       - Asignación obligatoria de mesa y validación de mesas ocupadas (`Mesa 01 a 06`).
       - Cálculos exactos en memoria RAM con `Decimal` para subtotales y total general.
       - Soporte para flujo dual: `Guardar Comanda (Pendiente)` para atención en salón y `Cobrar al Instante (Pagado)` para despacho rápido.
       - Cierre y cobro de comandas pendientes desde el Historial de Ventas, garantizando la liberación automática de la mesa asignada.

2. **Redacción y Mantenimiento del Manual Técnico Oficial (`manual_tecnico.md`):**
   - Documentar la arquitectura MVC detallando la separación de capas (Modelo $\leftrightarrow$ Controlador $\leftrightarrow$ Vista).
   - Elaborar y mantener el diagrama Entidad-Relación (E-R) en formato Mermaid con las 5 tablas relacionales y sus llaves foráneas.
   - Publicar el diccionario de datos exhaustivo de las tablas `usuarios`, `clientes`, `productos`, `pedidos` y `detalle_pedidos` (tipos de datos, restricciones de nulidad y descripciones).
   - Detallar la guía paso a paso de instalación y despliegue en Windows con XAMPP: clonación, entorno virtual `.venv`, instalación de `requirements.txt`, configuración de `.env`, importación de `schema.sql` y comando de arranque `python main.py`.
   - Redactar la Guía de Usuario ilustrada que enseñe a operar cada módulo del software al personal del restaurante.

3. **Gestión de Calidad, Pruebas y Reporte de Incidencias:**
   - Realizar pruebas de extremo a extremo (End-to-End) simulando el día a día de un cajero y un mozo en el restaurante.
   - Registrar y asignar incidencias a los responsables específicos:
     - Fallos visuales, estilos o modales $\rightarrow$ **Bolivar (Vistas)**.
     - Fallos en validaciones `re`, cálculos `Decimal` o flujo de mesas $\rightarrow$ **Israel (Controlador)**.
     - Errores de sintaxis SQL, llaves foráneas o conexión a XAMPP $\rightarrow$ **Jybran (Modelo/BD)**.

---

## 4. Lo que NO DEBE hacer (Límites Arquitectónicos)

- **NO alterar el código de los módulos para corregir fallos:** Su rol es detectar anomalías, levantar el informe técnico y certificar la corrección implementada por sus compañeros.
- **NO modificar el esquema relacional de forma unilateral:** Cualquier ajuste sobre las tablas debe ser coordinado y aprobado en conjunto con Jybran.
- **NO interferir en las decisiones de diseño estético o algorítmico interno** de sus compañeros, siempre y cuando cumplan con las reglas de negocio y los contratos de integración.

---

## 5. Criterio de Certificación Final

Alex emitirá el dictamen de aprobación formal del sistema cuando se cumplan las siguientes condiciones:
1. El ciclo comercial completo (toma de comanda $\rightarrow$ mesa ocupada $\rightarrow$ cobro desde historial $\rightarrow$ mesa liberada) opere sin inconsistencias.
2. No existan errores de redondeo de punto flotante en ninguna operación contable.
3. El manual técnico y las reglas de negocio se encuentren totalmente documentados y sincronizados con el software real.

---

## 6. Lista de Documentos, Auditorías y Criterios de Éxito al Culminar su Parte

Para considerar su módulo 100% culminado y operativo, Alex debe entregar elaborados, auditados y validados los siguientes entregables:

### 1. Manual Técnico Oficial (`docs/manual_tecnico.md`):
* [x] Diagrama arquitectónico MVC y explicación del flujo de eventos.
* [x] Diagrama Entidad-Relación (E-R) formal en código Mermaid con cardinalidades.
* [x] Diccionario de datos de las 5 tablas relacionales con campos, tipos y claves.
* [x] Guía de despliegue paso a paso para Windows y XAMPP (`pip`, `.venv`, MySQL, `main.py`).
* [x] Manual de Usuario detallado que guíe el inicio de sesión, registro de clientes, gestión de carta, toma de comandas y cobro en historial.

### 2. Especificación de Reglas de Negocio (`docs/reglas_negocio.md`):
* [x] Reglas de Acceso y Trazabilidad de Sesión (`RN-ACC-01` a `RN-ACC-04`).
* [x] Reglas de Clientes y Unicidad de DNI (`RN-CLI-01` a `RN-CLI-05`).
* [x] Reglas de Productos, Disponibilidad, Edición y Protección Contable (`RN-PRO-01` a `RN-PRO-06`).
* [x] Reglas de Pedidos, Carrito en RAM con Decimal, Mesas Ocupadas y Flujo Dual (`RN-PED-01` a `RN-PED-12`).
* [x] Matriz de responsabilidades por integrante del equipo.

### 3. Matriz de Auditoría y Control de Calidad (QA):
* [x] Certificación de que ningún plato con comandas previas pueda eliminarse físicamente de la base de datos.
* [x] Certificación de que no se puedan abrir comandas simultáneas en una mesa ocupada.
* [x] Certificación de que la comanda cobrada libere la mesa inmediatamente en la interfaz.
* [x] Certificación de exactitud monetaria en `Decimal` para compras múltiples y subtotales.
