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
SELECT fare_conditions AS 'Tipo de ticket', 
	   COUNT(fare_conditions) AS 'Frecuencia', 
	   SUM(amount) AS 'Suma del precio',
	   MAX(amount) AS 'Precio Maximo', 
	   MIN(AMOUNT) AS 'Precio minimo',
	   MAX(amount) - MIN(amount) AS 'Rango',
	   ROUND(AVG(amount),2) AS Price_Promedio,
	   ROUND((amount - (SELECT AVG(amount) FROM ticket_flights)) * (amount - (SELECT AVG(amount) FROM ticket_flights))/(SELECT COUNT(fare_conditions) FROM ticket_flights)) AS Varianza,
	   ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(fare_conditions) FROM ticket_flights)),2) AS Varianza2,
	   POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),3) AS Varianza3,
	   POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),3) AS Varianza4,
	   SQRT(
	    ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(fare_conditions) FROM ticket_flights)),2) 
		) AS Desviacion_tipica
FROM ticket_flights
GROUP BY fare_conditions
ORDER BY 'Frecuencia' DESC;

SELECT * FROM Pregunta_2;

CREATE VIEW Pregunta_2_2 AS
SELECT *, (Desviacion_tipica/Price_Promedio) * 100 AS 'Coeficiente_de_variacion',
Varianza3/Varianza2 * Desviacion_tipica AS Simetria,
Varianza4/Varianza2 * Varianza2 AS KURTOSIS
FROM Pregunta_2;





SELECT * FROM Pregunta_2_2;

select 
        fare_conditions, 
        count(*) as tickets_sold,
        avg(amount) as avg_per_ticket,
        sum(amount) as revenue_earned
from ticket_flights
group by fare_conditions
limit 10


CREATE TEMP TABLE FLIGHT_GEO_TICKET_2 AS

select *
from FLIGHT_INFO_ENRICHED_2 as fie
left join ticket_flights as tf on fie.flight_id = tf.flight_id


SELECT * FROM FLIGHT_GEO_TICKET_2

select *, (amount/average_distance_km) as amount_per_km
from FLIGHT_GEO_TICKET_2
WHERE amount_per_km > 0
order by amount_per_km asc
limit 10





-- Calculate the mean of average_distance_km
SELECT AVG(average_distance_km) AS avg_distance FROM FLIGHT_GEO_TICKET_2;

-- Calculate the mean of amount
SELECT AVG(amount) AS avg_amount FROM FLIGHT_GEO_TICKET_2;

-- Calculate the numerator
SELECT SUM((average_distance_km - (SELECT avg_distance FROM (SELECT AVG(average_distance_km) AS avg_distance FROM FLIGHT_GEO_TICKET_2))) * (amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM FLIGHT_GEO_TICKET_2))) ) AS numerator
FROM FLIGHT_GEO_TICKET_2;

-- Calculate the denominator
SELECT 
    SQRT(
        SUM(POW(average_distance_km - (SELECT avg_distance FROM (SELECT AVG(average_distance_km) AS avg_distance FROM FLIGHT_GEO_TICKET_2)), 2)) *
        SUM(POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM FLIGHT_GEO_TICKET_2)), 2))
    ) AS denominator
FROM FLIGHT_GEO_TICKET_2;

-- Calculate the correlation coefficient
SELECT (numerator / denominator) AS correlation
FROM (
    SELECT 
        SUM((average_distance_km - (SELECT avg_distance FROM (SELECT AVG(average_distance_km) AS avg_distance FROM FLIGHT_GEO_TICKET_2))) * (amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM FLIGHT_GEO_TICKET_2))) ) AS numerator,
        SQRT(
            SUM(POW(average_distance_km - (SELECT avg_distance FROM (SELECT AVG(average_distance_km) AS avg_distance FROM FLIGHT_GEO_TICKET_2)), 2)) *
            SUM(POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM FLIGHT_GEO_TICKET_2)), 2))
        ) AS denominator
    FROM FLIGHT_GEO_TICKET_2
) AS temp;








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





SELECT fl.flight_id, f.city as from_city, f.coordinates as from_coordinates, t.city as to_city, t.coordinates as to_coordinates from
    flights as fl
    left join airports_data as f
    on fl.departure_airport = f.airport_code
    left join airports_data as t
    on fl.arrival_airport = t.airport_code    
    limit 10;


