#collectors/descargador.py

import os
import io
import tempfile
import zipfile
import requests
import scipy.io
import networkx as nx
from urllib.parse import urlparse
from .utiles import leer_archivo_aristas

def cargar_grafo_desde_url(url: str) -> nx.Graph | None:
    """
    Descarga un archivo .zip que contiene un grafo, lo descomprime temporalmente
    y construye un objeto NetworkX Graph a partir de los archivos encontrados.

    Soporta archivos en formato `.mtx` (Matrix Market) o `.edges`.

    Args:
        url (str): URL directa al archivo .zip que contiene el grafo.

    Returns:
        nx.Graph | None: El grafo cargado si se pudo procesar correctamente.
        Retorna `None` si no se encontró un archivo compatible dentro del .zip.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(tmpdir)
        for root, _, files in os.walk(tmpdir):
            for f in files:
                path = os.path.join(root, f)
                if f.endswith('.mtx'):
                    A = scipy.io.mmread(path)
                    return nx.from_scipy_sparse_array(A)
                elif f.endswith('.edges'):
                    edges = leer_archivo_aristas(path)
                    G = nx.Graph()
                    G.add_edges_from(edges)
                    return G
    return None

def cargar_o_descargar_grafo(nombre: str, url: str, carpeta_destino: str = "grafos_guardados") -> nx.Graph:
    """
    Carga un grafo desde disco si ya está guardado. Si no, lo descarga desde la URL,
    lo guarda en disco y lo retorna.

    Args:
        nombre (str): Nombre del archivo para guardar el grafo.
        url (str): URL de donde descargar el grafo si no existe.
        carpeta_destino (str): Carpeta donde guardar/cargar los grafos.

    Returns:
        nx.Graph: El grafo cargado.
    """
    os.makedirs(carpeta_destino, exist_ok=True)
    ruta_grafo = os.path.join(carpeta_destino, f"{nombre}.gpickle")

    if os.path.exists(ruta_grafo):
        print(f"[INFO] Cargando grafo local: {ruta_grafo}")
        G = nx.read_gpickle(ruta_grafo)
    else:
        print(f"[INFO] Descargando grafo desde: {url}")
        G = cargar_grafo_desde_url(url)
        if G is None:
            raise RuntimeError(f"No se pudo descargar o procesar el grafo desde: {url}")
        nx.write_gpickle(G, ruta_grafo)
        print(f"[INFO] Grafo guardado localmente en: {ruta_grafo}")

    metadatos = {
        "nombre": nombre,
        "nodos": G.number_of_nodes(),
        "aristas": G.number_of_edges(),
        "dirigido": G.is_directed(),
        "archivo": ruta_grafo,
        "tamano_archivo_bytes": os.path.getsize(ruta_grafo)
    }

    return G, metadatos

def crear_zip_url(from_page_url: str, download_php_url: str):
    """
    Genera la URL directa a un archivo .zip a partir de la página de origen
    y la URL de descarga proporcionada por Network Repository (NR).

    Este método infiere la estructura de descarga típica de los datasets
    en NR, donde los archivos .zip están organizados según el nombre del
    script PHP y el nombre base del archivo.

    Args:
        from_page_url (str): URL de la página del dataset (por ejemplo, 'https://networkrepository.com/ca-GrQc.php').
        download_php_url (str): URL del enlace de descarga PHP (por ejemplo, 'https://networkrepository.com/download.php?file=ca-GrQc/ca-GrQc.edges').

    Returns:
        tuple[str, str]: Una tupla que contiene:
            - La URL directa al archivo .zip.
            - El nombre base del archivo (sin extensión).
    """
    parsed_download = urlparse(download_php_url)
    base_name = os.path.splitext(os.path.basename(parsed_download.path))[0]
    directory = from_page_url.split('/')[-1].replace('.php', '')
    zip_url = f"https://nrvis.com/download/data/{directory}/{base_name}.zip"
    return zip_url, base_name
