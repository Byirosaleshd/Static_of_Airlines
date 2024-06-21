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
conn = sql.connect('travel.sqlite') 


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
Df_PreguntaC





st.write("#### Contexto de la pregunta para posterior resolucion: dentro de los modelos previstos se necesita la variabilidades de los precios segun el destino y la clase de vuelo de cada clase de avion")












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

fig, ax = plt.subplots()
aviones = Df_PreguntaE1.Avión
frecuencia = ['4674', '4570', '646']
explotar = (0.1, 0.05, 0.12)
colors = ['#3A95B1', '#7BBFC9', '#BCE4D8']

def autopct_fun(frecuencia):
    gen = iter(frecuencia)
    return lambda pct: f"{pct:1.0f}% ({next(gen)})"

plt.pie(frecuencia, labels=aviones, explode=explotar, colors=colors,
        autopct= autopct_fun(frecuencia),
        shadow=True, startangle=20,
        pctdistance=0.6, radius=0.7, labeldistance=1.15)

plt.show()
st.pyplot(fig)




#st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?")
#Pregunta_E2 = s.Pregunta_E2
#Df_PreguntaE2 = ft.read_abilities(Pregunta_E2,conn)
#st.write(Df_PreguntaE2)
#print(Df_PreguntaE2)


st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?")

Pregunta_E2 = s.E2
Df_PreguntaE2 = ft.read_abilities(Pregunta_E2, conn)
st.write(Df_PreguntaE2)

fig, ax = plt.subplots()
x = Df_PreguntaE2.Avion

clase_economy = Df_PreguntaE2.TICKETS_ECONOMY
clase_comfort = Df_PreguntaE2.TICKETS_COMFROT
clase_business = Df_PreguntaE2.TICKETS_BUSINESS

plt.bar(x, clase_economy, 0.4, label = "Economy", color = "#7BBFC9")
plt.bar(x, clase_comfort, 0.4, label = "Comfort", color = "#BCE4D8")
plt.bar(x, clase_business, 0.4, label = "Business", color = "#3A95B1")

# Añadir etiquetas a las barras
for i, v in enumerate(clase_economy):
    plt.text(i, v, str(v), ha='center', va='bottom')
# Añadir etiquetas a las barras
for i, v in enumerate(clase_business):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.xlabel("Aviones")
plt.ylabel("asientos vendidos")


plt.legend()
plt.show()
st.pyplot(fig)
















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