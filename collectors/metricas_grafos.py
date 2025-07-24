#collectors/metricas_grafos.py

import networkx as nx
import logging

# Configurar el logging (puedes mover esto a un archivo común si lo usas en varios lugares)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def distancia_promedio_nodos(G: nx.Graph) -> float:
    """
    Calcula la distancia promedio entre todos los pares de nodos en un grafo.
    Si el grafo no está conectado, calcula la media sobre el componente gigante.
    """

    if G.number_of_nodes() < 2:
        return 0  

    if not nx.is_connected(G):
        # Tomar el componente conexo más grande
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

    try:
        return nx.average_shortest_path_length(G)
    except Exception as e:
        logger.warning(f"Error al calcular la distancia promedio: {e}")
        return -1
