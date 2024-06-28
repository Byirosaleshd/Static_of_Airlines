Pregunta_A = """SELECT flights.flight_id, flights.flight_no, flights.scheduled_departure, flights.scheduled_arrival, flights.departure_airport, flights.arrival_airport, flights.status, flights.aircraft_code, aircrafts_data.model, json_extract(aircrafts_data.model, '$.en') AS 'Nombre en ingles', json_extract(aircrafts_data.model, '$.ru') AS 'Nombre en ruso' FROM flights INNER JOIN aircrafts_data ON aircrafts_data.aircraft_code = flights.aircraft_code WHERE flights.status IN ('Arrived', 'On Time');"""

PreguntaA1 = "SELECT aircraft_code AS 'CÓDIGO DE AVIÓN', COUNT(CASE WHEN scheduled_arrival LIKE '%2017-07%' THEN 1 END) AS 'VUELOS EN 2017-07', COUNT(CASE WHEN scheduled_arrival LIKE '%2017-08%' THEN 1 END) AS 'VUELOS EN 2017-08', COUNT(aircraft_code) AS 'VUELOS VENDIDOS' FROM flights WHERE scheduled_arrival BETWEEN '2017-07-01' AND '2017-08-31' AND status = 'Arrived' GROUP BY aircraft_code ORDER BY COUNT(aircraft_code) DESC;"

PreguntaA2 = "SELECT aircraft_code AS 'CODIGO DE AVION', range AS 'ALCANCE DEL AVION' FROM aircrafts_data ORDER BY range DESC;"

PreguntaB = "SELECT flights.aircraft_code AS 'CodigodeAvion', SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS 'Economy', SUM(CASE WHEN ticket_flights.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS 'Business', SUM(CASE WHEN ticket_flights.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS 'Comfort', COUNT(ticket_flights.fare_conditions) AS 'Asientos vendidos' FROM flights INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id WHERE flights.status = 'Arrived' GROUP BY flights.aircraft_code ORDER BY SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) DESC;"

Pregunta_B = "SELECT flights.aircraft_code AS 'CodigodeAvion', SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS 'Economy', SUM(CASE WHEN ticket_flights.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS 'Business', SUM(CASE WHEN ticket_flights.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS 'Comfort', COUNT(ticket_flights.fare_conditions) AS 'Asientos Vendidos' FROM flights INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id  WHERE flights.status = 'Arrived' GROUP BY flights.aircraft_code ORDER BY SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) DESC;"


PreguntaC = """
SELECT
    arrival_airport,
    fare_conditions,
    COUNT(amount) AS num_flights,
    AVG(amount) AS avg_price,
    MIN(amount) AS min_price,
    MAX(amount) AS max_price,
	ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(*) FROM ticket_flights)),2) AS Varianza,
	SQRT(
		ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(*) FROM ticket_flights)),2) 
		) AS Desviacion_tipica,
	SQRT(
		ROUND((POW(amount - (SELECT avg_amount FROM (SELECT AVG(amount) AS avg_amount FROM ticket_flights)),2) /(SELECT COUNT(*) FROM ticket_flights)),2) 
		) / AVG(amount) AS Coeficiente_de_variacion
FROM 
    (SELECT
    flights.flight_no,
    flights.departure_airport,
    flights.arrival_airport,
    flights.status,
    flights.aircraft_code,
    ticket_flights.amount,
    ticket_flights.fare_conditions,
    aircrafts_data.model
FROM
    flights
INNER JOIN
    aircrafts_data
ON
    flights.aircraft_code = aircrafts_data.aircraft_code
INNER JOIN
    ticket_flights
ON
    flights.flight_id = ticket_flights.flight_id
WHERE
    flights.aircraft_code IN ('773', '763', 'SU9'))
GROUP BY
    arrival_airport, fare_conditions
ORDER BY
    arrival_airport, fare_conditions;
"""

Pregunta_C1 = "SELECT aircraft_code AS Avion, COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') THEN 1 END) AS 'Europa-Europa', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') THEN 1 END) AS 'Europa-Asia', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') THEN 1 END) AS 'Asia-Europa', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') THEN 1 END) AS 'Asia-Asia', COUNT(aircraft_code) AS 'Vuelos Totales' FROM flights WHERE status = 'Arrived' GROUP BY aircraft_code ORDER BY 'Europa-Europa' DESC;"

