import streamlit as st
import datetime as dt
import pandas    as pd
import seaborn   as sns
import matplotlib.pyplot as plt
import sqlite3 as sql
import numpy as np
import Functions as ft
import datetime as dt
from pandas import json_normalize
import json

def read_abilities(query:str, conector) -> pd.DataFrame:
    """"Esta funcion crea el Dataframe que se requiere para el ejemplo """
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

