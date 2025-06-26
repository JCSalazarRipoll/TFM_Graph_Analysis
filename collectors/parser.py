from collectors.metrics_extractor import (
    extraer_estadisticas_red,
    estadisticas_completas,
    mean_node_distance,
)

from collectors.downloader import (
    build_zip_url,
    cargar_grafo_desde_url,
)

import pandas as pd

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


def extraer_datos_de_url(url_php: str, head_url: str) -> dict | None:
    """
    Extrae la información de un grafo desde una URL y devuelve un diccionario con sus métricas.
    Solo devuelve el diccionario si el grafo tiene las 14 métricas necesarias.
    """

    url_zip, nombre_base = build_zip_url(head_url, url_php)
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

        avg_shortest_path_length = mean_node_distance(G)
        print(f" Grafo válido. Distancia promedio: {avg_shortest_path_length:.4f}")

        datos_grafo = {
            'name': nombre_base,
            'nodes': estadisticas['Nodes'],
            'edges': estadisticas['Edges'],
            'density': estadisticas['Density'],
            'maximum_degree': estadisticas['Maximum degree'],
            'minimum_degree': estadisticas['Minimum degree'],
            'average_degree': estadisticas['Average degree'],
            'assortativity': estadisticas['Assortativity'],
            'number_of_triangles': estadisticas['Number of triangles'],
            'average_number_of_triangles': estadisticas['Average number of triangles'],
            'maximum_number_of_triangles': estadisticas['Maximum number of triangles'],
            'average_clustering_coefficient': estadisticas['Average clustering coefficient'],
            'fraction_of_closed_triangles': estadisticas['Fraction of closed triangles'],
            'maximum_k-core': estadisticas['Maximum k-core'],
            'lower_bound_of_maximum_clique': estadisticas['Lower bound of Maximum Clique'],
            'avg_node_dis': avg_shortest_path_length
        }

        return datos_grafo

    except Exception as e:
        print(f" Error al procesar {url_php}: {e}")
        return None


def leer_archivo_edges(path: str):
    edges = []
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    edges.append((int(parts[0]), int(parts[1])))
                except ValueError:
                    continue
    return edges
