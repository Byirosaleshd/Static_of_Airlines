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
ON aircrafts_data.aircraft_code = flights.aircraft_code;"""

sillas = "SELECT a.aircraft_code AS 'CodigodeAvion', SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS 'Economy', SUM(CASE WHEN s.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS 'Business', SUM(CASE WHEN s.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS 'Comfort' FROM aircrafts_data a LEFT JOIN seats s ON a.aircraft_code = s.aircraft_code GROUP BY a.aircraft_code ORDER BY SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) DESC;"


PreguntaC = """
CREATE VIEW Flight_Price_Info AS
SELECT
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
    flights.aircraft_code IN ('773', '763', 'SU9');"""
    
    

PreguntaC2 = """
SELECT
    arrival_airport,
    fare_conditions,
    COUNT(amount) AS num_flights,
    AVG(amount) AS avg_price,
    MIN(amount) AS min_price,
    MAX(amount) AS max_price
FROM
    Flight_Price_Info
GROUP BY
    arrival_airport, fare_conditions
ORDER BY
    arrival_airport, fare_conditions;"""
    
    
    
    
PreguntaD1 = """CREATE VIEW Flights_Airports AS
SELECT
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
    flights.aircraft_code = '763';"""

Pregunta_D1 = """
SELECT
    city,
    COUNT(flight_no) AS num_flights
FROM
    Flights_Airports
GROUP BY
    city
ORDER BY
    num_flights DESC;"""
    
    
    
    
PreguntaD = """CREATE VIEW European_To_Asian_Flights AS
SELECT
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
    arr_airports.timezone LIKE 'Asia/%';"""

PreguntaD2= """ 
SELECT
    arr_city AS asian_city,
    COUNT(flight_no) AS num_flights
FROM
    European_To_Asian_Flights
GROUP BY
    arr_city
ORDER BY
    num_flights DESC;"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
Pregunta_E2 = '''SELECT  aircraft_code AS 'Codigo de Avion', status AS Estado , count(fare_conditions) AS Frecuencia , fare_conditions AS 'Tipo de Ticket'
FROM flights 
INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
WHERE status in ('Arrived','On Time') AND aircraft_code IN ('CR2','733','CN1') AND fare_conditions IN ('Business');'''
    
    
    
    
    
        