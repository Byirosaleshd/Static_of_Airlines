#Llamamos las librerias
import streamlit as st #App
import pandas as pd #Statics
import matplotlib.pyplot as plt #Graficos
import seaborn as sns #Graficos
import plotly.express as px #Graficos
import plotly.graph_objs as go #Graficos
import sqlite3 as sql #Database
import numpy as np # Algebra lineal
from sklearn.linear_model import LinearRegression #Regression
from sklearn.model_selection import train_test_split #Regression
from sklearn.metrics import r2_score #Regression
import Functions as ft #Functions for this program
import datetime as dt #Control for Time
from pandas import json_normalize #Json utilities
import json #Json utilites
import Sql as s #Sql querys
from PIL import Image #Images
from deep_translator import GoogleTranslator #Traducir
import statsmodels.api as sm #Regression
import statsmodels.formula.api as smf #Regression

# Conectar a la base de datos SQLite
conn = sql.connect('DATA/travel.sqlite')
translator = GoogleTranslator(source="en", target="es")


logo = Image.open(r'Images/avion.png')
st.sidebar.image(logo, width=100)
st.sidebar.header("Presentación")
st.sidebar.write(" ")
st.sidebar.write(" ")
option = st.sidebar.selectbox(
    'Selecciona una pagina para navegar por la app',
    ('Presentacion', 'Planteamiento', 'Campos de la BBDD', 'Pregunta A', 'Pregunta B',"Pregunta C","Pregunta D", "Pregunta E","Modelo de regresion"))
if option == 'Presentacion':
    st.write(" ")
    st.write(" ")
    Crj = Image.open(r'images/crj-200.jpg')
    st.sidebar.header('Recursos utilizados')
    st.sidebar.markdown('''
- [Database de Aerolineas](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset/data) De donde salio la informacion
''')
    col1, col2 = st.columns((1,4))
    col2.image(Crj, width=300)
    st.write(" ")
    st.write(" ")
    st.markdown("# Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos de Rusia durante el año 2017")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1, col2 = st.columns(2)
    col1.expander("Presentado por").write("- Ignacio Rosales\n- Lucia Bugallo\n- Daniel Sierra\n- María Alcalá\n- Daniel Aristiguieta")
    col2.expander("Git-hub").write("[Repositorio](https://github.com/Byirosaleshd/Static_of_Airlines)")
    
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


elif option == 'Campos de la BBDD':
    st.title("Entidades y campos")
    st.header("   - Entidad aircrafts_data")
    st.markdown(""" 
    1. **aircraft_code**: que alude al código de nueve aviones.
    2. **Model**: indica el tipo de modelo correspondiente a los nueve aviones. 
    3. **Range**: siendo el alcance la distancia que es capaz de recorrer volando a velocidad de crucero en línea recta.
    """)
    st.header("   - Entidad airports_data")
    st.markdown("""
    1. **airport_code**: que incluye el código del aeropuerto.
    2. **airport_name**: describe el nombre del aeropuerto.
    3. **city**: menciona la ciudad de cada aeropuerto.
    4. **coordinates**: señala las coordenadas de ubicación de cada aeropuerto.
    5. **timezone**: que es la zona horaria de cada ciudad con el continente al cual pertenece.""")
    st.header("   - Entidad boarding_passes:")
    st.markdown(""" 
    1. **ticket_no**: el cual describe el número de ticket.
    2. **flight_ID**: señala el código del vuelo.
    3. **boarding_no**: alude al número de reserva.
    4. **seat_no**: representa el número de asiento asignado por la aerolínea.""")
    st.header("   - Entidad bookings: ")
    st.markdown("""
    1. **book_ref**: señala la información correspondiente al vuelo.
    2. **book_date**: describe la fecha en la que fue emitido el libro. 
    3. **total_amount**: expresa el peso total que puede soportar un avión.""")
    st.header("   - Entidad flights:")        
    st.markdown("""
    1. **flight_id**: indica el código del vuelo.
    2. **flight_no**: expresa el código de vuelo emitido por la agencia de viajes o la misma aerolínea. 
    3. **schedule_ departure**: señala el despegue de los aviones hacia algún destino.
    4. **schedule_arrival**: indica la llegada de los aviones hacia algún destino.
    5. **departure_airport**: describe el código de aeropuerto de salida de un avión.
    6.**arrival_airport**: expresa el código del aeropuerto de llegada de un avión. 
    7. **Status**: relata información actualizada del vuelo que está realizándose o este próxima a realizarse.
    8. **aircraft_code**: que alude al código de nueve aviones.
    9. **actual_departure**: es un radar que expresa la salida y condiciones del vuelo en tiempo real.
    10. **actual_arrival**: es un radar en tiempo real que expresa la llegada y condiciones del vuelo en tiempo real.""")
    st.header("   - Entidad seats:")
    st.markdown("""
    1. **aircraft_code**: que alude al código de nueve aviones.
    2. **seat_no**: alude al número de asiento asignado por vuelo para cada pasajero.
    3. **fare_conditions**: expresa los tipos de vuelos a tomarse según cada aerolínea""")
    st.header("   - Entidad ticket_flights:")
    st.markdown(""" 
    1. **ticket_no**: el cual describe el número de ticket. 
    2. **flight_id**: indica el código del vuelo.
    3. **fare_conditions**: expresa los tipos de vuelos a tomarse según cada aerolínea. 
    4. **amount**: expresa el costo de cada vuelo según el tipo de boleto.""")
    st.header("   - Entidad tickets:")
    st.markdown(""" 
    1. **ticket_no**: el cual describe el número de ticket.
    2. **book_ref**: señala la información correspondiente al vuelo. 
    3. **passenger_id**: indica el código de cada usuario que ha comprado un ticket para un vuelo de avión.""")

      
    
