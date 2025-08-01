# main.py

#Librerías necesarias para ejecutar el código desde main
import pandas as pd
import logging
import os

from pathlib import Path

#Cargar funciones desde los diferentes directorios creados
from collectors.parser import url_dataframe
from collectors import guardar_resultados_en_duckdb, leer_config_desde_txt

#Se crea una carpeta para almacenar los logs generados
os.makedirs("logs", exist_ok=True)

#Se define la configuracion de los logs
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/ejecucion.log",mode='w'),
        logging.StreamHandler()
    ]
)

head_url, urls = leer_config_desde_txt("collectors/ant_colony.txt")

import os
from pathlib import Path


carpeta = Path("collectors")
archivos_txt = sorted(carpeta.glob("*.txt"))  # Todos los .txt ordenados alfabéticamente

for archivo in archivos_txt:
    print(archivo)

if __name__ == "__main__":
    try:
        logging.info("Inicio del proceso de recopilación y análisis de grafos.")

        df = pd.DataFrame()
        #Esta función devuelve un dataframe con los datos obtenidos de los grafos

        for archivo in archivos_txt:
            head_url, urls = leer_config_desde_txt(archivo)
            df_temp = url_dataframe(urls,head_url)
            df = pd.concat([df, df_temp], ignore_index=True)

        #En caso de que se hayan podido procesar los grafos correctamente
        if not df.empty:
            #imprime la informacion de las columnas dentro del dataframe
            logging.info(f"Columnas en df: {df.columns.tolist()}")
            # Elimina duplicados por nombre, nodos y aristas
            df.drop_duplicates(subset=["nombre", "nodos", "aristas"], inplace=True)

            # Guarda como CSV
            df.to_csv("datos_grafos.csv", index=False)
            logging.info(f"{len(df)} grafos procesados correctamente. Archivo guardado como datos_grafos.csv")

            # Muestra el resumen básico
            logging.info("Resumen de grafos procesados:\n" + df[["nombre", "nodos", "aristas"]].to_string(index=False))

            # Guarda en DuckDB
            guardar_resultados_en_duckdb(df, db_path="resultados.duckdb", tabla="experimentos")
            logging.info("Resultados almacenados en la base de datos DuckDB: resultados.duckdb")
            
        else:
            logging.info("No se procesó ningún grafo válido.")
    except Exception as e:
        logging.error("Ocurrió un error durante la ejecución", exc_info=True)
