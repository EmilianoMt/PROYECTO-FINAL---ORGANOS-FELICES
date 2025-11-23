-- Crear BD, tabla y filas de ejemplo
CREATE DATABASE IF NOT EXISTS organos_felices CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE organos_felices;

CREATE TABLE IF NOT EXISTS organos (
    id_organo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

INSERT INTO organos (nombre, descripcion, precio) VALUES
('Riñón', 'Riñón sano', 80000.00),
('Cornea', 'Cornea sana', 70000.00),
('Higado adulto', 'Higado totalmente sano', 90000.00);