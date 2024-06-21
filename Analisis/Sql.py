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
    
    


E1 = "SELECT aircraft_code AS 'Avión', count (status) AS 'Frecuencia_de_vuelos_realizados' FROM flights WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','733','CN1') GROUP BY aircraft_code ORDER BY count (status) DESC;"

E2 = "SELECT  flights.aircraft_code AS Avion, ticket_flights.fare_conditions AS Condiciones_de_vuelo, SUM(CASE WHEN ticket_flights.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS TICKETS_ECONOMY, SUM(CASE WHEN ticket_flights.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS TICKETS_COMFROT, SUM(CASE WHEN ticket_flights.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS TICKETS_BUSINESS, count (ticket_flights.fare_conditions) AS TOTAL_TICKETS FROM flights INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','733','CN1') GROUP by flights.aircraft_code ORDER BY TICKETS_ECONOMY DESC;"

    
    
    
    
    
    
    
    
    
    
    
    
    
    
Pregunta_E2 = '''SELECT  aircraft_code AS 'Codigo de Avion', status AS Estado , count(fare_conditions) AS Frecuencia , fare_conditions AS 'Tipo de Ticket'
FROM flights 
INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
WHERE status in ('Arrived','On Time') AND aircraft_code IN ('CR2','733','CN1') AND fare_conditions IN ('Business');'''
    
    
    
    
    
        