#collectors.__init__.py

from .descargador import crear_zip_url, cargar_grafo_desde_url, cargar_o_descargar_grafo
from .metricas_grafos import distancia_promedio_nodos
from .utiles import leer_archivo_aristas, guardar_resultados_en_duckdb


__all__ = [
    "crear_zip_url",
    "cargar_grafo_desde_url",
    "cargar_o_descargar_grafo",
    "distancia_promedio_nodos",
    "leer_archivo_aristas",
    "guardar_resultados_en_duckdb"
]
