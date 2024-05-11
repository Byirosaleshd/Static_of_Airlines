--1. Indicar los aeropuertos de llegada con mayor frecuencia.

CREATE VIEW Pregunta_1 AS
SELECT count(arrival_airport) AS 'Frecuencia de llegada', arrival_airport AS 'Aeropuerto', status AS 'Estado'
FROM flights 
WHERE status='Arrived'
 GROUP BY arrival_airport
 ORDER BY count(arrival_airport) DESC
 LIMIT 5;
 
SELECT * FROM Pregunta_1;

