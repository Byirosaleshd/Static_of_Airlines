DROP VIEW IF EXISTS European_To_Asian_Flights;

CREATE VIEW European_To_Asian_Flights AS
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
    arr_airports.timezone LIKE 'Asia/%';


SELECT
    arr_city AS asian_city,
    COUNT(flight_no) AS num_flights
FROM
    European_To_Asian_Flights
GROUP BY
    arr_city
ORDER BY
    num_flights DESC;