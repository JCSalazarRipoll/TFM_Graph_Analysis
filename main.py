# main.py

from collectors.parser import url_dataframe
from collectors import guardar_resultados_en_duckdb
import pandas as pd

HEAD_URL = "https://networkrepository.com/asn.php"
URLS = [
    "https://networkrepository.com/insecta-ant-colony1-day01.php",
    "https://networkrepository.com/insecta-ant-colony1-day02.php",
    "https://networkrepository.com/insecta-ant-colony1-day03.php",
    "https://networkrepository.com/insecta-ant-colony1-day04.php",
    "https://networkrepository.com/insecta-ant-colony1-day05.php"
]

if __name__ == "__main__":
    try:
        df = url_dataframe(URLS, HEAD_URL)
    
        if not df.empty:
            df.to_csv("datos_grafos.csv", index=False)
            print(f"\n{len(df)} grafos procesados correctamente. Archivo guardado como datos_grafos.csv")
    
            # Guardar en DuckDB
            guardar_resultados_en_duckdb(df, db_path="resultados.duckdb", tabla="experimentos")
            print("Resultados almacenados en la base de datos DuckDB: resultados.duckdb")
        else:
            print("No se procesó ningún grafo válido.")
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")



