
--CREACION DE TABLAS

CREATE TABLE Chiste(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje VARCHAR(5000)
);

CREATE TABLE Usuario(
    chat_id VARCHAR(100) UNIQUE,
    user VARCHAR(500) PRIMARY KEY
);

CREATE TABLE Cita(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(500) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME,
    mensaje_enviado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario) REFERENCES Usuario(user) 
);


--Ejecutar la siguiente consulta
SET GLOBAL event_scheduler = ON;

--EVENTO PARA QUE SE BORREN TODAS LAS FECHAS ANTERIORES AL DÍA Y HORA ACTUAL
CREATE EVENT eliminar_citas_antiguas
ON SCHEDULE EVERY 30 MINUTE
DO
  DELETE FROM Cita
  WHERE hora < NOW() and fecha < NOW();


--TRIGGER PARA EVITAR QUE SE ALMACENEN FECHAS Y HORAS ACTUALES
delimiter //
CREATE TRIGGER no_fecha_anterior
BEFORE INSERT ON Cita
FOR EACH ROW
BEGIN
  IF CONCAT(NEW.fecha, ' ', NEW.hora) < NOW() THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden almacenar fechas y horas anteriores a la actual';
  END IF;
END;



