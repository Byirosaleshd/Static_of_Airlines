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