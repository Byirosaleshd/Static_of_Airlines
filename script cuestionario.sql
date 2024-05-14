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

--5.Indique cuales son los 10 vuelos con mayor cantidad de pasajeros y cuál fue la ruta de estos (aeropuerto de salida y aeropuerto de llegada).

--SELECT tickets.ticket_no,tickets.book_ref,tickets.passenger_id, ticket_flights.ticket_no,ticket_flights.flight_id,ticket_flights.fare_conditions,ticket_flights.amount, flights.*
--FROM tickets
--INNER JOIN ticket_flights 
--ON tickets.ticket_no = ticket_flights.ticket_no
--INNER JOIN flights ON ticket_flights.flight_id = flights.flight_id
--GROUP BY fare_conditions;


