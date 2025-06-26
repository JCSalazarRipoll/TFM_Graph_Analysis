#collectors/downloader.py

import os
import io
import tempfile
import zipfile
import requests
import scipy.io
import networkx as nx
from .utils import leer_archivo_edges

def build_zip_url(from_page_url: str, download_php_url: str):
    from urllib.parse import urlparse
    parsed_download = urlparse(download_php_url)
    base_name = os.path.splitext(os.path.basename(parsed_download.path))[0]
    directory = from_page_url.split('/')[-1].replace('.php', '')
    zip_url = f"https://nrvis.com/download/data/{directory}/{base_name}.zip"
    return zip_url, base_name

def cargar_grafo_desde_url(url: str) -> nx.Graph | None:
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
                    edges = leer_archivo_edges(path)
                    G = nx.Graph()
                    G.add_edges_from(edges)
                    return G
    return None
