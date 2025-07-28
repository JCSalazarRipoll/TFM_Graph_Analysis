# main.py

from collectors.parser import url_dataframe
from collectors import guardar_resultados_en_duckdb
import pandas as pd
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/ejecucion.log",mode='w'),
        logging.StreamHandler()
    ]
)

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
        logging.info("Inicio del proceso de recopilación y análisis de grafos.")

        df = url_dataframe(URLS, HEAD_URL)

        if not df.empty:
            logging.info(f"Columnas en df: {df.columns.tolist()}")
            # Eliminar duplicados por nombre, nodos y aristas (opcional pero útil)
            df.drop_duplicates(subset=["nombre", "nodos", "aristas"], inplace=True)

            # Guardar como CSV
            df.to_csv("datos_grafos.csv", index=False)
            logging.info(f"{len(df)} grafos procesados correctamente. Archivo guardado como datos_grafos.csv")

            # Mostrar resumen básico
            logging.info("Resumen de grafos procesados:\n" + df[["nombre", "nodos", "aristas"]].to_string(index=False))

            # Guardar en DuckDB
            guardar_resultados_en_duckdb(df, db_path="resultados.duckdb", tabla="experimentos")
            logging.info("Resultados almacenados en la base de datos DuckDB: resultados.duckdb")
        else:
            logging.info("No se procesó ningún grafo válido.")
    except Exception as e:
        logging.error("Ocurrió un error durante la ejecución", exc_info=True)
