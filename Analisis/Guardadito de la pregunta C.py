""" 
DF_Destino_Clase = "SELECT *, SQRT(Varianza) AS 'Desviación tipica', SQRT(Varianza)/Precio_Promedio * 100 AS 'Coeficiente de variacion' FROM PREGUNTA_C;"
DF_Destino_Clase
DF_Destino_Clase= "SELECT  aircraft_code, fare_conditions,arrival_airport, amount FROM flights  INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id WHERE aircraft_code IN ('773','763','SU9')"
DF_Destino_Clase =pd.read_sql_query(sql = DF_Destino_Clase, con=conn)
DF_Destino_Clase
DF_Destino_Clase = DF_Destino_Clase.groupby(['arrival_airport','fare_conditions'])['amount'].count()
DF_Destino_Clase = pd.DataFrame(DF_Destino_Clase)
DF_Destino_Clase
DF_Destino_Clase['amount'].mean()
DF_Destino_Clase['Promedio']= DF_Destino_Clase['amount'].mean()
DF_Destino_Clase['amount'].var()
DF_Destino_Clase['Varianza']= DF_Destino_Clase['amount'].var()
DF_Destino_Clase['amount'].std()
DF_Destino_Clase['Desviacion Tipica']= DF_Destino_Clase['amount'].std()
DF_Destino_Clase['Coeficiente de Variacion']= DF_Destino_Clase['Desviacion Tipica']/DF_Destino_Clase['Promedio']*100
DF_Destino_Clase = DF_Destino_Clase.round(2)
DF_Destino_Clase.head()
precios = pd.read_sql_query("""SELECT  aircraft_code, fare_conditions,arrival_airport, amount
FROM flights 
INNER JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
WHERE aircraft_code IN ('773','763','SU9')
GROUP BY arrival_airport, fare_conditions""",con=conn)
df_precios = precios.groupby(['aircraft_code','arrival_airport', 'fare_conditions'])['amount'].sum().reset_index()
dv = df_precios["amount"].std()
media = df_precios["amount"].mean()

coeficiente_de_variavion = (media/dv)*100
round(coeficiente_de_variavion,2)
"""