CREATE TEMP TABLE FLIGHT_INFO AS

SELECT    
    flights.flight_id,
    json_extract(departure.city, '$.en') AS from_city,
    CAST(SUBSTR(departure.coordinates, 2, INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_longitude,
    CAST(SUBSTR(departure.coordinates, INSTR(departure.coordinates, ',') + 1, LENGTH(departure.coordinates) - INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_latitude,

json_extract(arrival.city, '$.en') AS to_city,
    CAST(SUBSTR(arrival.coordinates, 2, INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_longitude,
    CAST(SUBSTR(arrival.coordinates, INSTR(arrival.coordinates, ',') + 1, LENGTH(arrival.coordinates) - INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_latitude

    from
    flights 
    left join airports_data as departure
    on flights.departure_airport = departure.airport_code
    left join airports_data as arrival
    on flights.arrival_airport = arrival.airport_code    
    ;

    
CREATE INDEX idx_flight_id ON FLIGHT_INFO (flight_id);



select *
from FLIGHT_INFO
limit 10

CREATE TEMP TABLE FLIGHT_INFO_ENRICHED_2 AS

-- Calculate the average distance for each unique combination of from_city and to_city
SELECT
    from_city,
    to_city,
    flight_id,

    AVG(distance_km) AS average_distance_km
FROM (
    -- Subquery to calculate the distances as before
    SELECT
        flight_id,
        from_city,
        to_city,
        -- Calculate the distance using the Haversine formula
        2 * 6371 * ASIN(SQRT(
            POWER(SIN(RADIANS((to_latitude - from_latitude) / 2)), 2) +
            COS(RADIANS(from_latitude)) * COS(RADIANS(to_latitude)) *
            POWER(SIN(RADIANS((to_longitude - from_longitude) / 2)), 2)
        )) AS distance_km
    FROM FLIGHT_INFO
) AS subquery
GROUP BY from_city, to_city, flight_id
order by average_distance_km desc

SELECT count(*)
from FLIGHT_INFO_ENRICHED_2

-- Create a histogram distribution of average_distance_km
SELECT
    FLOOR(average_distance_km / 1000) * 1000 AS distance_range,
    COUNT(*) AS count
FROM (
    -- Calculate the average distance for each unique combination of from_city and to_city
    SELECT
        from_city,
        to_city,
        AVG(distance_km) AS average_distance_km
    FROM (
        -- Subquery to calculate the distances as before
        SELECT
            from_city,
            to_city,
            -- Calculate the distance using the Haversine formula
            2 * 6371 * ASIN(SQRT(
                POWER(SIN(RADIANS((to_latitude - from_latitude) / 2)), 2) +
                COS(RADIANS(from_latitude)) * COS(RADIANS(to_latitude)) *
                POWER(SIN(RADIANS((to_longitude - from_longitude) / 2)), 2)
            )) AS distance_km
        FROM FLIGHT_INFO
    ) AS subquery
    GROUP BY from_city, to_city
) AS distances
GROUP BY distance_range
ORDER BY distance_range;








--5. Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).

CREATE VIEW Pregunta_5 AS 
SELECT boarding_passes.flight_id AS 'NUMERO DE VUELO', 
		COUNT(boarding_passes.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		flights.departure_airport AS 'AEROPUERTO DE SALIDA', 
		flights.arrival_airport AS 'AEROPUERTO DE LLEGADA',
		flights.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		flights.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA'
	FROM boarding_passes
	INNER JOIN flights ON boarding_passes.flight_id = flights.flight_id
	INNER JOIN airports_data ON flights.departure_airport = airports_data.airport_code
	GROUP BY boarding_passes.flight_id
	ORDER BY COUNT(boarding_passes.seat_no) DESC
	LIMIT 10;
			
SELECT * FROM Pregunta_5;


SELECT b.flight_id AS 'NUMERO DE VUELO', 
		COUNT(b.seat_no) AS 'NUMERO DE ASIENTOS OCUPADOS', 
		fl.departure_airport AS 'AEROPUERTO DE SALIDA', 
		fl.arrival_airport AS 'AEROPUERTO DE LLEGADA',
		fl.scheduled_departure AS 'FECHA Y HORA DE SALIDA',
		fl.scheduled_arrival AS 'FECHA Y HORA DE LLEGADA', * FROM
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