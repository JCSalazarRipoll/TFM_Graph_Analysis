import requests
import re
from bs4 import BeautifulSoup

def estadisticas_completas(estadisticas: dict) -> bool:
    """
    Verifica si las estadísticas del grafo tienen exactamente las 14 métricas esperadas.
    """
    METRICAS_ESPERADAS = [
        "Nodes", "Edges", "Density", "Maximum degree", "Minimum degree",
        "Average degree", "Assortativity", "Number of triangles",
        "Average number of triangles", "Maximum number of triangles",
        "Average clustering coefficient", "Fraction of closed triangles",
        "Maximum k-core", "Lower bound of Maximum Clique"
    ]
    return all(m in estadisticas for m in METRICAS_ESPERADAS)


def extraer_estadisticas_red(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Esto lanza HTTPError si el código no es 200

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    stats_text = text[text.find("Network Data Statistics"):text.find("Network Data Statistics")+1000]

    patrones = {
        "Nodes": r"Nodes\s+([0-9\.KM]+)",
        "Edges": r"Edges\s+([0-9\.KM]+)",
        "Density": r"Density\s+([0-9\.]+)",
        "Maximum degree": r"Maximum degree\s+([0-9\.K]+)",
        "Minimum degree": r"Minimum degree\s+([0-9]+)",
        "Average degree": r"Average degree\s+([0-9\.]+)",
        "Assortativity": r"Assortativity\s+([\-0-9\.]+)",
        "Number of triangles": r"Number of triangles\s+([0-9\.KM]+)",
        "Average number of triangles": r"Average number of triangles\s+([0-9\.]+)",
        "Maximum number of triangles": r"Maximum number of triangles\s+([0-9\.KM]+)",
        "Average clustering coefficient": r"Average clustering coefficient\s+([0-9\.]+)",
        "Fraction of closed triangles": r"Fraction of closed triangles\s+([0-9\.]+)",
        "Maximum k-core": r"Maximum k-core\s+([0-9]+)",
        "Lower bound of Maximum Clique": r"Lower bound of Maximum Clique\s+([0-9]+)"
    }

    return {k: re.search(v, stats_text).group(1) for k, v in patrones.items() if re.search(v, stats_text)}
