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
conn = sql.connect('travel.sqlite')
translator = GoogleTranslator(source="en", target="es")


logo = Image.open(r'Images/avion.png')
st.sidebar.image(logo, width=100)
st.sidebar.header("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos")
st.sidebar.write(" ")
st.sidebar.write(" ")
option = st.sidebar.selectbox(
    'Selecciona una pagina para navegar por la app',
    ('Presentacion', 'Planteamiento', 'Pregunta A',  'Pregunta A2', 'Pregunta B',"Pregunta C","Pregunta D","Pregunta E","Modelo de regresion"))
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
    col1.expander("Presentado por").write("- Ignacio Rosales\n- Lucia Bugallo\n- Daniel Sierra\n- María Alcalá\n- Daniel Aristiguieta")
    col3.expander("Git-hub").write("[Repositorio](https://github.com/Byirosaleshd/Static_of_Airlines)")
    col2.expander("Contacto").write("""
#    [Perfil Linkedln]()
#    [CURRICULUM VITAE]()""")
    
elif option == 'Planteamiento':
    st.header("Planteamiento")
    st.markdown("Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos de los continentes de Asia y Europa durante el año 2017")
    st.markdown("a) ¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo? ")
    st.markdown("b) ¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?")
    st.markdown("c) En la base de datos contamos con 4 rutas posibles realizadas por los aviones registrados, se quiere saber:")
    st.markdown("   - ¿Cuál es la ruta con mayor frecuencia realizada por los aviones, que avión realiza mayor cantidad de vuelos para las rutas Europa-Europa, Europa-Asia, Asia-Asia y Asia-Europa?")
    st.markdown("   - ¿Cuál es la ruta con mayores vuelos, sin importar el avión?")
    st.markdown("d) Si los aviones realizan vuelos entre los continentes de Asia y Europa:")
    st.markdown("   - ¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?")
    st.markdown("   - Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?")
    st.markdown("e) Entre los modelos de aviones con los códigos: CR2, 733 y CN1 se desea conocer lo siguiente:")
    st.markdown("   - El promedio y la variabilidad de los vuelos realizados.")
    st.markdown("   - ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Económica?")


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
    
elif option == 'Pregunta A2':
    st.header("¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?")
    PreguntaA1= s.PreguntaA1
    df_PreguntaA1 = ft.imprimir_df("df_PreguntaB",PreguntaA1,conn)
    aviones = df_PreguntaA1['CÓDIGO DE AVIÓN']
    vuelos_vendidos_julio = df_PreguntaA1['VUELOS EN 2017-07']
    vuelos_vendidos_agosto = df_PreguntaA1['VUELOS EN 2017-08']
    fig, ax = plt.subplots()
    ax.barh(aviones, vuelos_vendidos_julio, color='#7BBFC9', label='Julio', edgecolor = "black", linewidth = 0.5)
    ax.barh(aviones, vuelos_vendidos_agosto, color='#BCE4D8', label='Agosto', edgecolor = "black", linewidth = 0.5)
    ax.set_xlabel('Vuelos vendidos')
    ax.set_ylabel('Aviones')
    ax.set_title('Vuelos vendidos por avión y mes')
    ax.legend()
    plt.show()
    st.pyplot(fig)
    st.markdown("Al analizar la distribución de las barras, podemos ver que el avión CN1 es el que más vuelos vendió en ambos meses, mientras que el avión 773 vendió menos vuelos en comparación. Y al ser un gráfico de barras apiladas tenemos que la barra de Julio es más larga que la barra de agosto, lo que indica que se vendieron más vuelos en Julio que en agosto; esto puede ser debido a que julio es un mes de alta demanda para viajes debido a las vacaciones de verano en algunos países, lo que podría explicar el aumento en la cantidad de vuelos vendidos.")
    
    PreguntaA2= s.PreguntaA2
    df_PreguntaA2 = ft.imprimir_df("df_PreguntaB",PreguntaA2,conn)
    # Datos
    x = df_PreguntaA2['CODIGO DE AVION']
    y = df_PreguntaA2['ALCANCE DEL AVION']
    # Stem plot
    fig, ax = plt.subplots()
    ax.stem(x, y, linefmt = '--')
    ax.set_xlabel('Avión')
    ax.set_ylabel('Alcance')
    ax.set_title('Alcance por avión')
    plt.show() 
    st.pyplot(fig)
    st.markdown("El avión con un mayor alcance es el 773, en comparación a los demás")


