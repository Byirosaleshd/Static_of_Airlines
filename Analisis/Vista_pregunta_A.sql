CREATE VIEW Pregunta_A AS 
SELECT flights.flight_id,
	   flights.flight_no,
	   flights.scheduled_departure,
	   flights.scheduled_arrival,
	   flights.departure_airport,
	   flights.arrival_airport,
	   flights.status,
	   flights.aircraft_code,
	   aircrafts_data.model
FROM flights
INNER JOIN aircrafts_data 
ON aircrafts_data.aircraft_code = flights.aircraft_code;

SELECT * FROM Pregunta_A