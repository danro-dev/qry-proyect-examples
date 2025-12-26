-- =============================================================================
-- Base de datos de ejemplo para qry-doc
-- Datos de ventas con múltiples tablas relacionadas
-- =============================================================================

-- Tabla de categorías
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(id),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT true
);

-- Tabla de regiones
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(100) DEFAULT 'México'
);

-- Tabla de vendedores
CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    region_id INTEGER REFERENCES regiones(id),
    fecha_contratacion DATE,
    activo BOOLEAN DEFAULT true
);

-- Tabla de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    telefono VARCHAR(20),
    region_id INTEGER REFERENCES regiones(id),
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- Tabla de ventas
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    producto_id INTEGER REFERENCES productos(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    cliente_id INTEGER REFERENCES clientes(id),
    cantidad INTEGER NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(5, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- Insertar datos de ejemplo
-- =============================================================================

-- Categorías
INSERT INTO categorias (nombre, descripcion) VALUES
    ('Electrónica', 'Dispositivos electrónicos y accesorios'),
    ('Ropa', 'Prendas de vestir para todas las edades'),
    ('Calzado', 'Zapatos, tenis y sandalias'),
    ('Accesorios', 'Gorras, bolsas, cinturones'),
    ('Hogar', 'Artículos para el hogar'),
    ('Deportes', 'Equipamiento deportivo');

-- Regiones
INSERT INTO regiones (nombre, pais) VALUES
    ('Norte', 'México'),
    ('Sur', 'México'),
    ('Centro', 'México'),
    ('Este', 'México'),
    ('Oeste', 'México');

-- Productos
INSERT INTO productos (nombre, categoria_id, precio_unitario, stock) VALUES
    ('Laptop Pro 15"', 1, 15999.99, 50),
    ('Smartphone X12', 1, 8999.99, 100),
    ('Audífonos Bluetooth', 1, 1299.99, 200),
    ('Tablet 10"', 1, 5999.99, 75),
    ('Smartwatch Sport', 1, 2499.99, 150),
    ('Camiseta Básica', 2, 299.99, 500),
    ('Jean Slim Fit', 2, 699.99, 300),
    ('Chamarra Invierno', 2, 1299.99, 100),
    ('Vestido Casual', 2, 599.99, 200),
    ('Playera Polo', 2, 449.99, 400),
    ('Tenis Running', 3, 1899.99, 150),
    ('Zapatos Formales', 3, 1499.99, 100),
    ('Sandalias Verano', 3, 399.99, 250),
    ('Botas Trabajo', 3, 1799.99, 80),
    ('Gorra Deportiva', 4, 249.99, 300),
    ('Mochila Urbana', 4, 799.99, 150),
    ('Cinturón Cuero', 4, 349.99, 200),
    ('Lentes de Sol', 4, 599.99, 180),
    ('Sartén Antiadherente', 5, 449.99, 120),
    ('Juego de Toallas', 5, 399.99, 200),
    ('Balón Fútbol', 6, 349.99, 100),
    ('Raqueta Tenis', 6, 899.99, 50);

-- Vendedores
INSERT INTO vendedores (nombre, email, region_id, fecha_contratacion) VALUES
    ('Ana García', 'ana.garcia@empresa.com', 3, '2022-01-15'),
    ('Carlos López', 'carlos.lopez@empresa.com', 1, '2021-06-01'),
    ('María Rodríguez', 'maria.rodriguez@empresa.com', 2, '2023-03-10'),
    ('Juan Martínez', 'juan.martinez@empresa.com', 4, '2022-08-20'),
    ('Lucía Hernández', 'lucia.hernandez@empresa.com', 5, '2021-11-05'),
    ('Pedro Sánchez', 'pedro.sanchez@empresa.com', 1, '2023-01-20'),
    ('Sofia Torres', 'sofia.torres@empresa.com', 2, '2022-05-15'),
    ('Miguel Flores', 'miguel.flores@empresa.com', 3, '2021-09-01');

-- Clientes
INSERT INTO clientes (nombre, email, telefono, region_id, fecha_registro) VALUES
    ('Empresa ABC', 'contacto@abc.com', '555-0101', 1, '2023-01-10'),
    ('Tienda XYZ', 'ventas@xyz.com', '555-0102', 2, '2023-02-15'),
    ('Comercial 123', 'info@123.com', '555-0103', 3, '2023-03-20'),
    ('Distribuidora Norte', 'norte@dist.com', '555-0104', 1, '2023-04-05'),
    ('Mayorista Sur', 'sur@mayorista.com', '555-0105', 2, '2023-05-12'),
    ('Retail Centro', 'centro@retail.com', '555-0106', 3, '2023-06-18'),
    ('Importadora Este', 'este@import.com', '555-0107', 4, '2023-07-22'),
    ('Exportadora Oeste', 'oeste@export.com', '555-0108', 5, '2023-08-30'),
    ('Mega Store', 'mega@store.com', '555-0109', 1, '2023-09-15'),
    ('Mini Market', 'mini@market.com', '555-0110', 2, '2023-10-01');

-- Ventas (datos de los últimos 6 meses)
INSERT INTO ventas (fecha, producto_id, vendedor_id, cliente_id, cantidad, precio_venta, descuento) VALUES
    -- Octubre 2024
    ('2024-10-05', 1, 1, 1, 2, 15999.99, 5.00),
    ('2024-10-08', 6, 2, 2, 10, 299.99, 0.00),
    ('2024-10-12', 11, 3, 3, 5, 1899.99, 10.00),
    ('2024-10-15', 15, 4, 4, 20, 249.99, 0.00),
    ('2024-10-18', 2, 5, 5, 3, 8999.99, 5.00),
    ('2024-10-22', 7, 6, 6, 8, 699.99, 0.00),
    ('2024-10-25', 19, 7, 7, 6, 449.99, 0.00),
    ('2024-10-28', 21, 8, 8, 15, 349.99, 5.00),
    
    -- Noviembre 2024
    ('2024-11-02', 3, 1, 9, 25, 1299.99, 10.00),
    ('2024-11-05', 8, 2, 10, 4, 1299.99, 0.00),
    ('2024-11-08', 12, 3, 1, 6, 1499.99, 5.00),
    ('2024-11-12', 16, 4, 2, 12, 799.99, 0.00),
    ('2024-11-15', 4, 5, 3, 8, 5999.99, 10.00),
    ('2024-11-18', 9, 6, 4, 15, 599.99, 0.00),
    ('2024-11-22', 20, 7, 5, 10, 399.99, 0.00),
    ('2024-11-25', 22, 8, 6, 3, 899.99, 5.00),
    ('2024-11-28', 5, 1, 7, 20, 2499.99, 15.00),
    
    -- Diciembre 2024
    ('2024-12-02', 1, 2, 8, 5, 15999.99, 10.00),
    ('2024-12-05', 6, 3, 9, 30, 299.99, 5.00),
    ('2024-12-08', 11, 4, 10, 10, 1899.99, 0.00),
    ('2024-12-12', 15, 5, 1, 50, 249.99, 10.00),
    ('2024-12-15', 2, 6, 2, 8, 8999.99, 5.00),
    ('2024-12-18', 7, 7, 3, 20, 699.99, 0.00),
    ('2024-12-22', 3, 8, 4, 40, 1299.99, 15.00),
    ('2024-12-25', 8, 1, 5, 6, 1299.99, 0.00),
    ('2024-12-28', 12, 2, 6, 8, 1499.99, 5.00),
    
    -- Enero 2025
    ('2025-01-03', 4, 3, 7, 12, 5999.99, 10.00),
    ('2025-01-06', 9, 4, 8, 25, 599.99, 0.00),
    ('2025-01-10', 16, 5, 9, 18, 799.99, 5.00),
    ('2025-01-13', 19, 6, 10, 8, 449.99, 0.00),
    ('2025-01-16', 21, 7, 1, 20, 349.99, 0.00),
    ('2025-01-20', 5, 8, 2, 15, 2499.99, 10.00),
    ('2025-01-23', 10, 1, 3, 30, 449.99, 5.00),
    ('2025-01-26', 13, 2, 4, 40, 399.99, 0.00),
    ('2025-01-29', 17, 3, 5, 25, 349.99, 0.00);

-- =============================================================================
-- Vista útil para análisis
-- =============================================================================

CREATE VIEW vista_ventas_detalle AS
SELECT 
    v.id as venta_id,
    v.fecha,
    p.nombre as producto,
    c.nombre as categoria,
    ve.nombre as vendedor,
    cl.nombre as cliente,
    r.nombre as region,
    v.cantidad,
    v.precio_venta,
    v.descuento,
    (v.cantidad * v.precio_venta * (1 - v.descuento/100)) as total_venta
FROM ventas v
JOIN productos p ON v.producto_id = p.id
JOIN categorias c ON p.categoria_id = c.id
JOIN vendedores ve ON v.vendedor_id = ve.id
JOIN clientes cl ON v.cliente_id = cl.id
JOIN regiones r ON ve.region_id = r.id;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos qry_ventas inicializada correctamente';
    RAISE NOTICE 'Tablas creadas: categorias, productos, regiones, vendedores, clientes, ventas';
    RAISE NOTICE 'Vista creada: vista_ventas_detalle';
END $$;
