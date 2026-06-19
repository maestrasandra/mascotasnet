-- =======================================================
--  MascotasNet — Base de Datos Corregida y Mejorada
--  Compatible con Django + MySQL
-- =======================================================

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mascotasnet
-- -----------------------------------------------------
-- DROP SCHEMA IF EXISTS `mascotasnet`;
CREATE SCHEMA IF NOT EXISTS `mascotasnet` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `mascotasnet`;

-- -----------------------------------------------------
-- Tabla: usuario
-- CORRECCIÓN: contraseña_hash VARCHAR(255) para soportar
--             hashes reales de bcrypt/PBKDF2
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario`        INT           NOT NULL AUTO_INCREMENT,
  `nombre`            VARCHAR(45)   NOT NULL,
  `apellido`          VARCHAR(45)   NOT NULL,
  `correo`            VARCHAR(100)  NOT NULL,
  `contraseña_hash`   VARCHAR(255)  NOT NULL,  -- ✔ corregido de 45 a 255
  `rol`               ENUM('cliente', 'administrador') NOT NULL DEFAULT 'cliente',
  `fecha_registro`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo`            TINYINT(1)    NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `correo_UNIQUE` (`correo` ASC)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: mascota
-- CORRECCIÓN: agregados campos nombre, sexo e imagen
--             que la página necesita para mostrar info
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mascota` (
  `id_mascota`        INT           NOT NULL AUTO_INCREMENT,
  `nombre`            VARCHAR(45)   NOT NULL,  -- ✔ nuevo: tu página muestra el nombre
  `especie`           VARCHAR(45)   NOT NULL,
  `raza`              VARCHAR(45)   NOT NULL,
  `edad`              INT           NOT NULL,
  `sexo`              ENUM('Macho', 'Hembra') NOT NULL,  -- ✔ nuevo
  `estado_salud`      VARCHAR(100)  NOT NULL,
  `descripcion`       TEXT,                              -- ✔ nuevo: descripción larga
  `imagen`            VARCHAR(255)  DEFAULT NULL,        -- ✔ nuevo: ruta de la imagen
  `estado_adopcion`   ENUM('Disponible', 'En proceso', 'Adoptada') NOT NULL DEFAULT 'Disponible',
  `fecha_ingreso`     DATE          NOT NULL DEFAULT (CURRENT_DATE),
  PRIMARY KEY (`id_mascota`)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: solicitud_adopcion
-- CORRECCIÓN: eliminada columna redundante codigo_usuario
--             (ya existe usuario_id_usuario para la FK)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solicitud_adopcion` (
  `id_adopcion`         INT     NOT NULL AUTO_INCREMENT,
  `fecha_solicitud`     DATE    NOT NULL DEFAULT (CURRENT_DATE),
  `estado`              ENUM('pendiente', 'aprobada', 'rechazada') NOT NULL DEFAULT 'pendiente',
  `notas`               TEXT    DEFAULT NULL,           -- ✔ nuevo: observaciones del admin
  `usuario_id_usuario`  INT     NOT NULL,
  `mascota_id_mascota`  INT     NOT NULL,
  PRIMARY KEY (`id_adopcion`),
  INDEX `fk_adopcion_usuario_idx`  (`usuario_id_usuario` ASC),
  INDEX `fk_adopcion_mascota_idx`  (`mascota_id_mascota` ASC),
  CONSTRAINT `fk_adopcion_usuario`
    FOREIGN KEY (`usuario_id_usuario`) REFERENCES `usuario` (`id_usuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_adopcion_mascota`
    FOREIGN KEY (`mascota_id_mascota`) REFERENCES `mascota` (`id_mascota`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: producto
-- CORRECCIÓN: descripcion TEXT (sin longitud),
--             agregados stock e imagen
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `producto` (
  `id_producto`         INT             NOT NULL AUTO_INCREMENT,
  `nombre`              VARCHAR(100)    NOT NULL,
  `categoria`           VARCHAR(45)     NOT NULL,
  `descripcion`         TEXT            NOT NULL,  -- ✔ corregido: TEXT sin longitud
  `precio`              DECIMAL(12, 2)  NOT NULL,  -- ✔ corregido: decimales definidos
  `stock`               INT             NOT NULL DEFAULT 0,  -- ✔ nuevo: unidades disponibles
  `imagen`              VARCHAR(255)    DEFAULT NULL,        -- ✔ nuevo: ruta de imagen
  `disponibilidad`      TINYINT(1)      NOT NULL DEFAULT 1,
  `usuario_id_usuario`  INT             NOT NULL,
  PRIMARY KEY (`id_producto`),
  INDEX `fk_producto_usuario_idx` (`usuario_id_usuario` ASC),
  CONSTRAINT `fk_producto_usuario`
    FOREIGN KEY (`usuario_id_usuario`) REFERENCES `usuario` (`id_usuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: carrito
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `carrito` (
  `id_carrito`          INT       NOT NULL AUTO_INCREMENT,
  `fecha_creacion`      DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado`              ENUM('activo', 'cerrado') NOT NULL DEFAULT 'activo',
  `usuario_id_usuario`  INT       NOT NULL,
  PRIMARY KEY (`id_carrito`),
  INDEX `fk_carrito_usuario_idx` (`usuario_id_usuario` ASC),
  CONSTRAINT `fk_carrito_usuario`
    FOREIGN KEY (`usuario_id_usuario`) REFERENCES `usuario` (`id_usuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: detalle_carrito
-- CORRECCIÓN: agregado precio_unitario para guardar
--             el precio al momento de agregar al carrito
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_carrito` (
  `id_carrito`      INT             NOT NULL,
  `id_producto`     INT             NOT NULL,
  `cantidad`        INT             NOT NULL DEFAULT 1,
  `precio_unitario` DECIMAL(12, 2)  NOT NULL,  -- ✔ nuevo: precio al momento de compra
  PRIMARY KEY (`id_carrito`, `id_producto`),
  INDEX `fk_detalle_producto_idx` (`id_producto` ASC),
  CONSTRAINT `fk_detalle_carrito`
    FOREIGN KEY (`id_carrito`) REFERENCES `carrito` (`id_carrito`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_producto`
    FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabla: articulo_informativo
-- CORRECCIÓN: PRIMARY KEY solo codigo_articulo
--             (antes era compuesta innecesariamente)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `articulo_informativo` (
  `codigo_articulo`     INT          NOT NULL AUTO_INCREMENT,
  `titulo`              VARCHAR(150) NOT NULL,  -- ✔ ampliado de 45 a 150
  `contenido`           TEXT         NOT NULL,
  `fecha_publicacion`   DATE         NOT NULL DEFAULT (CURRENT_DATE),
  `categoria`           VARCHAR(45)  NOT NULL,
  `imagen`              VARCHAR(255) DEFAULT NULL,  -- ✔ nuevo
  `usuario_id_usuario`  INT          NOT NULL,
  PRIMARY KEY (`codigo_articulo`),              -- ✔ corregido: PK simple
  INDEX `fk_articulo_usuario_idx` (`usuario_id_usuario` ASC),
  CONSTRAINT `fk_articulo_usuario`
    FOREIGN KEY (`usuario_id_usuario`) REFERENCES `usuario` (`id_usuario`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- =======================================================
--  Datos de prueba para arrancar el proyecto
-- =======================================================

-- Usuario administrador de prueba
-- Contraseña: admin123 (en Django se hashea automáticamente)
INSERT IGNORE INTO `usuario` (`nombre`, `apellido`, `correo`, `contraseña_hash`, `rol`)
VALUES ('Admin', 'MascotasNet', 'admin@mascotasnet.com', 'temporal_django_hashea_esto', 'administrador');

-- Mascotas de prueba
INSERT IGNORE INTO `mascota` (`nombre`, `especie`, `raza`, `edad`, `sexo`, `estado_salud`, `descripcion`, `estado_adopcion`)
VALUES
  ('Max',    'Perro',  'Labrador',  3, 'Macho',  'Excelente', 'Muy amigable y juguetón. Le encanta correr.',      'Disponible'),
  ('Luna',   'Gato',   'Persa',     2, 'Hembra', 'Excelente', 'Tranquila y cariñosa. Ideal para apartamentos.',   'Disponible'),
  ('Bolita', 'Conejo', 'Holandés',  1, 'Macho',  'Buena',     'Pequeño y curioso. Ya está en proceso de adopción.','En proceso');

-- Productos de prueba
INSERT IGNORE INTO `producto` (`nombre`, `categoria`, `descripcion`, `precio`, `stock`, `usuario_id_usuario`)
VALUES
  ('Alimento Premium para Perros', 'Alimentos',  'Alimento balanceado bolsa 5kg, rico en proteínas.', 189900.00, 15, 1),
  ('Juguete Interactivo para Gatos','Juguetes',  'Pelota con cascabel, resistente y segura.',           53900.00, 25, 1),
  ('Shampoo Hipoalergénico',        'Cuidado',   'Shampoo suave para todo tipo de pelaje, 500ml.',      76500.00, 30, 1);

-- Artículo de prueba
INSERT IGNORE INTO `articulo_informativo` (`titulo`, `contenido`, `categoria`, `usuario_id_usuario`)
VALUES ('Guía Completa de Cuidado de Perros', 'Aprende todo sobre el cuidado diario de tu perro...', 'Cuidado General', 1);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
