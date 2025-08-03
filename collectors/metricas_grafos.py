#collectors/metricas_grafos.py

import networkx as nx
import logging
import time

# Configurar el logging (puedes mover esto a un archivo común si lo usas en varios lugares)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def distancia_promedio_nodos(G: nx.Graph) -> float:
    """
    Calcula la distancia promedio entre todos los pares de nodos en un grafo.
    Si el grafo no está conectado, no calcula la distancia promedio
    """

    if G.number_of_nodes() < 2:
        return 0,0  

    if not nx.is_connected(G):
        raise ValueError("El grafo no es conexo. No se puede calcular la distancia promedio.")

    try:
        from networkx import average_shortest_path_length
        inicio = time.perf_counter()
        distancia = nx.average_shortest_path_length(G)
        fin = time.perf_counter()
        duracion = fin - inicio
        return distancia, duracion
    except Exception as e:
        logger.warning(f"Error al calcular la distancia promedio: {e}")
        return -1
