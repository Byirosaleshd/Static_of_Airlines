--1. Indicar los aeropuertos de llegada con mayor frecuencia.

CREATE VIEW Pregunta_1 AS
SELECT count(flights.arrival_airport) AS 'Frecuencia de llegada', airports_data.airport_name AS 'Nombre del Aeropuerto', flights.arrival_airport AS 'Aeropuerto', flights.status AS 'Estado'
FROM flights 
INNER JOIN airports_data 
ON flights.arrival_airport = airports_data.airport_code
WHERE status='Arrived'
GROUP BY arrival_airport
ORDER BY count(arrival_airport) DESC
LIMIT 5;
 
SELECT * FROM Pregunta_1;

--5. Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).

CREATE VIEW PREGUNTA_5 AS 
SELECT boarding_passes.flight_id AS 'ID_VUELO', 
		COUNT(boarding_passes.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		flights.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		flights.departure_airport AS 'AEROPUERTO DE SALIDA', 
		flights.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA',
		flights.arrival_airport AS 'AEROPUERTO DE LLEGADA'
	FROM boarding_passes
	INNER JOIN flights ON boarding_passes.flight_id = flights.flight_id
	GROUP BY boarding_passes.flight_id
	ORDER BY COUNT(boarding_passes.seat_no) DESC
	LIMIT 10;
	
	SELECT * FROM PREGUNTA_5;