elif option == 'Pregunta A':
    st.title("¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?")
    st.markdown("Duración de vuelos")
    st.markdown("Puedes seleccionar las columnas que deseas:")
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
    expandir.write(f"El modelo de avión que realiza vuelos en el menor tiempo promedio es: {modelo_menor_tiempo}")
    expandir.write(f"El modelo de avión que realiza la mayor cantidad de vuelos es: {modelo_mas_frecuente}")

    
    
    
    st.markdown("Vuelos realizados en Julio y Agosto")
    PreguntaA1= s.PreguntaA1
    df_PreguntaA1 = ft.imprimir_df("df_PreguntaA1",PreguntaA1,conn)
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



    
    

    expandir = st.expander("Ver interpretacion")
    expandir.write(f"Al analizar la distribución de las barras, podemos ver que el avión CN1 es el que más vuelos vendió en ambos meses, mientras que el avión 773 vendió menos vuelos en comparación. Y al ser un gráfico de barras apiladas tenemos que la barra de Julio es más larga que la barra de agosto, lo que indica que se vendieron más vuelos en Julio que en agosto; esto puede ser debido a que julio es un mes de alta demanda para viajes debido a las vacaciones de verano en algunos países, lo que podría explicar el aumento en la cantidad de vuelos vendidos.")

    
    st.markdown("Alcance de Aviones")
    PreguntaA2 = s.PreguntaA2
    df_PreguntaA2 = ft.imprimir_df("df_PreguntaB",PreguntaA2,conn)
    
    x = df_PreguntaA2['CODIGO DE AVION']
    y = df_PreguntaA2['ALCANCE DEL AVION']
    fig, ax = plt.subplots()
    ax.stem(x, y, linefmt = '--')
    ax.set_xlabel('Avión')
    ax.set_ylabel('Alcance')
    ax.set_title('Alcance por avión')
    plt.show() 
    st.plotly_chart(fig)  
    
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"El avión con un mayor alcance es el 773, en comparación a los demás.")



elif option == 'Pregunta B':
    st.title("¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?:")
    st.header("Total de asientos vendidos por los aviones")
    st.markdown("Puedes seleccionar las columnas que desees:")
    Pregunta_B = s.Pregunta_B
    df_PreguntaB = ft.pasar_dataframe("df_PreguntaB",Pregunta_B,conn)
    df_Pregunta_B = ft.imprimir_df("df_PreguntaB",Pregunta_B,conn)
    columnas = list(df_PreguntaB.columns)
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    columnas_seleccionadas = st.sidebar.multiselect('Selecciona las columnas a mostrar', columnas, default=["CodigodeAvion","Economy","Business","Comfort"])
    data_filt = df_PreguntaB[columnas_seleccionadas]
    st.dataframe(data_filt,width=550, height=400)
