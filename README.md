# El Rincón Criollo - Sistema de Gestión de Salón y Ventas (MVP)

Aplicación de escritorio desarrollada en **Python** y **MySQL** como **Producto Mínimo Viable (MVP)** para la administración operativa, atención de comensales en salón y control de caja en el restaurante tradicional "El Rincón Criollo". Diseñada para operar de forma local (offline) sin depender de servicios web ni conectividad a internet.

---

## 📌 Alcance Funcional del MVP

Este proyecto se enfoca en resolver el flujo operativo crítico de un restaurante mediante un Producto Mínimo Viable (MVP) robusto, cubriendo cinco componentes clave:

1. **Control de Acceso y Seguridad (Login):** Autenticación de personal con perfiles diferenciados (`administrador` y `vendedor`), con retención de sesión activa y trazabilidad del cajero en cada comprobante.
2. **Directorio y Gestión de Clientes:** Tabla de comensales frecuentes, formulario modal independiente con validación estricta de DNI de 8 dígitos y cliente genérico (`Público General`) para ventas rápidas.
3. **Carta de Platos Criollos (CRUD Completo):** Catálogo con categorización fija, precios exactos en `Decimal`, conmutación de stock en caliente (`Disponible` / `Agotado`), formulario modal para crear y editar platos, y **protección de integridad contable** que impide eliminar platos con historial de ventas.
4. **Terminal de Salón, Comandas y Caja:** Asignación y control de mesas con estado dinámico en vivo (`Mesa 01 a 06 (Disponible)` vs `(Ocupada - Pedido #X)`), carrito de compras en memoria RAM con notas especiales para cocina y **botonera de doble acción**:
   - `📝 Guardar Comanda (Pendiente)`: Envía la orden a cocina y marca la mesa como ocupada para comensales en salón.
   - `💳 Cobrar al Instante (Pagado)`: Liquida y emite el comprobante de inmediato para despachos rápidos o para llevar.
5. **Historial de Ventas ("Ver Pedidos"):** Módulo dedicado para auditar los comprobantes emitidos, consultar los platos consumidos (`ModalDetalleComanda`) y liquidar comandas pendientes (`ModalCobrarPedido`), liberando automáticamente la mesa asignada en tiempo real.

---

## 👥 Equipo y Distribución de Responsabilidades (MVC + QA)

El proyecto sigue una estricta separación de responsabilidades bajo el patrón **Modelo - Vista - Controlador (MVC)**:

| Integrante | Rol | Capa / Responsabilidad | Documento de Rol | Carpeta Asignada |
| :--- | :--- | :--- | :--- | :--- |
| **Jybran** | Modelo / Base de Datos | Scripts DDL, conexión segura y consultas SQL parametrizadas (`%s`). | [rol_jybran.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_jybran.md) | `database/`, `models/` |
| **Bolivar** | Vista / Interfaz Gráfica | CustomTkinter, modales `CTkToplevel`, `Treeviews`, botones ergonómicos. | [rol_bolivar.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_bolivar.md) | `views/` |
| **Israel** | Controlador / Lógica | Reglas de negocio, validaciones `re`, cálculos exactos en RAM (`Decimal`). | [rol_israel.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_israel.md) | `controllers/`, `main.py` |
| **Alex** | Líder / QA y Documentación | Auditoría de reglas, manual técnico oficial, pruebas de calidad y despliegue. | [rol_alex.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_alex.md) | `docs/` |

---

## 🚀 Guía de Instalación y Puesta en Marcha

Sigue estos pasos en tu computadora para configurar el entorno de trabajo:

### 1. Clonar el repositorio
Abre una terminal (PowerShell o Git Bash) y clona el proyecto:
```bash
git clone https://github.com/Alex-Cardenas76/Restaurante_Criollo.git
cd Restaurante_Criollo
```

### 2. Crear y activar el entorno virtual (`.venv`)
Crea un entorno aislado para que las dependencias se instalen exclusivamente en este proyecto:

* **En Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```
*(Al activarse verás el prefijo `(.venv)` al inicio de la línea de comandos).*

### 3. Instalar las dependencias oficiales
Con el entorno virtual activado, instala todas las librerías necesarias con un solo comando:
```powershell
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno (`.env`)
Para mantener aisladas y seguras las credenciales de base de datos de cada desarrollador:
1. Copia el archivo `.env.example` y renómbralo como `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Abre el archivo `.env` y verifica tus credenciales de XAMPP (`DB_HOST=localhost`, `DB_PORT=3306`, `DB_USER=root`, `DB_PASSWORD=`, `DB_NAME=el_rincon_criollo`).

> **Nota:** El archivo `.env` está registrado en `.gitignore`, por lo que **nunca se subirá a GitHub**, protegiendo tu configuración local.

### 5. Configurar la Base de Datos en MySQL (XAMPP)
1. Inicia **Apache** y **MySQL** desde el panel de control de **XAMPP**.
2. Ingresa a **phpMyAdmin** en tu navegador (`http://localhost/phpmyadmin`).
3. Crea la base de datos `el_rincon_criollo`.
4. Ve a la pestaña **Importar** y selecciona el archivo `database/schema.sql` (o ejecuta su contenido en la pestaña SQL).

