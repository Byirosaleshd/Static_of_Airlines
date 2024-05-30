--1. Indicar los aeropuertos de llegada con mayor frecuencia.

CREATE VIEW Pregunta_1 AS
SELECT count(flights.arrival_airport) AS 'Frecuencia de llegada',
 	json_extract(airport_name, '$.en') AS 'Nombre en ingles',
	json_extract(airport_name, '$.ru') AS 'Nombre en ruso',
 flights.arrival_airport AS 'Aeropuerto',
 flights.status AS 'Estado'
FROM flights 
INNER JOIN airports_data 
ON flights.arrival_airport = airports_data.airport_code
WHERE status='Arrived'
GROUP BY arrival_airport
ORDER BY count(arrival_airport) DESC
LIMIT 5;

SELECT * FROM Pregunta_1;

--2. Calcular las estadísticas básicas de los tickets dado su tipo
CREATE VIEW Pregunta_2 AS 
SELECT fare_conditions AS 'Tipo de ticket', 
	   COUNT(fare_conditions) AS 'Frecuencia del tipo de ticket', 
	   ROUND(AVG(amount),2) AS 'Precio Promedio',
	   SUM(amount) AS 'Suma del precio',
	   MAX(amount) AS 'Precio Maximo', 
	   MIN(AMOUNT) AS 'Precio minimo',
	   MAX(amount) - MIN(amount) AS 'Rango'
FROM ticket_flights
GROUP BY fare_conditions
ORDER BY Frecuencia DESC;

SELECT * FROM Pregunta_2;

--3. Calcular las estadísticas básicas de los tickets dado el aeropuerto de destino.

CREATE VIEW Pregunta_3 AS
SELECT fare_conditions AS 'Tipo de ticket', 
        COUNT(fare_conditions) AS 'Frecuencia del tipo de ticket',
        ROUND(AVG(amount),2) AS 'Precio_Promedio',
        SUM(amount) AS 'Sum_precio',
        MAX(amount) AS 'Precio Maximo', 
        MIN(AMOUNT) AS 'Precio minimo', 
        ROUND((amount - (SELECT AVG(amount) FROM ticket_flights)) * (amount - (SELECT AVG(amount) FROM ticket_flights))/(SELECT COUNT(fare_conditions) FROM ticket_flights))  AS 'Varianza'
FROM ticket_flights
GROUP BY fare_conditions
ORDER BY fare_conditions DESC;

SELECT *, SQRT(Varianza) AS 'Desviación tipica', SQRT(Varianza)/Precio_Promedio * 100 AS 'Coeficiente de variacion' FROM Pregunta_3


--5. Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).

CREATE VIEW PREGUNTA_5 AS 
SELECT boarding_passes.flight_id AS 'ID_VUELO', 
		COUNT(boarding_passes.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		flights.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		flights.departure_airport AS 'AEROPUERTO DE SALIDA', 
		flights.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA',
		flights.arrival_airport AS 'AEROPUERTO DE LLEGADA',
		airports_data.airport_name,
		json_extract(airports_data.airport_name, '$.en') AS 'Nombre en ingles',
	json_extract(airports_data.airport_name, '$.ru') AS 'Nombre en ruso'
	FROM boarding_passes
	INNER JOIN flights ON boarding_passes.flight_id = flights.flight_id
	INNER JOIN airports_data ON flights.departure_airport = airports_data.airport_code
	GROUP BY boarding_passes.flight_id
	ORDER BY COUNT(boarding_passes.seat_no) DESC
	LIMIT 10;
	
SELECT * FROM PREGUNTA_5;


