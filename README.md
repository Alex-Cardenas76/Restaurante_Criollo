# El Rincón Criollo - Sistema de Gestión de Ventas

Aplicación de escritorio desarrollada en **Python** y **MySQL** para la administración comercial y control de pedidos en el restaurante "El Rincón Criollo". Diseñada para operar de forma **100% local** (offline) sin depender de servicios web ni conectividad a internet.

---

## 📌 Resumen del Proyecto

El objetivo del equipo es construir un **Producto Mínimo Viable (MVP) operativo al 70%** enfocado en cuatro módulos principales:
1. **Control de Acceso (Login):** Autenticación de usuarios con permisos y trazabilidad de turnos.
2. **Catálogos y Directorio:** Registro y listado de clientes frecuentes y la carta de platos criollos (con control de disponibilidad).
3. **Punto de Venta / Caja (Núcleo):** Toma de pedidos asignando mesa y método de pago, con cálculo aritmético exacto en memoria RAM en tiempo real (`Decimal`). Al confirmar, se realiza el guardado atómico en base de datos desglosado en cabecera (`pedidos`) y renglones (`detalle_pedidos`).
4. **Dashboard Principal:** Navegación fluida y centralizada entre módulos.

---

## 👥 Equipo y Distribución de Responsabilidades (MVC + QA)

