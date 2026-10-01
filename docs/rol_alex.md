# Rol y Responsabilidades: Alex (Líder de Proyecto / QA y Documentación)

---

## 1. Misión del Rol
Asegurar la calidad, estabilidad técnica y formalización documental de "El Rincón Criollo". Alex es el responsable de certificar que el Producto Mínimo Viable (MVP) alcance el **70% de operatividad funcional**, auditando tanto el comportamiento de la interfaz como el rigor matemático de los cálculos en memoria RAM, la resiliencia de la conexión a MySQL en XAMPP y redactando el manual técnico que guiará el despliegue del sistema.

---

## 2. Territorio Asignado y Herramientas Tecnológicas

### Archivos y Carpetas:
- `docs/reglas_negocio.md` (Custodia y verificación del cumplimiento de las reglas operativas).
- `docs/manual_tecnico.md` (Manual de arquitectura MVC, modelo E-R, stack tecnológico y despliegue).
- `docs/` (Reportes de control de calidad, bitácoras de incidencias y actas de aceptación).

### Herramientas y Aspectos Técnicos a Auditar:
- **Auditoría de Componentes Visuales:** Verificar la correcta representación de ventanas con `customtkinter`, el funcionamiento fluido de las tablas `ttk.Treeview` con sus barras de desplazamiento y la adecuada aparición de diálogos modales nativos (`tkinter.messagebox`).
- **Auditoría de Precisión Financiera:** Probar que los cálculos de precios, subtotales y totales utilicen la precisión exacta del módulo `Decimal`, garantizando que no existan desajustes de céntimos por punto flotante.
- **Auditoría de Expresiones Regulares (`re`):** Introducir datos erróneos a propósito (letras en el DNI, DNIs de 7 o 9 dígitos) para verificar que las reglas de negocio intercepten los errores antes de tocar la base de datos.
- **Auditoría de Resiliencia de Base de Datos:** Comprobar el comportamiento del sistema ante caídas del servicio MySQL en XAMPP, validando que el conector `mysql-connector-python` atrape las excepciones mediante `mysql.connector.errors` y notifique amigablemente al usuario sin provocar cierres inesperados.
- **Entorno de Verificación:** Uso de `phpMyAdmin` o `MySQL Workbench` para comprobar de primera mano que las ventas registradas se reflejen fielmente en las tablas `PEDIDOS` y `DETALLE_PEDIDOS`.

---

## 3. Lo que DEBE hacer (Responsabilidades Principales)

1. **Auditoría de Cumplimiento de las Reglas de Negocio (`reglas_negocio.md`):**
   - Verificar de forma metódica que cada regla de negocio se cumpla en el sistema para certificar el 70% del MVP:
     - **Módulo de Acceso:** Validación de login exitoso, rechazo ante contraseña equivocada y verificación de que se asigne el `id_usuario` a la sesión.
     - **Módulo de Clientes:** Prueba de expresiones regulares (bloqueo ante DNI con menos o más de 8 dígitos, o con letras) y confirmación visual en el `Treeview`.
     - **Módulo de Productos:** Rechazo de precios negativos o cero, conmutación del estado de disponibilidad (`disponible`) y refresco de la carta.
     - **Módulo de Caja y Ventas (Núcleo en RAM y Transacción):**
       - Prueba de suma decimal acumulada en el carrito: verificar que la multiplicación de cantidad por precio unitario no arroje errores de aproximación.
       - Validación de que no se permita cobrar si el carrito está vacío, si falta el número de mesa o el método de pago.
       - Auditoría de persistencia: comprobar en `phpMyAdmin` que al confirmar la venta se genere el registro en `PEDIDOS` (con fecha y hora exacta de `datetime.now()`) y los renglones correspondientes en `DETALLE_PEDIDOS` (conservando las instrucciones de `nota_plato`).
   - Calificar cada escenario como Aprobado, Rechazado o Bloqueado.

2. **Redacción del Manual Técnico del Sistema (`manual_tecnico.md`):**
   - Documentar la arquitectura Modelo-Vista-Controlador (MVC) y la separación de responsabilidades.
   - Diagramar y explicar el Modelo Entidad-Relación (E-R) de las 5 tablas y sus relaciones de cardinalidad.
   - Describir la pila tecnológica completa:
     - Interfaz: `customtkinter`, `ttk.Treeview`, `tkinter.messagebox`, `Pillow`.
     - Lógica: `Decimal`, `re`, `datetime`, estructuras en RAM.
     - Persistencia: `mysql-connector-python`, MySQL vía XAMPP, `schema.sql`.
   - Incluir la guía de instalación y puesta en marcha:
     - Instalación de dependencias mediante `pip install -r requirements.txt`.
     - Inicio de servicios en el panel de control de XAMPP (Apache y MySQL).
     - Importación del archivo `schema.sql` en phpMyAdmin.
     - Ejecución del sistema mediante `python main.py`.
   - Incorporar la guía de uso operativo para el personal del restaurante.

3. **Gestión y Reporte de Incidencias (Bugs):**
   - Levantar reportes técnicos detallados especificando los pasos para reproducir la falla, la librería involucrada y asignando la tarea al miembro competente:
     - Problemas en `Treeview`, formularios o estilos -> **Bolivar**
     - Fallos en cálculos de `Decimal`, expresiones regulares de `re` o carrito en RAM -> **Israel**
     - Errores de sintaxis SQL, llaves foráneas o transacciones fallidas -> **Jybran**

---

## 4. Lo que NO DEBE hacer (Límites para no chocar con el equipo)

- **NO modificar el código fuente para subsanar errores:** Su responsabilidad es auditar, reportar y validar la corrección, nunca editar los archivos de sus compañeros.
- **NO alterar el esquema de la base de datos de forma unilateral:** Cualquier ajuste sobre las tablas o tipos de datos debe ser coordinado con Jybran.
- **NO alterar las dependencias en `requirements.txt` sin previo consenso.**

---

## 5. Criterio de Certificación Final
Alex emitirá la aprobación definitiva cuando la matriz de pruebas confirme que el ciclo comercial se ejecuta con fluidez, sin errores de punto flotante en caja, con datos protegidos contra inyecciones e inconsistencias, y con el manual técnico concluido para la entrega final.