#     ft.Grafico_multibarras(df_PreguntaB,'Economy','Business','Comfort',"Economy","Business","Comfort","Asientos Vendidos","Código de Avion","ASIENTOS VENDIDOS POR AVION")
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"Como podemos apreciar en la gráfica, los asientos más vendidos son los de clase económica, que ocupan más del 50% de los puestos totales de cada aeronave. Si nos guiamos por el avión que ha vendido una mayor cantidad de puestos, podemos ver que vendría siendo la nave cuyo código es “773”, el cual indica que tiene una mayor venta de puestos de clase económica, como también tuvo una mayor venta en las otras dos clases. Siendo así, la aeronave con mayores asientos vendidos.")
    codigo_avion = df_PreguntaB["CodigodeAvion"]
    economy = df_PreguntaB["Economy"]
    business = df_PreguntaB["Business"]
    comfort = df_PreguntaB["Comfort"]
    
    fig = go.Figure(data=[
        go.Bar(name="Economy", x=codigo_avion, y=economy, marker_color="skyblue"),
        go.Bar(name="Business", x=codigo_avion, y=business, marker_color="royalblue"),
        go.Bar(name="Comfort", x=codigo_avion, y=comfort, marker_color="dodgerblue")
    ])
    fig.update_layout(barmode='stack')  # Cambia el modo de las barras
    fig.update_layout(
        title="Asientos Vendidos Por Avión",
        xaxis_title="Código de Avión",
        yaxis_title="Asientos Vendidos",
        barmode="group"
    )
    st.plotly_chart(fig)
    
    
    labels = df_Pregunta_B.CodigodeAvion
    Economy = df_Pregunta_B.Economy
    Business = df_Pregunta_B.Business
    Comfort = df_Pregunta_B.Comfort

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

    ax.bar_label(barra1, padding=1, fontsize=5)
    ax.bar_label(barra2, padding=1, fontsize=5)
    ax.bar_label(barra3, padding=1, fontsize=5)

    ax.set_ylim(0,185000)
    fig.tight_layout()

    plt.show()
    st.pyplot(fig)
    columnas = list(df_Pregunta_B.columns)
    st.markdown("Como podemos apreciar en la gráfica, los asientos más vendidos son los de clase económica, que ocupan más del 50% de los puestos totales de cada aeronave. Si nos guiamos por el avión que ha vendido una mayor cantidad de puestos, podemos ver que vendría siendo la nave cuyo código es “773”, el cual indica que tiene una mayor venta de puestos de clase económica, como también tuvo una mayor venta en las otras dos clases. Siendo así, la aeronave con mayores asientos vendidos.")

    
    labels = df_Pregunta_B.CodigodeAvion
    Economy = df_Pregunta_B.Economy
    Business = df_Pregunta_B.Business
    Comfort = df_Pregunta_B.Comfort
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

    ax.bar_label(barra1, padding=1, fontsize=5)
    ax.bar_label(barra2, padding=1, fontsize=5)
    ax.bar_label(barra3, padding=1, fontsize=5)

    ax.set_ylim(0,185000)
    fig.tight_layout()

    plt.show()
    st.pyplot(fig)
    columnas = list(df_Pregunta_B.columns)
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"Como podemos apreciar en la gráfica, los asientos más vendidos son los de clase económica, que ocupan más del 50% de los puestos totales de cada aeronave, esto debido a que es la clase con mayor accesibilidad financiera para los pasajeros. Si nos guiamos por el avión que ha vendido una mayor cantidad de puestos, podemos ver que vendría siendo la nave cuyo código es “SU9”, el cual indica que tiene una mayor venta de puestos de clase económica, como también tuvo una mayor venta en la clase Business, mientras que el único avión en vender asientos en clase comfort fue la aeronave cuyo código es 773.")




