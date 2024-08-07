--1. Indicar los aeropuertos de llegada con mayor frecuencia.

CREATE VIEW Pregunta_1 AS
SELECT 
 	json_extract(airport_name, '$.en') AS 'Nombre en ingles',
	json_extract(airport_name, '$.ru') AS 'Nombre en ruso',
 flights.arrival_airport AS 'Codigo de Aeropuerto',
 flights.status AS 'Estado',
 count(*) AS 'Frecuencia de llegada'
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
SELECT Tipo_de_ticket AS 'Tipo de ticket',
	   Frecuencia,
	   Suma_del_precio AS 'Suma del Precio',
	   Precio_Maximo AS 'Precio Maximo',
	   Precio_Minimo AS 'Precio Minimo',
	   Rango,
	   Precio_Promedio AS 'Precio Promedio',
	   Varianza,
	   Desviacion_tipica AS 'Desviacion Tipica',
ROUND((Desviacion_tipica/Precio_Promedio) * 100,2) AS 'Coeficiente de variacion de Pearson'
	FROM 
(SELECT fare_conditions AS Tipo_de_ticket, 
	   COUNT(fare_conditions) AS Frecuencia,
	   SUM(amount) AS Suma_del_precio,
	   MAX(amount) AS Precio_Maximo, 
	   MIN(AMOUNT) AS Precio_minimo,
	   MAX(amount) - MIN(amount) AS Rango,
	   ROUND(AVG(amount),2) AS Precio_Promedio,
	   ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) * COUNT(fare_conditions) /(SELECT COUNT(fare_conditions) FROM ticket_flights)),2) AS Varianza,
	   ROUND(SQRT(
	    (POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) * COUNT(fare_conditions) /(SELECT COUNT(fare_conditions) FROM ticket_flights))
		),2) AS Desviacion_tipica
FROM ticket_flights
GROUP BY fare_conditions
ORDER BY Frecuencia DESC);

SELECT * FROM Pregunta_2;


--3. Calcular las estadísticas básicas de los tickets dado el aeropuerto de destino.
CREATE VIEW Pregunta_3 AS
SELECT arrival_airport AS 'Aeropuerto de destino',
	   Tipo_de_ticket AS 'Tipo de ticket',
	   Frecuencia,
	   Suma_del_precio AS 'Suma del Precio',
	   Precio_Maximo AS 'Precio Maximo',
	   Precio_Minimo AS 'Precio Minimo',
	   Rango,
	   Precio_Promedio AS 'Precio Promedio',
	   ROUND(Varianza) AS Varianza,
	   ROUND(Desviacion_tipica) AS 'Desviacion tipica',
	ROUND((Desviacion_tipica/Precio_Promedio) * 100 ,2) AS 'Coeficiente de variacion de Pearson'
	FROM 
(SELECT arrival_airport,
	   fare_conditions AS Tipo_de_ticket, 
	   COUNT(fare_conditions) AS Frecuencia, 
	   SUM(amount) AS Suma_del_precio,
	   MAX(amount) AS Precio_Maximo, 
	   MIN(AMOUNT) AS Precio_minimo,
	   MAX(amount) - MIN(amount) AS Rango,
	   ROUND(AVG(amount),2) AS Precio_Promedio,
	   ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(fare_conditions) FROM ticket_flights)),10) AS Varianza,
	   SQRT(
	    ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(fare_conditions) FROM ticket_flights)),10) 
		) AS Desviacion_tipica
FROM ticket_flights
INNER JOIN flights
ON ticket_flights.flight_id = flights.flight_id
GROUP BY arrival_airport
ORDER BY arrival_airport ASC)
LIMIT 10;
	  
	  	  
SELECT * FROM Pregunta_3;		  
	  
--4. Se requiere calcular la distancia en KM de los distintos aeropuertos que existen en la base de datos y con esta nueva variable mostrar las estadísticas básicas con respecto a la distancia de los vuelos.

