from pathlib import Path

BASE_URL = "https://networkrepository.com"
OUTPUT_DIR = Path("grafos_descargados")
OUTPUT_DIR.mkdir(exist_ok=True)
DB_PATH = "grafo_db.duckdb"
