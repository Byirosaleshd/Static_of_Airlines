import streamlit as st
import pandas    as pd
import seaborn   as sns
import matplotlib.pyplot as plt
import sqlite3 as sql
import Functions as ft

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
# Cargar la base de datos
conn = sql.connect('../.data/travel.sqlite') 

Pregunta_A = """SELECT flights.flight_id,
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
ON aircrafts_data.aircraft_code = flights.aircraft_code;"""

Df_vista1 = ft.read_abilities(Pregunta_A,conn)

Df_vista2 = Df_vista1[['scheduled_departure','scheduled_arrival','departure_airport','arrival_airport','status','aircraft_code','model']]
Df_vista2['scheduled_departure'] = pd.to_datetime(Df_vista2['scheduled_departure']).dt.time
Df_vista2['scheduled_arrival'] = pd.to_datetime(Df_vista2['scheduled_arrival']).dt.time
Df_vista2
# Agrupamos por modelo y contamos la cantidad de vuelos
modelo_vuelos = Df_vista2.groupby('model')['scheduled_departure'].count()

# Ordena en orden descendente
modelo_vuelos = modelo_vuelos.sort_values(ascending=False)

# Obtiene el modelo con la mayor cantidad de vuelos
modelo_mas_frecuente = modelo_vuelos.index[0]

print(f"El modelo de avión que realiza la mayor cantidad de vuelos es: {modelo_mas_frecuente}")
# Extraer horas y minutos para transformar todo en horas
Df_vista2['hora de salida'] = Df_vista2['scheduled_departure'].apply(lambda x: x.hour + x.minute / 60)
Df_vista2['hora de llegada'] = Df_vista2['scheduled_arrival'].apply(lambda x: x.hour + x.minute / 60)
# Calcula la duración de cada vuelo
Df_vista2['duracion_vuelo'] = Df_vista2['hora de salida'] - Df_vista2['hora de llegada'] 

# Agrupa por modelo y calcula el tiempo promedio de vuelo
modelo_tiempo_promedio = Df_vista2.groupby('model')['duracion_vuelo'].mean()

# Ordena en orden ascendente
modelo_tiempo_promedio = modelo_tiempo_promedio.sort_values(ascending=True)

# Obtiene el modelo con el menor tiempo promedio de vuelo
modelo_menor_tiempo = modelo_tiempo_promedio.index[0]

st.write(modelo_menor_tiempo)
st.write(f"El modelo de avión que realiza vuelos en el menor tiempo promedio es: {modelo_menor_tiempo}")

# Mostrar el DataFrame
#st.write("Datos de la base de datos:")
#st.write(conn.head(5))

# Mostrar estadísticas básicas
st.write("Estadísticas descriptivas:")
st.write(iris.describe())

# Seleccionar una característica para el gráfico de barras
feature = st.selectbox("Selecciona una característica para el gráfico de barras", iris.columns[:-1])

# Gráfico de barras
st.write(f"Gráfico de barras de {feature}:")
st.area_chart(iris[feature])

# Filtro por tipo de flor
species       = st.multiselect("Selecciona especies de Iris", iris['species'].unique(), iris['species'].unique())
filtered_iris = iris[iris['species'].isin(species)]

st.write(f"Datos filtrados por especies {species}:")
st.write(filtered_iris)

# Gráfico de dispersión
st.write("Gráfico de dispersión (Largo de tallo vs Ancho de tallo):")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_iris, x='sepal_length', y='sepal_width', hue='species', ax=ax)
st.pyplot(fig)

# Gráfico de pares (pairplot)
st.write("Gráfico de pares de las características Iris:")
fig = sns.pairplot(filtered_iris, hue='species')
st.pyplot(fig)

st.set_page_config(page_title="Statics_of_airlines", page_icon="🤖", layout="wide")

with st.container():
    st.subheader("Hola, :wave:")