elif option == 'Pregunta C':
    st.title("¿Cuál es la ruta con mayor frecuencia realizada por los aviones, que avión realiza mayor cantidad de vuelos para las rutas Europa-Europa, Europa-Asia, Asia-Asia y Asia-Europa?")
    Pregunta_C1 = s.Pregunta_C1   
    Df_Pregunta_C1 = ft.imprimir_df("Df_PreguntaC",Pregunta_C1,conn)
    columnas = list(Df_Pregunta_C1.columns)
    labels = Df_Pregunta_C1['Avion']
    Europa_Europa = Df_Pregunta_C1['Europa-Europa']
    Europa_Asia = Df_Pregunta_C1['Europa-Asia']
    Asia_Asia = Df_Pregunta_C1['Asia-Asia']
    Asia_Europa = Df_Pregunta_C1['Asia-Europa']
    fig, ax = plt.subplots()
    ax.bar(labels, Europa_Europa, 0.5, color = '#3A95B1', edgecolor = "black", linewidth = 0.5, label='Europe-Europe')
    ax.bar(labels, Europa_Asia, 0.5, bottom=Europa_Europa, color = '#7BBFC9', edgecolor = "black", linewidth = 0.5, label='Europe-Asia')
    ax.bar(labels, Asia_Asia, 0.5, bottom=[i+j for i,j in zip(Europa_Europa, Europa_Asia)], color = '#BCE4D8', edgecolor = "black", linewidth = 0.5, label='Asia-Asia')
    ax.bar(labels, Asia_Europa, 0.5, bottom=[i+j+k for i,j,k in zip(Europa_Europa, Europa_Asia, Asia_Asia)], color = '#7CC098', edgecolor = "black", linewidth = 0.5, label='Asia-Europe')
    ax.set_xlabel('Aviones')
    ax.set_ylabel('Cantidad de vuelos')
    ax.set_title('Grafico de barras de vuelos por ruta')
    ax.legend()
    plt.show()
    st.pyplot(fig)
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"En la gráfica contamos con 8 aviones, y sus respectivos vuelos categorizados por la ruta que hayan tomado. Podemos apreciar que la ruta con mayores aviones circulando es la de Europa-Europa. Tenemos que 5 de 8 aviones realizan vuelos en las 4 rutas posibles, pero el avión cuyo código es “SU9” realiza mayor cantidad de vuelos para la ruta Europa-Europa con 2212 vuelos. El avión cuyo código es “CR2” realiza mayor cantidad de vuelos para las rutas: Europa-Asia con 685 vuelos y Asia-Europa con 683 vuelos. Y por último el avión cuyo código es “CN1” realiza una mayor cantidad de vuelos para la ruta Asia-Asia con 1976 vuelos.")


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
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"En la base de datos se cuenta con un total de 16.707 vuelos que llegaron a su destino, en este gráfico de torta podemos apreciar que la ruta con mayor cantidad de vuelos es Europa-Europa con un 48%, duplicando la cantidad de vuelos que cuenta la segunda ruta más frecuentada por los aviones que es Asia-Asia, mientras que las rutas con destinos internacionales tienen el mismo porcentaje.")



