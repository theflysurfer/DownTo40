"""
Configuration centralisée pour les APIs d'énergie française
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Période d'analyse
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

# Seuil de prix pour l'analyse
PRICE_THRESHOLD = 40  # €/MWh

# Configuration ODRE (Open Data Réseaux Énergies)
ODRE_BASE_URL = "https://odre.opendatasoft.com/api/explore/v2.1"
ODRE_DATASETS = {
    "eco2mix_national": "eco2mix-national-cons-def",  # Données nationales consolidées
    "eco2mix_regional": "eco2mix-regional-cons-def",  # Données régionales consolidées
}

# Configuration ENTSO-E
ENTSOE_API_TOKEN = os.getenv("ENTSOE_API_TOKEN", "")
ENTSOE_BASE_URL = "https://web-api.tp.entsoe.eu/api"

# Codes EIC pour les pays frontaliers (ENTSO-E)
EIC_CODES = {
    "FR": "10YFR-RTE------C",  # France
    "DE": "10Y1001A1001A83F",  # Allemagne
    "BE": "10YBE----------2",  # Belgique
    "CH": "10YCH-SWISSGRIDZ",  # Suisse
    "IT": "10YIT-GRTN-----B",  # Italie
    "ES": "10YES-REE------0",  # Espagne
    "GB": "10YGB----------A",  # Grande-Bretagne
}

# Configuration RTE Data Portal (OAuth2)
RTE_CLIENT_ID = os.getenv("RTE_CLIENT_ID", "")
RTE_CLIENT_SECRET = os.getenv("RTE_CLIENT_SECRET", "")
RTE_BASE_URL = "https://digital.iservices.rte-france.com"
RTE_TOKEN_URL = f"{RTE_BASE_URL}/token/oauth/"
RTE_API_URL = f"{RTE_BASE_URL}/open_api/wholesale_market/v2"

# Chemins de sauvegarde des données
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"
RESULTS_DIR = "results"

# Paramètres de requêtes
REQUEST_TIMEOUT = 30  # secondes
MAX_RETRIES = 3
RETRY_DELAY = 5  # secondes