### 6. Ejecutar la aplicación
Con la base de datos iniciada y el entorno virtual activo:
```powershell
python main.py
```

### 7. Credenciales de acceso de prueba:
* **Administrador:** Usuario: `admin` | Contraseña: `admin123`
* **Vendedor / Cajero:** Usuario: `cajero1` | Contraseña: `cajero123`

---

## 📂 Estructura del Repositorio y Arquitectura

```text
Criollo/
│
├── .env.example                # Plantilla pública de variables de entorno para MySQL
├── .gitignore                  # Excluye .venv/, .env y __pycache__/ del repositorio
├── README.md                   # Esta guía general
├── requirements.txt            # Dependencias externas congeladas (customtkinter, mysql-connector, etc.)
├── main.py                     # Punto de entrada y orquestador del ciclo de vida del software
│
├── database/                   # Persistencia y scripts DDL (Jybran)
│   ├── conexion.py             # Administrador de contexto seguro para MySQL
│   └── schema.sql              # Estructura de tablas relacionales y datos semilla
│
├── models/                     # Consultas SQL preparadas y parametrizadas %s (Jybran)
│   ├── cliente_model.py        # Consultas de comensales
│   ├── pedido_model.py         # Transacciones atómicas, historial y estado de mesas
│   ├── producto_model.py       # CRUD de platos y protección referencial
│   └── usuario_model.py        # Autenticación de personal y roles
│
├── views/                      # Interfaz gráfica moderna con CustomTkinter (Bolivar)
│   ├── clientes_view.py        # Directorio de clientes y modal emergente
│   ├── dashboard_view.py       # Menú lateral y cabecera de sesión
│   ├── historial_pedidos_view.py # Historial de comprobantes y modales de cobro/detalle
│   ├── login_view.py           # Pantalla de acceso
│   ├── pedidos_view.py         # Terminal de pedidos, carrito y mesas
│   └── productos_view.py       # Catálogo de carta y modal de creación/edición
│
├── controllers/                # Lógica de negocio y precisión en RAM (Israel)
│   ├── cliente_controller.py   # Validaciones regex (DNI, teléfonos)
│   ├── login_controller.py     # Manejo de sesión activa
│   ├── pedido_controller.py    # Motor de pedidos en RAM (Decimal), mesas e historial
│   └── producto_controller.py  # Orquestador del CRUD de productos y protección contable
│
└── docs/                       # Documentación técnica oficial y auditoría (Alex)
    ├── El_proyecto.md          # Visión global del sistema y arquitectura
    ├── manual_tecnico.md       # Manual de ingeniería: justificación MVC, E-R, diccionario y despliegue
    ├── reglas_negocio.md       # Reglas operativas obligatorias (RN-ACC, RN-CLI, RN-PRO, RN-PED)
    ├── informe_auditoria_integracion.md # Informe de Aseguramiento de Calidad y Certificación QA
    ├── rol_alex.md             # Responsabilidades y entregables de Líder/QA
    ├── rol_bolivar.md          # Responsabilidades y entregables de Vistas
    ├── rol_israel.md           # Responsabilidades y entregables de Controladores
    └── rol_jybran.md           # Responsabilidades y entregables de Modelos y BD
```

---

## 📖 Documentación Técnica Oficial
Para un análisis exhaustivo de la ingeniería de software detrás del proyecto, consulta los documentos especializados en la carpeta [docs/](file:///C:/Users/ACER/Desktop/Criollo/docs/):
- **Fundamentos de Ingeniería y Buenas Prácticas:** Consulta [manual_tecnico.md](file:///C:/Users/ACER/Desktop/Criollo/docs/manual_tecnico.md) (Sección 1.1) para la explicación formal de por qué se adoptó el patrón MVC, por qué existe `main.py`, la necesidad de aislar con `.venv`, la portabilidad con `requirements.txt` y la seguridad con `.env`.
- **Diagrama Entidad-Relación y Diccionario de Datos:** En [manual_tecnico.md](file:///C:/Users/ACER/Desktop/Criollo/docs/manual_tecnico.md) (Secciones 2 y 3).
- **Reglas de Negocio Operativas:** En [reglas_negocio.md](file:///C:/Users/ACER/Desktop/Criollo/docs/reglas_negocio.md).
- **Informe de Certificación de Calidad (QA):** En [informe_auditoria_integracion.md](file:///C:/Users/ACER/Desktop/Criollo/docs/informe_auditoria_integracion.md).
