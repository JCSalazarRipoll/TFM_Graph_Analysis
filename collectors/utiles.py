# collectors/utiles.py

def leer_archivo_aristas(path: str):
    aristas = []
    with open(path, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) >= 2:
                try:
                    aristas.append((int(partes[0]), int(partes[1])))
                except ValueError:
                    continue
    return aristas
