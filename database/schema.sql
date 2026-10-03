USE el_rincon_criollo;

-- ============================================================
-- TABLA: usuarios
-- ============================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'vendedor'
);

-- ============================================================
-- TABLA: clientes
-- ============================================================
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(8) NOT NULL UNIQUE,
    telefono VARCHAR(15)
);

-- ============================================================
-- TABLA: productos
-- ============================================================
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);

-- ============================================================
-- TABLA: pedidos
-- ============================================================
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    usuario_id INT,
    mesa VARCHAR(20) NOT NULL,
    metodo_pago VARCHAR(20),
    total DECIMAL(10,2),
    estado VARCHAR(20) NOT NULL DEFAULT 'Pagado',
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- ============================================================
-- TABLA: detalle_pedidos
-- ============================================================
CREATE TABLE detalle_pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    nota_plato VARCHAR(150),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- ============================================================
-- DATOS INICIALES (SEEDS)
-- ============================================================

-- Usuario administrador por defecto
INSERT INTO usuarios (nombre, contrasena, rol) VALUES
('admin', 'admin123', 'administrador');

-- Cliente genérico para ventas sin cliente registrado
INSERT INTO clientes (nombre, dni, telefono) VALUES
('Público General', '00000000', '000000000');

-- Carta de platos criollos de muestra
INSERT INTO productos (nombre, categoria, precio, disponible) VALUES
('Ceviche Clásico',        'Entradas',        25.00, TRUE),
('Anticuchos',             'Entradas',        18.00, TRUE),
('Lomo Saltado',           'Platos de Fondo', 32.00, TRUE),
('Ají de Gallina',         'Platos de Fondo', 28.00, TRUE),
('Arroz con Pollo',        'Platos de Fondo', 26.00, TRUE),
('Papa a la Huancaína',    'Guarniciones',    15.00, TRUE),
('Choclo con Queso',       'Guarniciones',    12.00, TRUE),
('Chicha Morada (jarra)',  'Bebidas',         10.00, TRUE),
('Limonada Frozen',        'Bebidas',         12.00, TRUE),
('Suspiro a la Limeña',    'Postres',         14.00, TRUE),
('Picarones',              'Postres',         12.00, TRUE);