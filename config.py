# config.py
import os
from pathlib import Path

# Ruta absoluta (La más segura si no mueves la carpeta Proyectos)
BASE_PATH = Path("/Users/mariaclara/Desktop/Proyectos/CONSOLAS_PROMO")

# Si quieres que sea automática buscando la carpeta "Proyectos" 
# un nivel arriba de donde está el código:
# BASE_PATH = Path(__file__).parent.parent / "Proyectos" / "CONSOLAS_SAAS"

# Estas son las "consolas" o carpetas de trabajo
CONSOLAS = [
   "BeatlesInLondon","Pontisultamigi","Lechiesedilondra",
    "Londonchurch","Goticoreligiosopuglia","Pontisultamigi_Mail","BristolParty(B2B)"
]

# Dentro de cada consola creamos estas carpetas
SUBFOLDERS = [
    "ENTRADA_DIR",      # aquí entran los CSV
    "BBDD_DIR",         # base de datos SQLite
    "LOGS_DIR",         # archivos de registro
    "HARD_DOMINIO_DIR", # exportación de errores graves
    "INTERNAL_DIR",     # emails internos
    "PROCESSED_DIR",    # archivos ya procesados
    "ERROR_DIR"         # archivos con errores
]

# Tamaño de lectura de archivos grandes (para no saturar memoria)
CHUNK_SIZE = 100_000

# Columnas obligatorias que debe tener cada CSV
EXPECTED_COLUMNS = ['Email', 'Bounce type', 'Message', 'Date added']