elif option == 'Pregunta D':
    st.title("Si los aviones realizan vuelos entre los continentes de Asia y Europa: ¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?:")
    st.markdown("Puedes seleccionar las columnas que desees:")
    Pregunta_D1 = s.Pregunta_D1
    Df_Pregunta_D1 = ft.read_abilities(Pregunta_D1,conn)
    Df_Pregunta_D1 = ft.pasar_dataframe("Pregunta_D1",Pregunta_D1,conn)
    ft.limpiar_json(Df_Pregunta_D1,"Ciudad","Ciudad en ingles","Ciudad en ruso")
    Df_Pregunta_D1["Numero de vuelos"] = Df_Pregunta_D1["num_flights"] 
    Df_Pregunta_D1 = Df_Pregunta_D1.drop("num_flights", axis=1)
    Df_Pregunta_D1 = Df_Pregunta_D1[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
    Df_Pregunta_D1 =  Df_Pregunta_D1.sort_values(by="Numero de vuelos", ascending=False)
    columnas = list(Df_Pregunta_D1.columns)
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    columnas_seleccionadas = st.sidebar.multiselect('Selecciona las columnas a mostrar', columnas, default=["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"])
    data_filt = Df_Pregunta_D1[columnas_seleccionadas]
    st.dataframe(data_filt,width=550, height=400)

    
    
    
    
    st.bar_chart(Df_Pregunta_D1, x="Ciudad en ingles", y="Numero de vuelos")
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"Al analizar la gráfica podemos apreciar que la ciudad que recibe una mayor cantidad de vuelos del avión cuyo código es “763” es la ciudad de Moscow con una cantidad altamente representativa frente a las demás ciudades, cuenta con un total de 453 vuelos recibidos por dicho avión ,esto puede ser debido a que es una ciudad que cuenta con mayor turismo en el continente asiático; mientras que como segundas ciudades con mayor cantidad de vuelos, encontramos a las cuidades de Krasnodar y Khabarovsk con un total de 122 vuelos recibidos.")

    
    st.title("Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?")
    PreguntaD2 = s.PreguntaD2
    Df_PreguntaD2 = ft.read_abilities(PreguntaD2,conn)
    ft.limpiar_json(Df_PreguntaD2,"asian_city","Ciudad en ingles","Ciudad en ruso")
    Df_PreguntaD2["Numero de vuelos"] = Df_PreguntaD2["num_flights"] 
    Df_PreguntaD2 = Df_PreguntaD2.drop("num_flights", axis=1)
    Df_PreguntaD2 = Df_PreguntaD2[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
    Df_PreguntaD2 =  Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)
    Df_PreguntaD2["Ciudad"] = Df_PreguntaD2["Ciudad en ingles"].apply(translator.translate)
    Df_PreguntaD2_sorted = Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)
    Df_PreguntaD2_sorteda = Df_PreguntaD2_sorted[["Ciudad","Numero de vuelos"]]
    Df_PreguntaD2_sorteda = Df_PreguntaD2_sorteda[["Ciudad","Numero de vuelos"]]
    Df_PreguntaD2_sorteda = Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)
    st.write(Df_PreguntaD2_sorteda)
    st.bar_chart(Df_PreguntaD2_sorteda, x="Ciudad", y="Numero de vuelos", color="#FF0000")
    columnas = list(Df_PreguntaD2_sorteda.columns)
    expandir = st.expander("Ver interpretacion")
    expandir.write(f"La ciudad que recibe una mayor cantidad de vuelo de parte de las aerolíneas europeas es Perm, ciudad de Rusia que está situada a orillas del río Kama en la parte europea de Rusia, y cuenta con un total de 366 vuelos recibidos.")


elif option == 'Pregunta E':

    st.title("Entre los modelos de aviones con los códigos: CR2, SU9 y CN1 se desea conocer lo siguiente: vuelos realizados al aeropuerto DME")
    Pregunta_e2_1= s.E2_1
    df_Pregunta_E1 = ft.imprimir_df("df_PreguntaB",Pregunta_e2_1,conn)
    #columnas = list(df_Pregunta_E1.columns)
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    #columnas_seleccionadas = st.sidebar.multiselect('Selecciona las columnas a mostrar', columnas, default=["Avión","Frecuencia_de_vuelos_realizados"])
    #data_filt = df_Pregunta_E1[columnas_seleccionadas]
    #st.dataframe(data_filt,width=550, height=400)
    ft.grafico_pie_nueva(df_Pregunta_E1)

    st.title("Entre los modelos de aviones con los códigos: CR2, SU9 y CN1 se desea conocer lo siguiente: vuelos realizados al aeropuerto DME")
    Pregunta_e2_2= s.E2_2
    df_Pregunta_E2 = ft.imprimir_df("df_PreguntaB",Pregunta_e2_2,conn)
    CLASES = ['Economy','Comfort', 'Business']
    AVION_CR2 = [8939, 0, 0]
    AVION_CN1 = [601, 0, 0]
    AVION_SU9 = [20880, 0, 2975]
    # Crear la figura y el eje
    fig, ax = plt.subplots()
    # Crear la gráfica
    plt.plot(CLASES, AVION_CR2, label="CR2", marker='o', linestyle='-', color='#3A95B1')
    plt.plot(CLASES, AVION_CN1, label="CN1", marker='o', linestyle='-', color= '#BCE4D8')
    plt.plot(CLASES, AVION_SU9, label="SU9", marker='o', linestyle='-', color= '#7CC098')
    plt.xlabel("Condicion de vuelo")
    plt.ylabel("tickets vendidos")
    plt.title("Tickets vendidos por condicion de vuelo")
    ax.grid(True)  # Agregar líneas de cuadrícula
    ax.legend(loc='upper right')  # Mover la leyenda a la esquina superior derecha
    plt.legend()
    st.pyplot(fig)

