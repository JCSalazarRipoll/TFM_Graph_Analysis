import requests
import re
from bs4 import BeautifulSoup

def extraer_estadisticas_red(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
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
