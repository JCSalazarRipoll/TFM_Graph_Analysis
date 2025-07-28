#collectors/parser.py

from .metricas_grafo import (
    extraer_estadisticas_red,
    estadisticas_completas,
)

from .metricas_grafos import distancia_promedio_nodos

from .descargador import (
    crear_zip_url,
    cargar_grafo_desde_url,
)

import pandas as pd

def extraer_datos_de_url(url_php: str, head_url: str) -> dict | None:
    """
    Extrae la información de un grafo desde una URL y devuelve un diccionario con sus métricas.
    Solo devuelve el diccionario si el grafo tiene las 14 métricas necesarias.
    """

    url_zip, nombre_base = crear_zip_url(head_url, url_php)
    print(f" Procesando: {nombre_base}")

    try:
        G = cargar_grafo_desde_url(url_zip)
        if G is None:
            print(f" No se pudo cargar el grafo desde ZIP: {url_zip}")
            return None

        estadisticas = extraer_estadisticas_red(url_php)

        if not estadisticas_completas(estadisticas):
            print(f" Grafo {nombre_base} ignorado: métricas incompletas")
            return None

        distancia_promedio = distancia_promedio_nodos(G)
        print(f" Grafo válido. Distancia promedio: {distancia_promedio:.4f}")

        datos_grafo = {
            'nombre': nombre_base,
            'nodos': estadisticas['Nodes'],
            'aristas': estadisticas['Edges'],
            'densidad': estadisticas['Density'],
            'grado_maximo': estadisticas['Maximum degree'],
            'grado_minimo': estadisticas['Minimum degree'],
            'grado_promedio': estadisticas['Average degree'],
            'asortatividad': estadisticas['Assortativity'],
            'numero_triangulos': estadisticas['Number of triangles'],
            'triangulos_promedio': estadisticas['Average number of triangles'],
            'triangulos_maximo': estadisticas['Maximum number of triangles'],
            'coeficiente_aglomeracion_promedio': estadisticas['Average clustering coefficient'],
            'proporcion_triangulos_promedio': estadisticas['Fraction of closed triangles'],
            'centro_k_maximo': estadisticas['Maximum k-core'],
            'estimacion_minima_clique_maxima': estadisticas['Lower bound of Maximum Clique'],
            'distancia_promedio': distancia_promedio
        }

        return datos_grafo

    except Exception as e:
        print(f" Error al procesar {url_php}: {e}")
        return None

def url_dataframe(urls_php: list, head_url: str) -> pd.DataFrame:
    """
    Procesa una lista de URLs individuales de grafos, extrae sus métricas
    y devuelve un DataFrame solo con los grafos válidos.
    """
    registros = []

    for url_php in urls_php:
        datos = extraer_datos_de_url(url_php, head_url)
        if datos:
            registros.append(datos)

    df = pd.DataFrame(registros)
    return df

