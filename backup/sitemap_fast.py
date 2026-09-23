import os
import json
import time
import random
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = "sitemaps_cache"
SITEMAP_INDEX_URL = "https://searchengineland.com/sitemap_index.xml"
CUTOFF_DATE = datetime(2024, 1, 1)

os.makedirs(CACHE_DIR, exist_ok=True)

# Gunakan cloudscraper untuk memintas proteksi JS Challenge dari Cloudflare
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

def fetch_with_retry(url: str, max_retries: int = 5) -> str | None:
    """Fetch URL menggunakan Cloudscraper dengan delay acak dan Exponential Backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            # Jeda acak 1.5 - 3.5 detik agar pola lalu lintas mirip manusia
            time.sleep(random.uniform(1.5, 3.5))
            
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code in [403, 429, 503]:
                wait_time = attempt * 5 + random.uniform(2, 4)
                print(f"  ⚠️ Limit/Block terdeteksi ({response.status_code}). Menunggu {wait_time:.1f}s (Coba {attempt}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"  ⚠️ HTTP Status {response.status_code} pada {url}")
        except Exception as e:
            wait_time = attempt * 3
            print(f"  ⚠️ Network Error: {e}. Retry {attempt}/{max_retries}...")
            time.sleep(wait_time)
            
    return None

def main():
    print("=== STEP 1: MEMBACA SITEMAP INDEX ===")
    index_html = fetch_with_retry(SITEMAP_INDEX_URL)
    
    if not index_html:
        print("❌ Gagal membaca sitemap index. Coba gunakan koneksi internet lain (misal: Mobile Hotspot).")
        return

    soup = BeautifulSoup(index_html, "xml")
    target_sitemaps = []
    
    for sm in soup.find_all("sitemap"):
        loc = sm.find("loc").get_text().strip() if sm.find("loc") else ""
        lastmod = sm.find("lastmod").get_text().strip() if sm.find("lastmod") else ""
        
        # Filter hanya sitemap yang mengandung artikel tahun 2024, 2025, atau 2026
        if "post-sitemap" in loc and any(yr in lastmod for yr in ["2024", "2025", "2026"]):
            target_sitemaps.append(loc)
            
    print(f"✅ Ditemukan {len(target_sitemaps)} sitemap relevan (2024-2026).\n")

    print("=== STEP 2: DOWNLOAD FILE XML KE CACHE LOKAL ===")
    for idx, loc_url in enumerate(target_sitemaps, start=1):
        filename = os.path.basename(loc_url)
        local_path = os.path.join(CACHE_DIR, filename)

        # Jika file XML sudah terdownload sebelumnya, lewati
        if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            print(f"[{idx}/{len(target_sitemaps)}] [CACHED] {filename}")
            continue

        print(f"[{idx}/{len(target_sitemaps)}] Downloading: {filename} ...")
        xml_content = fetch_with_retry(loc_url)
        
        if xml_content and "<urlset" in xml_content:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"  ↳ Tersimpan di {local_path}")
        else:
            print(f"  ❌ Gagal mengunduh {filename}. Akan dilompati ke sitemap berikutnya.")

    print("\n=== STEP 3: EKSTRAKSI ARTIKEL DARI FILE LOKAL ===")
    all_articles = []
    
    for filename in sorted(os.listdir(CACHE_DIR)):
        if not filename.endswith(".xml"):
            continue
            
        filepath = os.path.join(CACHE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            sub_soup = BeautifulSoup(f.read(), "xml")
            
        count = 0
        for u in sub_soup.find_all("url"):
            loc = u.find("loc")
            lastmod = u.find(["lastmod", "publication_date"])
            
            if loc:
                url_str = loc.get_text().strip()
                date_str = lastmod.get_text().strip() if lastmod else ""
                
                if date_str:
                    clean_date = date_str.split("T")[0].split()[0]
                    try:
                        if datetime.strptime(clean_date, "%Y-%m-%d") >= CUTOFF_DATE:
                            all_articles.append({"url": url_str, "published_date": clean_date})
                            count += 1
                    except ValueError:
                        continue
        print(f"Parsed {filename}: {count} artikel valid (>= 2024)")

    # Eliminasi URL duplikat
    unique_articles = list({a["url"]: a for a in all_articles}.values())
    
    output_file = "articles_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_articles, f, indent=4)

    print(f"\n==========================================")
    print(f"✨ SELESAI! Total {len(unique_articles)} artikel berhasil dihimpun ke '{output_file}'")
    print(f"==========================================")

if __name__ == "__main__":
    main()