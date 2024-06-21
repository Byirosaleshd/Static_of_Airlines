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
import Sql as s    
from PIL import Image



# Conectar a la base de datos SQLite
conn = sql.connect('../.data/travel.sqlite') 


# Título de la aplicación
st.title("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")

st.write("#### ¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?")

Pregunta_A = s.Pregunta_A
Df_PreguntaA = ft.read_abilities(Pregunta_A,conn)
ft.caracteristicas_modelo(Df_PreguntaA, 'scheduled_departure', 'scheduled_arrival','model')
st.line_chart(Df_PreguntaA, x="scheduled_departure", y="model")

st.write("#### ¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?")

#ft.imprimir_tabla('sillas',conn,'df_sillas','sillas')

sillas = s.sillas
df_sillas = ft.read_abilities(sillas,conn)
st.write(df_sillas)
ft.Grafico_multibarras(df_sillas,'Economy','Business','Comfort',"Economy","Business","Comfort","Asientos Vendidos","Código de Avion","ASIENTOS VENDIDOS POR AVION")


st.write("#### Dentro de los modelos de aviones con códigos: 773, 763 y SU9. ¿De cuánto ha sido la variabilidad de precios según el destino y la clase de vuelo?")
PreguntaC = s.PreguntaC   
Df_PreguntaC = ft.read_abilities(PreguntaC,conn)
st.write(Df_PreguntaC)


st.write("#### Si los aviones realizan vuelos entre los continentes de Asia y Europa: ¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?")
Pregunta_D1 = s.Pregunta_D1
Df_Pregunta_D1 = ft.read_abilities(Pregunta_D1,conn)
Df_Pregunta_D1
st.bar_chart(Df_Pregunta_D1, x="city", y="num_flights")


st.write("#### Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?")
PreguntaD2 = s.PreguntaD2
Df_PreguntaD2 = ft.read_abilities(PreguntaD2,conn)
Df_PreguntaD2["asian_city"] = Df_PreguntaD2["asian_city"].apply(json.loads)
Df_PreguntaD2[["city_en", "city_ru"]] = Df_PreguntaD2["asian_city"].apply(lambda x: pd.Series([x["en"], x["ru"]]))
Df_PreguntaD2 = Df_PreguntaD2.drop("asian_city", axis=1)
Df_PreguntaD2 = Df_PreguntaD2[["city_en","city_ru","num_flights"]]
Df_PreguntaD2["Numero de vuelos"] = Df_PreguntaD2["num_flights"] 
Df_PreguntaD2 = Df_PreguntaD2.drop("num_flights", axis=1)
Df_PreguntaD2["Ciudad en ingles"] = Df_PreguntaD2["city_en"]
Df_PreguntaD2["Ciudad en ruso"] = Df_PreguntaD2["city_ru"]
Df_PreguntaD2 = Df_PreguntaD2.drop("city_en", axis=1)
Df_PreguntaD2 = Df_PreguntaD2.drop("city_ru", axis=1)
Df_PreguntaD2 = Df_PreguntaD2[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
Df_PreguntaD2 =  Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)
st.write(Df_PreguntaD2)
st.bar_chart(Df_PreguntaD2, x="Ciudad en ingles", y="Numero de vuelos", color="#FF0000")


#colunas=['aircraft_code','flight_id','flight_no','scheduled_departure','scheduled_arrival','departure_airport','arrival_airport','status','model_en','actual_departure','actual_arrival']
#new_voos_list = pd.merge (voos,aeronaves, on='aircraft_code', how='inner')[colunas]
#new_voos_list



st.write("#### Entre los modelos de aviones con los códigos: CR2, 733 y CN1 se desea conocer lo siguiente: El promedio y la variabilidad de los vuelos realizados.")


E1 = "SELECT aircraft_code AS 'Avión', count (status) AS 'Frecuencia_de_vuelos_realizados' FROM flights WHERE status IN ('Arrived') AND aircraft_code IN ('CR2','733','CN1') GROUP BY aircraft_code ORDER BY count (status) DESC;"
Pregunta_E1 = s.E1
Df_PreguntaE1 = ft.read_abilities(Pregunta_E1, conn)
st.write(Df_PreguntaE1)
ft.grafico_pie(Df_PreguntaE1)


#st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?")
#Pregunta_E2 = s.Pregunta_E2
#Df_PreguntaE2 = ft.read_abilities(Pregunta_E2,conn)
#st.write(Df_PreguntaE2)
#print(Df_PreguntaE2)


st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?")

Pregunta_E2 = s.E2
Df_PreguntaE2 = ft.read_abilities(Pregunta_E2, conn)
st.write(Df_PreguntaE2)
ft.grafico_barras_superpuestas(Df_PreguntaE2)
















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