# Static_of_Airlines

## BREVE RESUMEN DEL TRABAJO
Desde los primeros intentos de vuelo de los hermanos Wright en 1903, la aviación ha experimentado avances significativos en tecnología, diseño y seguridad. Actualmente, un avión es un medio de transporte común implementado para la realización de viajes en corta, mediana y larga distancia. La finalidad de llevar acabo esta investigación estadística, consiste en reconocer los modelos de aviones idóneos para la realización de vuelos en Rusia durante el año 2017.  Es importante destacar, que la utilización de los histogramas, gráficos circulares, gráficos de barra y los cálculos estadísticos como promedios, desviaciones típicas, kurtosis, porcentajes, ente otros, fueron necesarios para conocer el comportamiento de cada modelo de avión y evaluar su rentabilidad en la venta de clases de vuelo.

## INTERROGANTES DEL TRABAJO
1. ¿Qué modelo de avión realiza una mayor cantidad de vuelos, y cuál lo hace en un menor tiempo?

2. ¿Qué modelo de avión ha vendido en promedio una mayor cantidad de puestos según la clase del vuelo?

3. En la base de datos contamos con 4 rutas posibles realizadas por los aviones registrados, se quiere saber:
- ¿Cuál es la ruta con mayor frecuencia realizada por los aviones, que avión realiza mayor cantidad de vuelos para las rutas Europa-Europa, Europa-Asia, Asia-Asia y Asia-Europa?
- ¿Cuál es la ruta con mayores vuelos, sin importar el avión?

4. Si los aviones realizan vuelos entre los continentes de Asia y Europa:
- ¿Cuáles son las ciudades en recibir vuelos cuyo modelo de avión pertenece al código 763?
- Dentro de los aeropuertos asiáticos, ¿Quiénes recibe una mayor cantidad de vuelos provenientes de aerolineas europeas?

5. Entre los modelos de aviones con los códigos: CR2, SU9 y CN1 se desea conocer lo siguiente:
- Vuelos realizados al aeropuerto DME.
- ¿Cuántos de estos modelos tienen una mayor cantidad de vuelos realizados con boletos vendidos para el destino en DME?

## OBJETIVO DEL TRABAJO
Determinar el mejor modelo de avión para vuelos más eficientes en distintos aeropuertos de Rusia durante el año 2017

## BASE DE DATOS
- [Database de Aerolineas](https://www.kaggle.com/datasets/saadharoon27/airlines-dataset/data)

## PRINCIPALES ENTIDADES DE LA DATA UTILIZADAS
    1. FLIGHTS
    2. AIRCRAFTS_DATA
    3. TICKETS_FLIGHTS

## ASPECTOS IMPORTANTES A CONSIDERAR
- Rusia pertenece a dos continentes a la vez, estos son: Europa y Asia.
- Se trabajaron con datos donde el estado del vuelo haya sido 'Arrived', lo que indicaba que el avión llegó a su destino, debido a que hubieron vuelos cancelados o reprogramados.

## PRINCIPALES LIBRERIAS
- streamlit
- pandas
- matplotlib.pyplot
- seaborn
- ploty.express
- ploty.graph_objs
- sqlite3
- numpy

## PROGRAMAS UTILIZADOS PARA LA REALIZACIÓN DEL TRABAJO
    1. Python
    2. GitHub
    3. Power BI