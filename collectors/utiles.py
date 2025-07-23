# collectors/utiles.py

import duckdb
import pandas as pd

def guardar_resultados_duckdb(df: pd.DataFrame, db_path: str = "grafos.duckdb", table_name: str = "grafos"):
    """
    Guarda un DataFrame en una base de datos DuckDB, creando la tabla si no existe.
    """
    try:
        con = duckdb.connect(db_path)

        # Crear tabla si no existe con el esquema del DataFrame
        con.register("df", df)  # registra el DataFrame como una tabla temporal
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df LIMIT 0")
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        print(f"✅ Resultados guardados exitosamente en {db_path}, tabla '{table_name}'.")

    except Exception as e:
        print(f"⚠️ Error al guardar en DuckDB: {e}")

    finally:
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
