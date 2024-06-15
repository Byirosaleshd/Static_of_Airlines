#Descarga los paquetes necesarios por si alguien no los tiene
pip install pandas
pip install sqlite3 
pip install numpy
pip install seaborn

#Llamamos las librerias
import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt #Graficos
import seaborn as sns #Graficos
import sqlite3 as sql
import numpy as np # Algebra lineal
import Functions as ft
import datetime as dt
from pandas import json_normalize
import json

# Conectar a la base de datos SQLite
conn = sql.connect('../.data/travel.sqlite') 

# Título de la aplicación
st.title("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")

# Just add it after st.sidebar:
a = st.sidebar.radio('Choose:',[1,2])

st.write("""Formulación del Problema 
a	¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo? 
b	¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?
c	Dentro de los modelos de aviones con códigos: 773, 763 y SU9. ¿De cuánto ha sido la variabilidad de precios según el destino y la clase de vuelo?
d	Si los aviones realizan vuelos entre los continentes de Asia y Europa:
1	¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?
2	Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?
E.	Entre los modelos de aviones con los códigos: CR2, 733 y CN1 se desea conocer lo siguiente: 
1	El promedio y la variabilidad de los vuelos realizados.
2   ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?"
""")


st.write('# ¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?')

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


Df_PreguntaA = ft.read_abilities(Pregunta_A,conn)
ft.caracteristicas_modelo(Df_PreguntaA, 'scheduled_departure', 'scheduled_arrival','model')


# Mostrar el DataFrame
#st.write("Datos de la base de datos:")
#st.write(conn.head(5))

# Mostrar estadísticas básicas
#st.write("Estadísticas descriptivas:")
#st.write(iris.describe())


sillas = "SELECT a.aircraft_code AS 'CodigodeAvion', SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) AS 'Economy', SUM(CASE WHEN s.fare_conditions = 'Business' THEN 1 ELSE 0 END) AS 'Business', SUM(CASE WHEN s.fare_conditions = 'Comfort' THEN 1 ELSE 0 END) AS 'Comfort' FROM aircrafts_data a LEFT JOIN seats s ON a.aircraft_code = s.aircraft_code GROUP BY a.aircraft_code ORDER BY SUM(CASE WHEN s.fare_conditions = 'Economy' THEN 1 ELSE 0 END) DESC;"

df_sillas = pd.read_sql_query(sql = sillas, con = conn)
st.write(df_sillas)

#definir variables

labels = df_sillas.CodigodeAvion
Economy = df_sillas.Economy
Business = df_sillas.Business
Comfort = df_sillas.Comfort

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
barra1 = ax.bar(x-0.30, Economy, width, label='Economy', color='#87CEFA')
barra2 = ax.bar(x, Business, width, label='Business', color='#4169E1')
barra3 = ax.bar(x+0.30, Comfort, width, label='Comfort', color='#1E90FF')

ax.set_ylabel('Asientos Vendidos')
ax.set_xlabel('Código de Avion')
ax.set_title('ASIENTOS VENDIDOS POR AVION')
ax.set_xticks(x, labels)

ax.legend()

ax.bar_label(barra1, padding=1)
ax.bar_label(barra2, padding=1)
ax.bar_label(barra3, padding=1)

ax.set_ylim(0,350)
fig.tight_layout()

plt.show()

st.pyplot(fig)




st.write("Dentro de los modelos de aviones con códigos: 773, 763 y SU9. ¿De cuánto ha sido la variabilidad de precios según el destino y la clase de vuelo?")

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

    
    
Df_PreguntaC1 = ft.read_abilities(PreguntaC2,conn)

Df_PreguntaC1

st.write("""Si los aviones realizan vuelos entre los continentes de Asia y Europa:
1	¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?
2	Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?""")

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


Df_Pregunta_D1 = ft.read_abilities(Pregunta_D1,conn)

Df_Pregunta_D1




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

Df_PreguntaD2 = ft.read_abilities(PreguntaD2,conn)

Df_PreguntaD2



Pregunta_E2 = '''SELECT  aircraft_code AS 'Codigo de Avion', status AS Estado , count(fare_conditions) AS Frecuencia , fare_conditions AS 'Tipo de Ticket'
FROM flights 
INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
WHERE status in ('Arrived','On Time') AND aircraft_code IN ('CR2','733','CN1') AND fare_conditions IN ('Business')
;'''

Df_PreguntaE2 = ft.read_abilities(Pregunta_E2,conn)
st.write(Df_PreguntaE2)
print(Df_PreguntaE2)






















# Seleccionar una característica para el gráfico de barras
# feature = st.selectbox("Selecciona una característica para el gráfico de barras", iris.columns[:-1])

# Gráfico de barras
# st.write(f"Gráfico de barras de {feature}:")
# st.area_chart(iris[feature])

# Filtro por tipo de flor
# species       = st.multiselect("Selecciona especies de Iris", iris['species'].unique(), iris['species'].unique())
# filtered_iris = iris[iris['species'].isin(species)]

# st.write(f"Datos filtrados por especies {species}:")
# st.write(filtered_iris)

# Gráfico de dispersión
# st.write("Gráfico de dispersión (Largo de tallo vs Ancho de tallo):")
# fig, ax = plt.subplots()
# sns.scatterplot(data=filtered_iris, x='sepal_length', y='sepal_width', hue='species', ax=ax)
# st.pyplot(fig)

# Gráfico de pares (pairplot)
# st.write("Gráfico de pares de las características Iris:")
# fig = sns.pairplot(filtered_iris, hue='species')
# st.pyplot(fig)

# st.set_page_config(page_title="Statics_of_airlines", page_icon="🤖", layout="wide")

#with st.container():
#    st.subheader("Hola, :wave:")

conn.close()