elif option == 'Modelo de regresion':
        #-- TABLA DEL RANGO
    aircrafts_data = "SELECT * FROM aircrafts_data;"
    Df_aircrafts_data = ft.read_abilities(aircrafts_data,conn)

    #-- TABLA DEL Monto total de las reservas
    bookings = "SELECT * FROM bookings;"
    Df_bookings = ft.read_abilities(bookings,conn)

    #-- TABLA DEL PRECIO DE VENTA
    ticket_flights = "SELECT * FROM ticket_flights;"
    Df_ticket_flights = ft.read_abilities(ticket_flights,conn)

    flights = "SELECT * FROM flights;"
    Df_flights = ft.read_abilities(flights,conn)
    
    tickets = "SELECT * FROM tickets;"
    Df_tickets = ft.read_abilities(tickets,conn)    
    
    Distancia = """
    SELECT
        flight_id,
        Ciudad_salida,
        Ciudad_llegada,
        2 * 6371 * ASIN(SQRT(
            POWER(SIN(RADIANS((to_latitude - from_latitude) / 2)), 2) +
            COS(RADIANS(from_latitude)) * COS(RADIANS(to_latitude)) *
            POWER(SIN(RADIANS((to_longitude - from_longitude) / 2)), 2)
        )) AS distancia_km
    FROM (SELECT    
    flights.flight_id,
    json_extract(departure.city, '$.en') AS Ciudad_salida,
    CAST(SUBSTR(departure.coordinates, 2, INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_longitude,
    CAST(SUBSTR(departure.coordinates, INSTR(departure.coordinates, ',') + 1, LENGTH(departure.coordinates) - INSTR(departure.coordinates, ',') - 2) AS REAL) AS from_latitude,
json_extract(arrival.city, '$.en') AS Ciudad_llegada,
    CAST(SUBSTR(arrival.coordinates, 2, INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_longitude,
    CAST(SUBSTR(arrival.coordinates, INSTR(arrival.coordinates, ',') + 1, LENGTH(arrival.coordinates) - INSTR(arrival.coordinates, ',') - 2) AS REAL) AS to_latitude
    from
    flights 
    INNER JOIN airports_data AS departure
    ON flights.departure_airport = departure.airport_code
    INNER JOIN airports_data AS arrival
    ON flights.arrival_airport = arrival.airport_code);
"""
    Df_distancia = ft.read_abilities(Distancia,conn)  

    Merged_df = Df_ticket_flights.merge(Df_flights, on='flight_id', how='inner')
    Merged_df = Df_aircrafts_data.merge(Merged_df, on='aircraft_code', how='inner' )
    Merged_df = Df_tickets.merge(Merged_df, on='ticket_no', how='inner')
    Merged_df = Df_bookings.merge(Merged_df, on='book_ref', how='inner' )
    Merged_df = Df_distancia.merge(Merged_df, on='flight_id', how='inner')
    Merged_df_new = Merged_df[["aircraft_code","range","amount","total_amount","distancia_km"]] 
    Merged_df_new    
    correlation_matrix = Merged_df_new.select_dtypes(include=['int64', 'float64']).corr()

    # Crear un mapa de calor de la matriz de correlación
    fig = plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de Correlación')
    plt.show()
    sns.pairplot(Merged_df_new.select_dtypes(include=['int64', 'float64']))
    plt.show()
    st.pyplot(fig)

    # Ajustar el modelo de regresión lineal simple usando statsmodels
    modelo = smf.ols('range ~ amount', data=Merged_df_new).fit()
    st.write(modelo.summary())
    
    Merged_df_new['predicted_range'] = modelo.predict(Merged_df_new['range'])

    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(x='range', y='amount', data=Merged_df_new, label='Datos Observados')\
#    sns.lineplot(x='petal_length', y='predicted_sepal_length', data=Merged_df_new, color='red', label='Línea de Regresión')
#    plt.xlabel('Petal Length')
#    plt.ylabel('Sepal Length')
#    plt.title('Regresión Lineal Simple: Sepal Length vs Petal Length')
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