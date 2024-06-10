DROP VIEW IF EXISTS Flight_Price_Info;

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
    flights.aircraft_code IN ('773', '763', 'SU9');


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
    arrival_airport, fare_conditions;