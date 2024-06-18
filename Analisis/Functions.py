import streamlit as st
import datetime as dt
import pandas  as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3 as sql
import numpy as np
import Functions as ft
import datetime as dt
from pandas import json_normalize
import json
import Sql as s

    
def load_sql(type:str) -> pd.DataFrame:
    consulta = f'SELECT name FROM sqlite_master Where type={type} ORDER BY name;'
    print("Entidades o Vistas en la base de datos:")
    nombre_tabla = pd.read_sql_query(consulta,conn)
    return nombre_tabla
    

def read_abilities(query:str, conector) -> pd.DataFrame:
    Df_aircrafts_data   = pd.read_sql_query(sql = query, con = conector)
    return Df_aircrafts_data


def load_view_to_dataframe(view_name:str) -> pd.DataFrame:
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql_query(query, conn)


def procesar_vuelos(Df, columna_salida, columna_llegada):
    Df[columna_salida] = pd.to_datetime(Df[columna_salida])
    Df[columna_llegada] = pd.to_datetime(Df[columna_llegada])
    Df['hora de salida'] = Df[columna_salida].apply(lambda x: x.hour + x.minute / 60)
    Df['hora de llegada'] = Df[columna_llegada].apply(lambda x: x.hour + x.minute / 60)
    Df['duracion_vuelo'] = Df['hora de salida'] - Df['hora de llegada']
    modelo_tiempo_promedio = Df.groupby('model')['duracion_vuelo'].mean()
    modelo_tiempo_promedio = modelo_tiempo_promedio.sort_values(ascending=True)
    modelo_menor_tiempo = modelo_tiempo_promedio.index[0]
    return modelo_menor_tiempo


def modelo_frecuente(Df, columna_salida):    
    modelo_vuelos = Df.groupby('model')[columna_salida].count()
    modelo_vuelos = modelo_vuelos.sort_values(ascending=False)
    modelo_mas_frecuente = modelo_vuelos.index[0]
    return modelo_mas_frecuente



def caracteristicas_modelo(Df, columna_salida, columna_llegada,nombres):
    modelo_menor_tiempo = procesar_vuelos(Df, columna_salida, columna_llegada)
    modelo_mas_frecuente = modelo_frecuente(Df, columna_salida)
    st.write(f"El modelo de avión que realiza vuelos en el menor tiempo promedio es: {modelo_menor_tiempo}")
    st.write(f"El modelo de avión que realiza la mayor cantidad de vuelos es: {modelo_mas_frecuente}")
    Df[columna_salida] = pd.to_datetime(Df[columna_salida]).dt.time
    Df[columna_llegada] = pd.to_datetime(Df[columna_llegada]).dt.time
    Df = Df[[columna_salida,'hora de salida',columna_llegada,'hora de llegada','departure_airport','arrival_airport','status','aircraft_code','Nombre en ingles','Nombre en ruso','duracion_vuelo']]
    st.write(Df)

def cargar_librerias(nombre_librerias):
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
    
    
    
def Grafico_multibarras(df,tipo1,tipo2,tipo3,label1:str,label2:str,label3:str,ylabel:str,xlabel:str,title:str):
    labels = df.CodigodeAvion
    tipo1 = df.Economy
    tipo2 = df.Business
    tipo3 = df.Comfort
    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots()
    barra1 = ax.bar(x-0.30, tipo1, width, label=label1, color='#87CEFA')
    barra2 = ax.bar(x, tipo2, width, label=label2, color='#4169E1')
    barra3 = ax.bar(x+0.30, tipo3, width, label=label3, color='#1E90FF')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title) 
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(barra1, padding=1)
    ax.bar_label(barra2, padding=1)
    ax.bar_label(barra3, padding=1)
    ax.set_ylim(0,350)
    fig.tight_layout()
    plt.show()
    return st.pyplot(fig)
    
    
 #que va despues de la s?   
#def imprimir_tabla(nombre_de_consulta, conn, nombre_del_nuevo_dataframe, argumento ):
    #nombre_de_consulta = s.argumento
    #nombre_del_nuevo_dataframe = pd.read_sql_query(nombre_de_consulta, con = conn)
    #st.write(nombre_del_nuevo_dataframe)
    
    
    