> [!IMPORTANT]
> **Lectura Obligatoria para todos los integrantes antes de programar:**
> Para evitar confusiones, conflictos en el repositorio y cruces de código, **es indispensable que cada miembro lea:**
> 1. El archivo general de [reglas_negocio.md](file:///C:/Users/ACER/Desktop/Criollo/docs/reglas_negocio.md).
> 2. Su archivo de rol asignado dentro de la carpeta `docs/` para tener 100% claro qué le corresponde hacer y qué límites técnicos debe respetar.

El proyecto sigue una estricta separación bajo el patrón **Modelo-Vista-Controlador**:

| Integrante | Rol | Capa / Responsabilidad | Documento de Lectura Obligatoria | Carpeta |
| :--- | :--- | :--- | :--- | :--- |
| **Jybran** | Modelo / Base de Datos | Scripts SQL, conexión y consultas preparadas. | [rol_jybran.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_jybran.md) | `database/`, `models/` |
| **Bolivar** | Vista / Interfaz | CustomTkinter, Treeviews, formularios y alertas. | [rol_bolivar.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_bolivar.md) | `views/` |
| **Israel** | Controlador / Lógica | Reglas de negocio, validaciones (`re`), RAM (`Decimal`). | [rol_israel.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_israel.md) | `controllers/`, `main.py` |
| **Alex** | Líder / QA y Documentación | Auditoría de reglas, manual técnico y coordinación. | [rol_alex.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_alex.md) | `docs/` |

---

## 🚀 Guía de Instalación y Puesta en Marcha

Sigue estos pasos en tu computadora para configurar el entorno de trabajo sin conflictos con el equipo:

### 1. Clonar el repositorio
Abre una terminal y clona el proyecto:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Criollo
```

### 2. Crear y activar el entorno virtual (`venv`)
Crea un entorno aislado para que las dependencias se instalen solo en este proyecto:

* **En Windows (PowerShell / CMD):**
```powershell
# Crear el entorno virtual en la carpeta .venv
python -m venv .venv

# Activar el entorno virtual
.venv\Scripts\activate
```
*(Al activarse verás el prefijo `(.venv)` a la izquierda de tu terminal).*

### 3. Instalar las dependencias
Con el entorno virtual activado, instala todas las librerías necesarias con un solo comando:
```powershell
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno (`.env`)
Para que no choquemos con las contraseñas ni puertos de MySQL entre compañeros:
1. Copia el archivo `.env.example` y renómbralo como `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Abre el nuevo archivo `.env` y edita tus credenciales locales de XAMPP (por ejemplo, si tienes contraseña o usas el puerto 3307).

> **Nota importante:** El archivo `.env` está en el `.gitignore`, por lo que **nunca se subirá a GitHub**, protegiendo tu configuración local.

### 5. Configurar la Base de Datos en MySQL (XAMPP)
1. Abre el panel de control de **XAMPP** e inicia los módulos **Apache** y **MySQL**.
2. Entra a **phpMyAdmin** en tu navegador (`http://localhost/phpmyadmin`).
3. Crea la base de datos `el_rincon_criollo`.
4. Ve a la pestaña **Importar** y selecciona el archivo `database/schema.sql` (o copia y ejecuta su contenido en la pestaña SQL).

### 6. Ejecutar la aplicación
Con la base de datos iniciada y el entorno virtual activo:
```powershell
python main.py
```

---

## 📂 Estructura del Repositorio

```text
Criollo/
│
├── .env.example                # Plantilla pública de variables de entorno para MySQL
├── .gitignore                  # Excluye .venv/, .env y __pycache__/ del repositorio
├── README.md                   # Esta guía general
├── requirements.txt            # Dependencias externas (customtkinter, mysql-connector, etc.)
├── main.py                     # Archivo de inicio del software
│
├── database/                   # Conexión y script DDL de la BD
│   ├── conexion.py
│   └── schema.sql
│
├── models/                     # Consultas SQL por entidad (Jybran)
│   ├── cliente_model.py
│   ├── pedido_model.py
│   ├── producto_model.py
│   └── usuario_model.py
│
├── views/                      # Pantallas e interfaces CustomTkinter (Bolivar)
│   ├── clientes_view.py
│   ├── dashboard_view.py
│   ├── login_view.py
│   ├── pedidos_view.py
│   └── productos_view.py
│
├── controllers/                # Lógica de negocio y orquestación en RAM (Israel)
│   ├── cliente_controller.py
│   ├── login_controller.py
│   ├── pedido_controller.py
│   └── producto_controller.py
│
└── docs/                       # Documentación y seguimiento (Alex)
    ├── El_proyecto.md          # Resumen técnico extenso y diagrama E-R
    ├── reglas_negocio.md       # Reglas de negocio operativas y validaciones
    ├── manual_tecnico.md       # Manual técnico y de usuario paso a paso
    ├── informe_auditoria_integracion.md # Informe de auditoría e integración MVC
    ├── rol_alex.md             # Funciones de QA y Líder
    ├── rol_bolivar.md          # Funciones de Vistas
    ├── rol_israel.md           # Funciones de Controladores
    └── rol_jybran.md           # Funciones de Modelos y BD
```

---

## 📖 Documentación Detallada
Para conocer a fondo las reglas técnicas, los contratos de comunicación y la matriz de responsabilidades, consulta los archivos en la carpeta [docs/](file:///C:/Users/ACER/Desktop/Criollo/docs/):
- **Visión General y Diagrama E-R:** [El_proyecto.md](file:///C:/Users/ACER/Desktop/Criollo/docs/El_proyecto.md)
- **Manual Técnico y de Usuario:** [manual_tecnico.md](file:///C:/Users/ACER/Desktop/Criollo/docs/manual_tecnico.md)
- **Informe de Auditoría e Integración:** [informe_auditoria_integracion.md](file:///C:/Users/ACER/Desktop/Criollo/docs/informe_auditoria_integracion.md)
- **Reglas de Negocio del Sistema:** [reglas_negocio.md](file:///C:/Users/ACER/Desktop/Criollo/docs/reglas_negocio.md)
- **Rol de Jybran (Base de Datos):** [rol_jybran.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_jybran.md)
- **Rol de Bolivar (Vistas):** [rol_bolivar.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_bolivar.md)
- **Rol de Israel (Controladores):** [rol_israel.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_israel.md)
- **Rol de Alex (QA y Líder):** [rol_alex.md](file:///C:/Users/ACER/Desktop/Criollo/docs/rol_alex.md)
