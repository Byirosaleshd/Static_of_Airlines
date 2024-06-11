import streamlit as st
<<<<<<< HEAD
import pandas    as pd
import seaborn   as sns
import matplotlib.pyplot as plt
import sqlite3 as sql

# Título de la aplicación
st.title("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")

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

# Cargar el conjunto de datos Iris
conn = sql.connect('data/travel.sqlite') 

# Mostrar el DataFrame
st.write("Datos de la base de datos:")
st.write(conn.head(5))

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
=======

st.set_page_config(page_title="Statics_of_airlines", page_icon="🤖", layout="wide")

with st.container():
    st.subheader("Hola, :wave:")
>>>>>>> 942bf8fad4a7c930c0dfdb5384353b537cb8b88e
