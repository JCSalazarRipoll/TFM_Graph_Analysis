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
