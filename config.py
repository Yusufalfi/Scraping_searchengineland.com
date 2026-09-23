import os
from datetime import datetime

# URL & Cutoff
SITEMAP_INDEX_URL = "https://searchengineland.com/sitemap_index.xml"
CUTOFF_DATE = datetime(2024, 1, 1)
TARGET_YEARS = ["2024", "2025", "2026"]

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "sitemaps_cache")
OUTPUT_DIR = os.path.join(BASE_DIR, "word_outputs")
JSON_RESULT_FILE = os.path.join(BASE_DIR, "articles_result.json")

# Ensure Directories Exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Scraper Settings
MAX_RETRIES = 5
MIN_DELAY = 1.5
MAX_DELAY = 3.5