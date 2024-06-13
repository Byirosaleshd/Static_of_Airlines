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
	   ROUND((amount - (SELECT AVG(amount) FROM ticket_flights)) * (amount - (SELECT AVG(amount) FROM ticket_flights))/(SELECT COUNT(fare_conditions) FROM ticket_flights)) AS Varianza,
FROM ticket_flights
GROUP BY fare_conditions
ORDER BY 'Frecuencia del tipo de ticket' DESC;

SELECT * FROM Pregunta_2;

CREATE VIEW Pregunta_2_2 AS
SELECT *, SQRT(Varianza) AS 'Desviación tipica', (SQRT(Varianza)/Precio_Promedio) * 100 AS 'Coeficiente_de_variacion' FROM Pregunta_2;


SELECT * FROM Pregunta_2_2;



--3. Calcular las estadísticas básicas de los tickets dado el aeropuerto de destino.

CREATE VIEW Pregunta_3 AS
SELECT fare_conditions AS 'Tipo de ticket', 
        COUNT(fare_conditions) AS 'Frecuencia del tipo de ticket',
        ROUND(AVG(amount),2) AS Precio_Promedio,
        SUM(amount) AS 'Sum_precio',
        MAX(amount) AS 'Precio Maximo', 
        MIN(AMOUNT) AS 'Precio minimo', 
		MAX(amount) - MIN(amount) AS 'Rango'
        ROUND((amount - (SELECT AVG(amount) FROM ticket_flights)) * (amount - (SELECT AVG(amount) FROM ticket_flights))/(SELECT COUNT(fare_conditions) FROM ticket_flights)) AS Varianza,
FROM ticket_flights
INNER JOIN flights
ON ticket_flights.flight_id = flights.flight_id
GROUP BY arrival_airport
ORDER BY arrival_airport ASC;

CREATE VIEW Pregunta_3_2 AS
SELECT *, SQRT(Varianza) AS 'Desviación tipica', (SQRT(Varianza)/Precio_Promedio) * 100 AS 'Coeficiente_de_variacion' FROM Pregunta_3;


SELECT * FROM Pregunta_3_2;

	  
--4. Se requiere calcular la distancia en KM de los distintos aeropuertos que existen en la base de datos y con esta nueva variable mostrar las estadísticas básicas con respecto a la distancia de los vuelos.
CREATE VIEW Pregunta_4 AS
SELECT departure_airport,Distancia_km_llegada - Distancia_km_salida AS 'Distancia_recorrida_en _km', 
arrival_airport, ROUND(Distancia_km_salida,2) AS 'Distancia en km salida',
ROUND(Distancia_km_llegada,2) AS 'Distancia en km llegada',
	   ROUND(AVG(Distancia_km_llegada - Distancia_km_salida),2) AS 'Distancia Promedio en km',
	   ROUND(SUM(Distancia_km_llegada - Distancia_km_salida),2) AS 'Suma de la distancia en km',
	   ROUND(MAX(Distancia_km_llegada - Distancia_km_salida),2) AS 'Maxima distancia en km', 
	   ROUND(MIN(Distancia_km_llegada - Distancia_km_salida),2) AS 'Minima distancia en km',
	   ROUND(MAX(Distancia_km_llegada - Distancia_km_salida) - MIN(Distancia_km_llegada - Distancia_km_salida),2) AS 'Rango de la distancia'
  From Distancia
GROUP BY departure_airport
ORDER BY 'Distancia_recorrida_en_km' DESC
Limit 10;

SELECT * FROM Pregunta_4


SELECT *,strftime('%H',Time(scheduled_departure)) FROM flights;


--5. Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).

CREATE VIEW Pregunta_5 AS 
SELECT boarding_passes.flight_id AS 'ID_VUELO', 
		COUNT(boarding_passes.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		flights.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		flights.departure_airport AS 'AEROPUERTO DE SALIDA', 
		flights.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA',
		flights.arrival_airport AS 'AEROPUERTO DE LLEGADA',
		json_extract(airports_data.airport_name, '$.en') AS 'Nombre en ingles',
	json_extract(airports_data.airport_name, '$.ru') AS 'Nombre en ruso'
	FROM boarding_passes
	INNER JOIN flights ON boarding_passes.flight_id = flights.flight_id
	INNER JOIN airports_data ON flights.departure_airport = airports_data.airport_code
	GROUP BY boarding_passes.flight_id
	ORDER BY COUNT(boarding_passes.seat_no) DESC
	LIMIT 10;
	
SELECT * FROM Pregunta_5;