elif option == 'Pregunta B':
    st.header("¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    PreguntaB= s.PreguntaB
    df_PreguntaB = ft.imprimir_df("df_PreguntaB",PreguntaB,conn)
    ft.Grafico_multibarras(df_PreguntaB,'Economy','Business','Comfort',"Economy","Business","Comfort","Asientos Vendidos","Código de Avion","ASIENTOS VENDIDOS POR AVION")
    columnas = list(df_PreguntaB.columns)
    st.markdown("Como podemos apreciar en la gráfica, los asientos más vendidos son los de clase económica, que ocupan más del 50% de los puestos totales de cada aeronave. Si nos guiamos por el avión que ha vendido una mayor cantidad de puestos, podemos ver que vendría siendo la nave cuyo código es “773”, el cual indica que tiene una mayor venta de puestos de clase económica, como también tuvo una mayor venta en las otras dos clases. Siendo así, la aeronave con mayores asientos vendidos.")


elif option == 'Pregunta C':
    st.header("¿Cuál es la ruta con mayor frecuencia realizada por los aviones, que avión realiza mayor cantidad de vuelos para las rutas Europa-Europa, Europa-Asia, Asia-Asia y Asia-Europa?")
    Pregunta_C1 = s.Pregunta_C1   
    Df_Pregunta_C1 = ft.imprimir_df("Df_PreguntaC",Pregunta_C1,conn)
    columnas = list(Df_Pregunta_C1.columns)
    labels = Df_Pregunta_C1['Avion']
    Europa_Europa = Df_Pregunta_C1['Europe_to_Europe']
    Europa_Asia = Df_Pregunta_C1['Europe_to_Asia']
    Asia_Asia = Df_Pregunta_C1['Asia_to_Asia']
    Asia_Europa = Df_Pregunta_C1['Asia_to_Europe']
    # Crear figura y ejes
    fig, ax = plt.subplots()
    # Crear barras acumuladas
    ax.bar(labels, Europa_Europa, 0.5, color = '#3A95B1', edgecolor = "black", linewidth = 0.5, label='Europe-Europe')
    ax.bar(labels, Europa_Asia, 0.5, bottom=Europa_Europa, color = '#7BBFC9', edgecolor = "black", linewidth = 0.5, label='Europe-Asia')
    ax.bar(labels, Asia_Asia, 0.5, bottom=[i+j for i,j in zip(Europa_Europa, Europa_Asia)], color = '#BCE4D8', edgecolor = "black", linewidth = 0.5, label='Asia-Asia')
    ax.bar(labels, Asia_Europa, 0.5, bottom=[i+j+k for i,j,k in zip(Europa_Europa, Europa_Asia, Asia_Asia)], color = '#7CC098', edgecolor = "black", linewidth = 0.5, label='Asia-Europe')
    # Configurar ejes y título
    ax.set_xlabel('Aviones')
    ax.set_ylabel('Cantidad de vuelos')
    ax.set_title('Grafico de barras de vuelos por ruta')
    # Mostrar leyenda
    ax.legend()
    # Mostrar gráfico
    plt.show()
    st.pyplot(fig)
    st.markdown("En la gráfica contamos con 8 aviones, y sus respectivos vuelos categorizados por la ruta que hayan tomado. Podemos apreciar que la ruta con mayores aviones circulando es la de Europa-Europa. Tenemos que 5 de 8 aviones realizan vuelos en las 4 rutas posibles, pero el avión cuyo código es “SU9” realiza mayor cantidad de vuelos para la ruta Europa-Europa con 2212 vuelos. El avión cuyo código es “CR2” realiza mayor cantidad de vuelos para las rutas: Europa-Asia con 685 vuelos y Asia-Europa con 683 vuelos. Y por último el avión cuyo código es “CN1” realiza una mayor cantidad de vuelos para la ruta Asia-Asia con 1976 vuelos.")

    st.header("¿Cuál es la ruta con mayores vuelos, sin importar el avión?")
    Pregunta_C2 = s.Pregunta_C2   
    Df_Pregunta_C2 = ft.imprimir_df("Df_PreguntaC",Pregunta_C2,conn)
    columnas = list(Df_Pregunta_C2.columns)
    Rutas = ['Europa-Europa', 'Europa-Asia', 'Asia-Europa', 'Asia-Asia']
    frecuencia = ['8101', '2283', '2282', '4041']
    explotar = (0.1, 0.05, 0.12, 0.1)
    colors = ['#3A95B1', '#7BBFC9', '#BCE4D8', '#7CC098']
    fig, ax = plt.subplots()
    plt.pie(frecuencia, labels=Rutas, explode=explotar, colors=colors,
        autopct='%1.0f%%',
        shadow=True, startangle=20,
        pctdistance=0.6, radius=0.7, labeldistance=1.15)
    plt.show()
    st.pyplot(fig)
    st.markdown("En la base de datos se cuenta con un total de 16.707 vuelos que llegaron a su destino, en este gráfico de torta podemos apreciar que la ruta con mayor cantidad de vuelos es Europa-Europa con un 48%, duplicando la cantidad de vuelos que cuenta la segunda ruta más frecuentada por los aviones que es Asia-Asia, mientras que las rutas con destinos internacionales tienen el mismo porcentaje.")



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
    st.markdown("Al analizar la gráfica podemos apreciar que la ciudad que recibe una mayor cantidad de vuelos del avión cuyo código es “763” es la ciudad de Moscow con una cantidad altamente representativa frente a las demás ciudades, cuenta con un total de 453 vuelos recibidos por dicho avión ,esto puede ser debido a que es una ciudad que cuenta con mayor turismo en el continente asiático; mientras que como segundas ciudades con mayor cantidad de vuelos, encontramos a las cuidades de Krasnodar y Khabarovsk con un total de 122 vuelos recibidos.")
    
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
    st.markdown("La ciudad que recibe una mayor cantidad de vuelo de parte de las aerolíneas europeas es Perm, ciudad de Rusia que está situada a orillas del río Kama en la parte europea de Rusia, y cuenta con un total de 366 vuelos recibidos.")


elif option == 'Pregunta E':
    st.header("Entre los modelos de aviones con los códigos: CR2, 733 y CN1 se desea conocer lo siguiente: El promedio y la variabilidad de los vuelos realizados:")
    st.markdown("Puedes seleccionar las estadisticas que desees")
    Pregunta_E1 = s.E1
    Df_PreguntaE1 = ft.imprimir_df("Df_PreguntaE1",Pregunta_E1,conn)
    ft.grafico_pie(Df_PreguntaE1)
    columnas = list(Df_PreguntaE1.columns)
    st.markdown("Entre estos tres modelos de aviones tenemos que el 47% de vuelos realizados y que llegaron a su destino pertenece al avión cuyo código es “CN1” con un total de 4674 vuelos, mientras que el CR2 cuenta con casi 100 vuelos menos que el CN1.")

    st.write("#### ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos pertenecientes a la clase Económica?")
    Pregunta_E2 = s.E2
    Df_PreguntaE2 = ft.imprimir_df("Df_PreguntaE2",Pregunta_E2,conn)
    CLASES = ['Economy','Comfort', 'Business']
    AVION_CR2 = [83311, 0, 0]
    AVION_CN1 = [8095, 0, 0]
    AVION_733 = [42988, 0, 4365]
    # Crear la figura y el eje
    fig, ax = plt.subplots()
    # Crear la gráfica
    plt.plot(CLASES, AVION_CR2, label="CR2", marker='o', linestyle='-', color='#3A95B1')
    plt.plot(CLASES, AVION_CN1, label="CN1", marker='o', linestyle='-', color= '#BCE4D8')
    plt.plot(CLASES, AVION_733, label="733", marker='o', linestyle='-', color= '#7CC098')
    # Personalizar la gráfica
    plt.xlabel("Condicion de vuelo")
    plt.ylabel("tickets vendidos")
    plt.title("Tickets vendidos por condicion de vuelo")
    ax.grid(True)  # Agregar líneas de cuadrícula
    ax.legend(loc='upper right')  # Mover la leyenda a la esquina superior derecha
    plt.legend()
    # Mostrar la gráfica
    plt.show()
    st.pyplot(fig)
    st.markdown("Al analizar el gráfico de barras apiladas, contamos con que el avión CR2 tiene la mayor cantidad de asientos vendidos con 83311 asientos en total. El avión 733 cuenta con la segunda mayor cantidad de asientos vendidos, con 47353 asientos en total, mientras que el avión CN1 tiene la menos cantidad de asientos con 8095 asientos vendidos en total. Dentro de cada modelo de avión, podemos decir que la clase económica es el tipo de asiento predominante. En general el gráfico muestra que la clase económica es la más popular por los pasajeros, mientras que en el caso de estas tres aeronaves la clase confort es la menos popular debido a que cuenta con 0 asientos vendidos.")
    







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