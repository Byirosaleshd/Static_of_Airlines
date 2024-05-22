# 4. Se requiere calcular la distancia en KM de los distintos aeropuertos que existen en la base de datos y con esta nueva variable mostrar las estadísticas básicas con respecto a la distancia de los vuelos.

import pandas
import sqlite3
from math import sqrt



print("Ingresa los valores del punto 1")
xl = float(input())
y1 = float(input())
print("Ingresa los valores del punto 2")
x2 = float(input())
y2 = float(input())

distancia = sqrt((x2-x1)**2 + (y2-y1)**2)
print("Las distancia entre los 2 puntos es: ", distancia)


def calcular_distancia(velocidad, tiempo):
    distancia = velocidad = tiempo
    return distancia

#PEDIR AL USUARIO LA VELOCIDAD EN M/S
velocidad = float(input("Ingrese la velocidad (m/s): "))

#PEDIR AL USUARIO EL TIEMPO EN SEGUNDOS
tiempo = float(input("Ingrese el tiempo (s): "))

#CALCULAR LA DISTANCIA
distancia_recorrida = calcular_distancia(velocidad, tiempo)

#MOSTRAR LA DISTANCIA RECORRIDA
print(f"La distancia recorrida es: {distancia_recorrida} metros.")


import math
def calcular_distancia(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#Solicitamos las cordenadas de los puntos al usuario
xl = float(input("Introduce x1: "))
y1 = float(input("Introduce y1"))
x2 = float(input("Introduce x2: "))
y2 = float(input("Introduce y2: "))

distancia = calcular_distancia(x1, y1, x2, y2)

print(f"""La distancia entre los puntos ({x1}, {y1}) y ({x2}, {y2}) es: {distancia}""")



#ALTER TABLE airports_data
# ADD Distancia_KM;
#UPDATE airports_data
#SET Distancia_KM = (
#    --CASE WHEN strftime('%m%d', CURRENT_DATE) >= strftime('%m%d', Fecha_Nacimiento)
#    --    THEN strftime('%Y', CURRENT_DATE) - strftime('%Y', Fecha_Nacimiento)
#    --    ELSE strftime('%Y', CURRENT_DATE) - strftime('%Y', Fecha_Nacimiento) - 1
#    --END
#	--Distancia = Velocidad * Tiempo
#	Distancia = range * scheduled_arrival
#); 

#SELECT * FROM airports_data;





conn = sqlite3.connect("data/travel.sqlite")

#Consulta de los aeropuertos 
consulta_datos = "SELECT * FROM flights INNER JOIN aircrafts_data ON flights.aircraft_code = aircrafts_data.aircraft_code INNER JOIN airports_data ON flights.arrival_airport = airports_data.airport_code;"
Df_aiports_data   = pd.read_sql_query(sql = consulta_datos, con = conn)
Df_aiports_data