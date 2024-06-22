#Llamamos las librerias
import streamlit as st #App
import pandas as pd #Statics
import matplotlib.pyplot as plt #Graficos
import seaborn as sns #Graficos
import plotly.express as px #Graficos
import plotly.graph_objs as go #Graficos
import sqlite3 as sql #Database
import numpy as np # Algebra lineal
#from sklearn.linear_model import LinearRegression #Regression
#from sklearn.model_selection import train_test_split #Regression
#from sklearn.metrics import r2_score #Regression
import Functions as ft #Functions for this program
import datetime as dt #Control for Time
from pandas import json_normalize #Json utilities
import json #Json utilites
import Sql as s #Sql querys
from PIL import Image #Images
from deep_translator import GoogleTranslator #Traducir


# Conectar a la base de datos SQLite
conn = sql.connect('Data/travel.sqlite')
#translator = GoogleTranslator(source="en", target="es")


logo = Image.open(r'Images/avion.png')
st.sidebar.image(logo, width=100)
st.sidebar.header("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")
st.sidebar.write(" ")
st.sidebar.write(" ")
option = st.sidebar.selectbox(
    'Selecciona una pagina para navegar por la app',
    ('Presentacion','Pregunta A', 'Pregunta B',"Pregunta C","Pregunta D","Pregunta E","Modelo de regresion"))
if option == 'Presentacion':
    st.write(" ")
    st.write(" ")
#    stats = Image.open(r'imagenes/STATS.jpg')
    st.sidebar.header('Recursos utilizados')
    st.sidebar.markdown('''
- [Database de Aerolineas](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset/data) De donde salio la informacion
''')
    col1, col2, col3 = st.columns((1,4,1))
#    col2.image(stats, width=300)
    st.write(" ")
    st.write(" ")
    st.markdown("# Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1, col2, col3 = st.columns(3)
    col1.expander("Presentado por").write("Ignacio Rosales")
    col3.expander("Git-hub").write("[Repositorio](https://github.com/Byirosaleshd/Static_of_Airlines)")
    col2.expander("Contacto").write("""
#    [Perfil Linkedln]()
#    [CURRICULUM VITAE]()""")
    

   
    
elif option == 'Pregunta A':
    st.header("¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?")
    st.markdown("Puedes seleccionar las estadisticas que desees:")
    Pregunta_A = s.Pregunta_A
    Df_PreguntaA = ft.read_abilities(Pregunta_A,conn)
    modelo_menor_tiempo = ft.modelos_menor(Df_PreguntaA,'scheduled_arrival','scheduled_departure')
    modelo_mas_frecuente = ft.modelos_mas(Df_PreguntaA,'scheduled_arrival','scheduled_departure')
    ft.caracteristicas_modelo(Df_PreguntaA,'scheduled_arrival','scheduled_departure','model')
    columnas = list(Df_PreguntaA.columns)
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    columnas_seleccionadas = st.sidebar.multiselect('Selecciona las columnas a mostrar', columnas, default=["hora de llegada","hora de salida","departure_airport","arrival_airport","status","aircraft_code","Nombre en ingles","Nombre en ruso","duracion_vuelo"])
    data_filt = Df_PreguntaA[columnas_seleccionadas]
    st.dataframe(data_filt,width=550, height=400)
    expandir = st.expander("Ver interpretacion")
    expandir.write("goku")
    expandir.write(f"El modelo de avión que realiza vuelos en el menor tiempo promedio es: {modelo_menor_tiempo}")
    expandir.write(f"El modelo de avión que realiza la mayor cantidad de vuelos es: {modelo_mas_frecuente}")
    
    
    
elif option == 'Pregunta B':
    st.header("¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    PreguntaB= s.PreguntaB
    df_PreguntaB = ft.imprimir_df("df_PreguntaB",PreguntaB,conn)
    ft.Grafico_multibarras(df_PreguntaB,'Economy','Business','Comfort',"Economy","Business","Comfort","Asientos Vendidos","Código de Avion","ASIENTOS VENDIDOS POR AVION")
    columnas = list(df_PreguntaB.columns)


elif option == 'Pregunta C':
    st.header("Dentro de los modelos de aviones con códigos: 773, 763 y SU9. ¿De cuánto ha sido la variabilidad de precios según el destino y la clase de vuelo:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    PreguntaC = s.PreguntaC   
    Df_PreguntaC = ft.imprimir_df("Df_PreguntaC",PreguntaC,conn)
    columnas = list(Df_PreguntaC.columns)


elif option == 'Pregunta D':
    st.header("Si los aviones realizan vuelos entre los continentes de Asia y Europa: ¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    Pregunta_D1 = s.Pregunta_D1
    Df_Pregunta_D1 = ft.read_abilities(Pregunta_D1,conn)
    ft.limpiar_json(Df_Pregunta_D1,"Ciudad","Ciudad en ingles","Ciudad en ruso")
    Df_Pregunta_D1["Numero de vuelos"] = Df_Pregunta_D1["num_flights"] 
    Df_Pregunta_D1 = Df_Pregunta_D1.drop("num_flights", axis=1)
    Df_Pregunta_D1 = Df_Pregunta_D1[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
    Df_Pregunta_D1 =  Df_Pregunta_D1.sort_values(by="Numero de vuelos", ascending=False)
    st.write(Df_Pregunta_D1)
    st.bar_chart(Df_Pregunta_D1, x="Ciudad en ingles", y="Numero de vuelos")
    columnas = list(Df_Pregunta_D1.columns)
    
    st.write("#### Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?")
    PreguntaD2 = s.PreguntaD2
    Df_PreguntaD2 = ft.read_abilities(PreguntaD2,conn)
    ft.limpiar_json(Df_PreguntaD2,"asian_city","Ciudad en ingles","Ciudad en ruso")
    Df_PreguntaD2["Numero de vuelos"] = Df_PreguntaD2["num_flights"] 
    Df_PreguntaD2 = Df_PreguntaD2.drop("num_flights", axis=1)
    Df_PreguntaD2 = Df_PreguntaD2[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
    Df_PreguntaD2 =  Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)
    Df_PreguntaD2["Ciudad"] = Df_PreguntaD2["Ciudad en ingles"].apply(translator.translate)
    st.write(Df_PreguntaD2)
    st.bar_chart(Df_PreguntaD2, x="Ciudad en ingles", y="Numero de vuelos", color="#FF0000")
    columnas = list(Df_PreguntaD2.columns)


elif option == 'Pregunta E':
    st.header("Entre los modelos de aviones con los códigos: CR2, 733 y CN1 se desea conocer lo siguiente: El promedio y la variabilidad de los vuelos realizados:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    Pregunta_E1 = s.E1
    Df_PreguntaE1 = ft.imprimir_df("Df_PreguntaE1",Pregunta_E1,conn)
    ft.grafico_pie(Df_PreguntaE1)
    columnas = list(Df_PreguntaE1.columns)

    st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Business?")
    Pregunta_E2 = s.E2
    Df_PreguntaE2 = ft.imprimir_df("Df_PreguntaE2",Pregunta_E2,conn)
    ft.grafico_barras_superpuestas(Df_PreguntaE2)
    columnas = list(Df_PreguntaE2.columns)








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