Pregunta_C2 = "SELECT COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') THEN 1 END) AS 'Europa-Europa', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') THEN 1 END) AS 'Europa-Asia', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Europe%') THEN 1 END) AS 'Asia-Europa', COUNT(CASE WHEN departure_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') AND arrival_airport IN (SELECT airport_code FROM airports_data WHERE timezone LIKE '%Asia%') THEN 1 END) AS 'Asia-Asia', COUNT(arrival_airport) AS 'Total de vuelos' FROM flights WHERE status = 'Arrived';"

Pregunta_D1 = """
SELECT
    city AS Ciudad,
    COUNT(flight_no) AS num_flights
FROM
    (SELECT
    flights.flight_no,
    flights.arrival_airport,
    flights.aircraft_code,
    airports_data.city
FROM
    flights
INNER JOIN
    airports_data
ON
    flights.arrival_airport = airports_data.airport_code
WHERE
    flights.aircraft_code = '763') 
GROUP BY
    city
ORDER BY
    num_flights DESC;"""
    
    

PreguntaD2= """ SELECT
    arr_city AS asian_city,
    COUNT(flight_no) AS num_flights
FROM
    (SELECT
    flights.flight_no,
    flights.departure_airport,
    flights.arrival_airport,
    dep_airports.city AS dep_city,
    arr_airports.city AS arr_city,
    dep_airports.timezone AS dep_timezone,
    arr_airports.timezone AS arr_timezone
FROM
    flights
INNER JOIN
    airports_data AS dep_airports
ON
    flights.departure_airport = dep_airports.airport_code
INNER JOIN
    airports_data AS arr_airports
ON
    flights.arrival_airport = arr_airports.airport_code
WHERE
    dep_airports.timezone LIKE 'Europe/%'
AND
    arr_airports.timezone LIKE 'Asia/%')
GROUP BY
    arr_city
ORDER BY
    num_flights DESC;"""
    




    


E1 = "SELECT aircraft_code AS 'Avión', count (status) AS 'Frecuencia_de_vuelos_realizados' FROM flights WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','733','CN1') GROUP BY aircraft_code ORDER BY count (status) DESC;"

E2 = "SELECT  flights.aircraft_code AS Avion, ticket_flights.fare_conditions AS Condiciones_de_vuelo, SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS TICKETS_ECONOMY, SUM(CASE WHEN ticket_flights.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS TICKETS_COMFROT, SUM(CASE WHEN ticket_flights.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS TICKETS_BUSINESS, count (ticket_flights.fare_conditions) AS TOTAL_TICKETS FROM flights INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','733','CN1') GROUP by flights.aircraft_code ORDER BY TICKETS_ECONOMY DESC;"

E2_1 =  "SELECT aircraft_code AS 'Avión', count (status) AS 'Frecuencia_de_vuelos_realizados' FROM flights WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','SU9','CN1') AND arrival_airport IN ('DME') GROUP BY aircraft_code ORDER BY count (status) DESC;"

E2_2 = "SELECT  flights.aircraft_code AS Avion, SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS TICKETS_ECONOMY, SUM(CASE WHEN ticket_flights.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS TICKETS_COMFROT, SUM(CASE WHEN ticket_flights.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS TICKETS_BUSINESS, count (ticket_flights.fare_conditions) AS TOTAL_TICKETS FROM flights INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','SU9','CN1') AND flights.arrival_airport IN ('DME') GROUP by flights.aircraft_code ORDER BY TICKETS_ECONOMY DESC;"


modelo = """SELECT 
    ad.aircraft_code,
    f.vuelos_vendidos,
    ad.range,
    tf.avg_amount,
    tr.cantidad_de_reservas
FROM 
    aircrafts_data ad
INNER JOIN 
    (SELECT 
         aircraft_code, 
         COUNT(*) AS vuelos_vendidos
     FROM 
         flights
     GROUP BY 
         aircraft_code) f ON ad.aircraft_code = f.aircraft_code
INNER JOIN 
    (SELECT 
         flights.aircraft_code,
         ROUND(AVG(ticket_flights.amount), 2) AS avg_amount
     FROM flights
     INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
     WHERE ticket_flights.fare_conditions = 'Economy'
     GROUP BY flights.aircraft_code) tf ON ad.aircraft_code = tf.aircraft_code
INNER JOIN 
    (SELECT 
         flights.aircraft_code,
         COUNT(ticket_flights.flight_id) AS cantidad_de_reservas
     FROM flights
     INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
     GROUP BY flights.aircraft_code) tr ON ad.aircraft_code = tr.aircraft_code
ORDER BY 
    tf.avg_amount ASC;"""