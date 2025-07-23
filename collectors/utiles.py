# collectors/utiles.py

import duckdb
import pandas as pd
from datetime import datetime

def guardar_resultados_en_duckdb(df_resultados: pd.DataFrame, db_path: str = "resultados.duckdb", tabla: str = "experimentos"):
    """
    Guarda los resultados de un DataFrame en una base de datos DuckDB.

    Si la tabla no existe, la crea. Si existe, inserta los nuevos registros.
    Maneja errores y asegura el cierre de la conexión.
    """
    con = None
    try:
        con = duckdb.connect(db_path)

        if "timestamp" not in df_resultados.columns:
            df_resultados["timestamp"] = datetime.now()

        con.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabla} AS 
            SELECT * FROM df_resultados LIMIT 0
        """)

        con.register("df_temp", df_resultados)
        con.execute(f"INSERT INTO {tabla} SELECT * FROM df_temp")

    except Exception as e:
        print(f"[ERROR] No se pudo guardar en DuckDB: {e}")

    finally:
        if con:
            con.close()

def leer_archivo_aristas(path: str):
    aristas = []
    with open(path, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) >= 2:
                try:
                    aristas.append((int(partes[0]), int(partes[1])))
                except ValueError:
                    continue
    return aristas
