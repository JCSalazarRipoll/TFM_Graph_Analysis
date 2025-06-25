# main.py

from collectors import build_zip_url, cargar_grafo_desde_url, extraer_estadisticas_red

if __name__ == "__main__":
    graph_php_url = "https://networkrepository.com/insecta-ant-colony1-day01.php"
    download_php_url = "https://networkrepository.com/download.php?file=insecta-ant-colony1-day01"

    zip_url, name = build_zip_url(graph_php_url, download_php_url)
    print(f"[INFO] Descargando grafo: {name}")
    G = cargar_grafo_desde_url(zip_url)

    if G:
        print(f"[INFO] Grafo cargado con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas")
        stats = extraer_estadisticas_red(graph_php_url)
        print("[INFO] Estadísticas extraídas:")
        for key, value in stats.items():
            print(f" - {key}: {value}")
