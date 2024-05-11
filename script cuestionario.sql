--1. Indicar los aeropuertos de llegada con mayor frecuencia.

SELECT count(arrival_airport) as 'frecuencia de llegada', arrival_airport as 'aeropuerto', status
FROM flights 
WHERE status='Arrived'
 GROUP BY arrival_airport
 ORDER BY count(arrival_airport) DESC
 LIMIT 5;
