import pandas as pd 

def read_abilities(query:str, conector) -> pd.DataFrame:
    """"Esta funcion crea el Dataframe que se requiere para el ejemplo """

    Df_aircrafts_data   = pd.read_sql_query(sql = query, con = conector)
    return Df_aircrafts_data


def load_view_to_dataframe(view_name:str) -> pd.DataFrame:
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql_query(query, conn)

