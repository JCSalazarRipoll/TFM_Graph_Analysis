#collectors/metricas_grafos.py

import networkx as nx

def distancia_promedio_nodos(G: nx.Graph) -> float:
    """
    Calcula la distancia promedio entre todos los pares de nodos en un grafo.
    Si el grafo no está conectado, calcula la media sobre el componente gigante.
    """

    #Grafo de 0 o 1 nodo
    if G.number_of_nodes() < 2:
        return 0  
    
    if not nx.is_connected(G):
        # Tomar el componente conexo más grande
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

    try:
        return nx.average_shortest_path_length(G)
    except Exception as e:
        print(f"Error al calcular la distancia promedio: {e}")
        return -1
