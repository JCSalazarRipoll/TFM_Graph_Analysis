#src/estimador_distancias

import networkx as nx
import random
import numpy as np

def estimar_distancia_grafo(G, sample_size=1000, bfs_sources=10):
    """
    Devuelve estimaciones de la distancia promedio entre nodos usando 3 métodos:
    - Método exacto si es posible (solo grafos pequeños y conexos)
    - Muestreo aleatorio de pares de nodos
    - BFS desde nodos aleatorios

    Args:
        G (networkx.Graph): grafo de entrada
        sample_size (int): número de pares aleatorios a muestrear
        bfs_sources (int): número de nodos desde los que hacer BFS

    Returns:
        dict: {'exact': float | None, 'random_pairs': float | None, 'bfs_sampling': float | None}
    """
    result = {}

    # 1. Exacto (solo para grafos pequeños y conexos)
    if nx.is_connected(G) and G.number_of_nodes() < 1000:
        try:
            result["exact"] = nx.average_shortest_path_length(G)
        except Exception:
            result["exact"] = None
    else:
        result["exact"] = None

    # 2. Muestreo de pares aleatorios
    nodes = list(G.nodes)
    distances = []
    for _ in range(sample_size):
        u, v = random.sample(nodes, 2)
        try:
            d = nx.shortest_path_length(G, u, v)
            distances.append(d)
        except nx.NetworkXNoPath:
            continue
    result["random_pairs"] = np.mean(distances) if distances else None

    # 3. BFS desde k nodos
    bfs_distances = []
    for source in random.sample(nodes, min(bfs_sources, len(nodes))):
        lengths = nx.single_source_shortest_path_length(G, source)
        bfs_distances.extend(lengths.values())
    result["bfs_sampling"] = np.mean(bfs_distances) if bfs_distances else None

    return result
