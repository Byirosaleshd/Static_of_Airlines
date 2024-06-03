-- Eliminar la vista si ya existe para evitar conflictos
DROP VIEW IF EXISTS Flights_Airports;

-- Crear una vista que combina información de vuelos y aeropuertos, filtrando por aviones del modelo 763
CREATE VIEW Flights_Airports AS
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
    flights.aircraft_code = '763';

-- Consultar las ciudades que reciben vuelos con aviones del modelo 763
SELECT
    city,
    COUNT(flight_no) AS num_flights
FROM
    Flights_Airports
GROUP BY
    city
ORDER BY
    num_flights DESC;