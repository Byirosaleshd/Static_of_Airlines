Pregunta_A = """SELECT flights.flight_id,
flights.flight_no,
flights.scheduled_departure,
flights.scheduled_arrival,
flights.departure_airport,
flights.arrival_airport,
flights.status,
flights.aircraft_code,
aircrafts_data.model,
json_extract(aircrafts_data.model, '$.en') AS 'Nombre en ingles',
json_extract(aircrafts_data.model, '$.ru') AS 'Nombre en ruso'
FROM flights
INNER JOIN aircrafts_data 
ON aircrafts_data.aircraft_code = flights.aircraft_code
WHERE
    flights.status IN ('Arrived', 'On Time');"""


Pa ="""SELECT Nombre, Mes, Count(Mes) AS cantidad FROM PreguntaA
GROUP BY Nombre,Mes;
"""


PreguntaB = "SELECT a.aircraft_code AS 'CodigodeAvion', SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS 'Economy', SUM(CASE WHEN s.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS 'Business', SUM(CASE WHEN s.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS 'Comfort' FROM aircrafts_data a LEFT JOIN seats s ON a.aircraft_code = s.aircraft_code GROUP BY a.aircraft_code ORDER BY SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) DESC;"
    


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