-- Respuesta Forma 1
CREATE VIEW Pregunta_4_Forma_1  AS
SELECT *,
	ROUND((Desviacion_tipica/Promedio_distancia) * 100 ,2 )AS 'Coeficiente de variacion de Pearson'
	FROM (
SELECT
    Ciudad_salida AS 'Ciudad de salida',
    Ciudad_llegada AS 'Ciudad de llegada',
    flight_id 'Numero de vuelo',
	ROUND(AVG(distancia_km),2) AS Promedio_distancia,
	ROUND((POW(distancia_km - (SELECT avg_distancia FROM (SELECT AVG(distancia_km) AS avg_distancia FROM ticket_flights)),2) * COUNT(distancia_km) /(SELECT COUNT(distancia_km) FROM ticket_flights)),2) AS Varianza,
	 ROUND(SQRT(
	    (POW(distancia_km  - (SELECT avg_distancia FROM (SELECT AVG(distancia_km ) AS avg_distancia FROM ticket_flights)),2) * COUNT(distancia_km) /(SELECT COUNT(distancia_km ) FROM ticket_flights))
		),2) AS Desviacion_tipica
FROM (
    SELECT
        flight_id,
        Ciudad_salida,
        Ciudad_llegada,
        2 * 6371 * ASIN(SQRT(
            POWER(SIN(RADIANS((to_latitude - from_latitude) / 2)), 2) +
            COS(RADIANS(from_latitude)) * COS(RADIANS(to_latitude)) *
            POWER(SIN(RADIANS((to_longitude - from_longitude) / 2)), 2)
        )) AS distancia_km
    FROM (SELECT    
    flights.flight_id,
    json_extract(departure.city, '$.en') AS Ciudad_salida,
    CAST(SUBSTR(departure.coordinates, 2, INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_longitude,
    CAST(SUBSTR(departure.coordinates, INSTR(departure.coordinates, ',') + 1, LENGTH(departure.coordinates) - INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_latitude,
json_extract(arrival.city, '$.en') AS Ciudad_llegada,
    CAST(SUBSTR(arrival.coordinates, 2, INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_longitude,
    CAST(SUBSTR(arrival.coordinates, INSTR(arrival.coordinates, ',') + 1, LENGTH(arrival.coordinates) - INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_latitude
    from
    flights 
    INNER JOIN airports_data AS departure
    ON flights.departure_airport = departure.airport_code
    INNER JOIN airports_data AS arrival
    ON flights.arrival_airport = arrival.airport_code)
) AS subquery
GROUP BY Ciudad_salida, Ciudad_llegada 
ORDER BY distancia_km DESC);

SELECT * FROM Pregunta_4_Forma_1;





-- Respuesta Forma 2

CREATE VIEW Pregunta_4_Forma_2 AS
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

SELECT * FROM Pregunta_4_Forma_2






--5. Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).
CREATE VIEW Pregunta_5 AS
SELECT b.flight_id AS 'NUMERO DE VUELO', 
		COUNT(b.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		fl.departure_airport AS 'AEROPUERTO DE SALIDA', 
		json_extract(f.airport_name, '$.en') AS 'Nombre del Aeropuerto de salida en ingles',
		json_extract(f.airport_name, '$.ru') AS 'Nombre del Aeropuerto de salida en ruso',
		fl.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		fl.arrival_airport AS 'AEROPUERTO DE LLEGADA',
		json_extract(t.airport_name, '$.en') AS 'Nombre del Aeropuerto de llegada en ingles',
		json_extract(t.airport_name, '$.ru') AS 'Nombre del Aeropuerto de llegada en ruso',
		fl.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA'
		FROM
    flights AS fl
    INNER JOIN airports_data AS f
    ON fl.departure_airport = f.airport_code
    INNER JOIN airports_data AS t
    ON fl.arrival_airport = t.airport_code    
	INNER JOIN boarding_passes AS b
	ON fl.flight_id = b.flight_id
	GROUP BY b.flight_id
	ORDER BY COUNT(b.seat_no) DESC
    LIMIT 10;


			
SELECT * FROM Pregunta_5;

