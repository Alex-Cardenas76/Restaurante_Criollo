# Informe de Auditoría Técnica e Integración MVC

**Proyecto:** El Rincón Criollo - Sistema de Gestión de Ventas (MVP)  
**Líder / QA:** Alex Cárdenas  
**Fecha:** 04 de Octubre de 2026  
**Rama de Integración:** `main`

---

## 1. Resumen Ejecutivo
El presente informe documenta la auditoría técnica realizada sobre los aportes entregados por cada integrante del equipo (**Jybran**, **Bolivar** e **Israel**), los hallazgos identificados en sus respectivas capas (Modelo, Vista y Controlador), la resolución del conflicto de historiales en Git (`unrelated histories`) y el proceso de cableado y ensamble final en [main.py](file:///C:/Users/ACER/Desktop/Criollo/main.py) para alcanzar el **Producto Mínimo Viable (MVP) funcional al 70%**.

---

## 2. Auditoría Detallada por Integrante

### A. Jybran (Capa de Persistencia / Modelos y Base de Datos)
* **Carpetas asignadas:** `database/` y `models/`
* **Commits auditados:** `f328c40` e `130dec2`
* **Cumplimiento de límites:** **100%**. No modificó archivos de vistas ni controladores.

#### Hallazgos y Correcciones Aplicadas:
1. **Seguridad SQL:** Uso estricto de sentencias preparadas con parámetros seguros (`%s`), previniendo inyecciones SQL en todas las operaciones.
2. **Atomicidad en Pedidos:** Implementación de bloques transaccionales con `commit()` y `rollback()` para garantizar que la cabecera del pedido y los renglones de detalle se guarden juntos o ninguno en caso de fallo.
3. **Ajustes al Esquema Relacional ([schema.sql](file:///C:/Users/ACER/Desktop/Criollo/database/schema.sql)):**
   - Se añadió la columna `categoria VARCHAR(50)` en `PRODUCTOS` para permitir el filtrado de la carta (*Entradas, Platos de Fondo, Guarniciones, Bebidas, Postres*).
   - Se añadieron `precio_unitario DECIMAL(10,2)` y `nota_plato VARCHAR(150)` en `DETALLE_PEDIDOS` para registrar observaciones de cocina y auditoría de precios.
   - Se modificó la columna `mesa` de `INT` a `VARCHAR(20)` en `PEDIDOS` para soportar identificadores reales como *"Mesa 01"* o *"Barra"*.
   - Se añadió la restricción `UNIQUE` en el `dni` de `CLIENTES` para evitar clientes duplicados.
   - Se incorporaron semillas de datos iniciales (*usuario administrador `admin`/`admin123`*, *cliente genérico `Público General`* y *11 platos criollos*).
4. **Resiliencia de Conexión:** Creación del manejador de contexto `conexion_segura()` en [conexion.py](file:///C:/Users/ACER/Desktop/Criollo/database/conexion.py), protegiendo contra caídas de XAMPP mediante `int(os.getenv("DB_PORT", 3306))`.

---

### B. Bolivar (Capa de Presentación / Vistas CustomTkinter)
* **Carpeta asignada:** `views/`
* **Commit auditado:** `07f37d7` (`feat/bolivar-views`)
* **Cumplimiento de límites en código:** **100%**. El único código nuevo programado pertenece a la interfaz gráfica.

#### Hallazgos y Resolución del Incidente en Git:
1. **Incidente técnico:** Al intentar fusionar la rama (`git merge feat/bolivar-views`), Git arrojó el error crítico:
   ```text
   fatal: refusing to merge unrelated histories
   ```
2. **Causa raíz:** Bolivar no creó su rama partiendo del historial del repositorio clonado, sino que inicializó un repositorio independiente (`git init`) sobre una copia estática del proyecto, generando un commit raíz sin ancestro común con `main`.
3. **Resolución aplicada:** Se ejecutó una fusión estratégica:
   ```bash
   git merge feat/bolivar-views --allow-unrelated-histories -X ours
   ```
   Esto permitió unir los dos historiales y, mediante la estrategia `-X ours`, se preservaron intactos los modelos y controladores de `main`, extrayendo de forma limpia y exclusiva los archivos de la carpeta `views/`.
4. **Mejoras aplicadas a las vistas:**
   - En [login_view.py](file:///C:/Users/ACER/Desktop/Criollo/views/login_view.py): Se corrigió `get_usuario()` para que no forzara sufijos `@gmail.com`, permitiendo el acceso del usuario `admin`.
   - En [dashboard_view.py](file:///C:/Users/ACER/Desktop/Criollo/views/dashboard_view.py): Se incorporó el botón **"Cerrar Sesión"** en el menú lateral.
   - En [pedidos_view.py](file:///C:/Users/ACER/Desktop/Criollo/views/pedidos_view.py): Se implementó el panel de selección de platos, notas de cocina, método de pago y botones para agregar/quitar ítems del carrito en memoria RAM.

---

### C. Israel (Capa de Lógica / Controladores y Reglas de Negocio)
* **Carpetas asignadas:** `controllers/` y `main.py`
* **Commit auditado:** `8e646ae` (`feat/israel-controladores`)
* **Cumplimiento de límites:** **100%**. Solo programó en su área asignada.

#### Hallazgos y Ensamble Realizado:
1. **Reglas de Negocio:** Validación de DNI de 8 dígitos y teléfonos con expresiones regulares (`re`).
2. **Precisión Financiera:** Uso obligatorio de `Decimal` en todos los cálculos de dinero, previniendo errores de redondeo de punto flotante en la caja.
3. **Estado del Carrito en RAM:** Gestión dinámica de listas de diccionarios en memoria RAM para actualizar subtotales y total general en tiempo real.
4. **Alineación de interfaces:** Se sincronizaron las firmas de los métodos entre los controladores y las funciones de los modelos de Jybran (por ejemplo: paso de parámetros limpios en lugar de diccionarios planos incompatibles).

---

## 3. Ensamble de la Aplicación ([main.py](file:///C:/Users/ACER/Desktop/Criollo/main.py))

Se sustituyó el mensaje temporal de prueba por el ciclo de vida completo de la aplicación:
1. **Arranque:** Inicializa la ventana principal centrada (1020x680) y renderiza [LoginView](file:///C:/Users/ACER/Desktop/Criollo/views/login_view.py).
2. **Autenticación:** Valida credenciales contra MySQL mediante [LoginController](file:///C:/Users/ACER/Desktop/Criollo/controllers/login_controller.py).
3. **Transición:** Al autenticarse, destruye la pantalla de login y monta [DashboardView](file:///C:/Users/ACER/Desktop/Criollo/views/dashboard_view.py).
4. **Navegación Dinámica:** Alterna entre [ClientesView](file:///C:/Users/ACER/Desktop/Criollo/views/clientes_view.py), [ProductosView](file:///C:/Users/ACER/Desktop/Criollo/views/productos_view.py) y [PedidosView](file:///C:/Users/ACER/Desktop/Criollo/views/pedidos_view.py), refrescando los datos desde la base de datos en cada navegación.
5. **Cierre de Sesión:** Permite regresar al Login restableciendo la memoria del sistema.

---

## 4. Estado de Certificación del MVP (70% Funcional)

| Módulo Evaluado | Estado | Evidencia / Comprobación |
| :--- | :---: | :--- |
| **Acceso y Seguridad** | ✅ APROBADO | Login operativo con usuario `admin`/`admin123`. Bloqueo ante campos vacíos o clave errónea. |
| **Directorio de Clientes** | ✅ APROBADO | Validación de DNI numérico (8 dígitos), registro en MySQL y visualización en tabla `Treeview`. |
| **Catálogo de Carta Criolla** | ✅ APROBADO | Registro con categorías fijas, validación de precio positivo con `Decimal` y visualización de disponibilidad. |
| **Gestión de Pedidos / Caja** | ✅ APROBADO | Selección de cliente, mesa y método de pago; cálculo en RAM en tiempo real de subtotales/totales; guardado atómico en cabecera y detalle. |
| **Arquitectura y Código** | ✅ APROBADO | 0 errores de sintaxis, compilación limpia en Python y repositorio sincronizado. |

**Conclusión:** El sistema cumple cabalmente con todos los criterios de diseño, separación de responsabilidades MVC y requerimientos del MVP al 70%.
