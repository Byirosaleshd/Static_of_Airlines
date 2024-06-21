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

    
#def load_sql(type:str) -> pd.DataFrame:
#    consulta = f'SELECT name FROM sqlite_master Where type={type} ORDER BY name;'
#    print("Entidades o Vistas en la base de datos:")
#    nombre_tabla = pd.read_sql_query(consulta,conn)
#    return nombre_tabla
    

def read_abilities(query:str, conector) -> pd.DataFrame:
    Df_aircrafts_data   = pd.read_sql_query(sql = query, con = conector)
    return Df_aircrafts_data


#def load_view_to_dataframe(view_name:str) -> pd.DataFrame:
#    query = f"SELECT * FROM {view_name}"
#    return pd.read_sql_query(query, conn)


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
    
    
def grafico_pie(df):
    fig, ax = plt.subplots()
    aviones = df.Avión
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
    return st.pyplot(fig)
    
    

def grafico_barras_superpuestas(df):
    fig, ax = plt.subplots()
    x = df.Avion

    clase_economy = df.TICKETS_ECONOMY
    clase_comfort = df.TICKETS_COMFROT
    clase_business = df.TICKETS_BUSINESS
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
    return st.pyplot(fig)



def limpiar_json(df,name_total,name1,name2):
    Df_PreguntaD2[name_total] = Df_PreguntaD2[name_total].apply(json.loads)
    Df_PreguntaD2[[name1, name2]] = Df_PreguntaD2[name_total].apply(lambda x: pd.Series([x["en"], x["ru"]]))
    Df_PreguntaD2 = Df_PreguntaD2.drop(name_total, axis=1)
    Df_PreguntaD2 = Df_PreguntaD2[["city_en","city_ru","num_flights"]]
    Df_PreguntaD2["Numero de vuelos"] = Df_PreguntaD2["num_flights"] 
    Df_PreguntaD2 = Df_PreguntaD2.drop("num_flights", axis=1)
    Df_PreguntaD2["Ciudad en ingles"] = Df_PreguntaD2["city_en"]
    Df_PreguntaD2["Ciudad en ruso"] = Df_PreguntaD2["city_ru"]
    Df_PreguntaD2 = Df_PreguntaD2.drop("city_en", axis=1)
    Df_PreguntaD2 = Df_PreguntaD2.drop("city_ru", axis=1)
    Df_PreguntaD2 = Df_PreguntaD2[["Ciudad en ingles","Ciudad en ruso","Numero de vuelos"]]
    Df_PreguntaD2 =  Df_PreguntaD2.sort_values(by="Numero de vuelos", ascending=False)



def limpiar_json(df,columna_completa,columna_ingles,columna_ruso):
    df[columna_completa] = df[columna_completa].apply(json.loads)
    df[[columna_ingles, columna_ruso]] = df[columna_completa].apply(lambda x: pd.Series([x["en"], x["ru"]]))
    df = df.drop(columna_completa, axis=1)
    
    
def imprimir_df(df,Pregunta,conn):
    df = ft.read_abilities(Pregunta,conn)
    st.write(df)
    return df
    