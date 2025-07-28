#collectors.__init__.py

from .descargador import crear_zip_url, cargar_grafo_desde_url
from .metricas_grafos import extraer_estadisticas_red
from .utiles import leer_archivo_aristas, guardar_resultados_en_duckdb

__all__ = [
    "crear_zip_url",
    "cargar_grafo_desde_url",
    "extraer_estadisticas_red",
    "leer_archivo_aristas",
    "guardar_resultados_en_duckdb"
]
