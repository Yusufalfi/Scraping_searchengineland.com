import time
import random
import cloudscraper
from config import MAX_RETRIES, MIN_DELAY, MAX_DELAY

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

def fetch_url(url: str, max_retries: int = MAX_RETRIES) -> str | None:
    """Fetch URL menggunakan Cloudscraper dengan Exponential Backoff & Random Delay."""
    for attempt in range(1, max_retries + 1):
        try:
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code in [403, 429, 503]:
                wait_time = attempt * 5 + random.uniform(2, 4)
                print(f"Limit/Block ({response.status_code}). Waiting {wait_time:.1f}s (Try {attempt}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"HTTP Status {response.status_code} on {url}")
        except Exception as e:
            wait_time = attempt * 3
            print(f"Network Error: {e}. Retry {attempt}/{max_retries}...")
            time.sleep(wait_time)
            
    return None