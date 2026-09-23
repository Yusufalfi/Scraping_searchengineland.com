import os
import json
from bs4 import BeautifulSoup
from datetime import datetime
from config import SITEMAP_INDEX_URL, CACHE_DIR, TARGET_YEARS, CUTOFF_DATE, JSON_RESULT_FILE
from fetcher import fetch_url

def get_target_sitemaps() -> list[str]:
    """Membaca sitemap index utama dan mengambil URL sub-sitemap relevan."""
    print("=== STEP 1: MEMBACA SITEMAP INDEX ===")
    index_html = fetch_url(SITEMAP_INDEX_URL)
    if not index_html:
        print("Gagal membaca sitemap index.")
        return []

    soup = BeautifulSoup(index_html, "xml")
    target_sitemaps = []

    for sm in soup.find_all("sitemap"):
        loc = sm.find("loc").get_text().strip() if sm.find("loc") else ""
        lastmod = sm.find("lastmod").get_text().strip() if sm.find("lastmod") else ""

        if "post-sitemap" in loc and any(yr in lastmod for yr in TARGET_YEARS):
            target_sitemaps.append(loc)

    print(f"Ditemukan {len(target_sitemaps)} sitemap relevan ({', '.join(TARGET_YEARS)}).\n")
    return target_sitemaps

def download_sitemaps(target_sitemaps: list[str]):
    """Mengunduh dan menyimpan file XML sitemap ke folder cache lokal."""
    print("=== STEP 2: DOWNLOAD FILE XML KE CACHE LOKAL ===")
    for idx, loc_url in enumerate(target_sitemaps, start=1):
        filename = os.path.basename(loc_url)
        local_path = os.path.join(CACHE_DIR, filename)

        if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            print(f"[{idx}/{len(target_sitemaps)}] [CACHED] {filename}")
            continue

        print(f"[{idx}/{len(target_sitemaps)}] Downloading: {filename} ...")
        xml_content = fetch_url(loc_url)

        if xml_content and "<urlset" in xml_content:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"  ↳ Tersimpan di {local_path}")
        else:
            print(f"  X Gagal mengunduh {filename}.")

def extract_valid_articles() -> list[dict]:
    """Membaca file XML cache dan menyaring artikel >= 2024."""
    print("\n=== STEP 3: EKSTRAKSI ARTIKEL DARI CACHE LOKAL ===")
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

    # Deduplikasi
    unique_articles = list({a["url"]: a for a in all_articles}.values())

    with open(JSON_RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_articles, f, indent=4)

    print(f"Total {len(unique_articles)} artikel unik disimpan ke '{JSON_RESULT_FILE}'")
    return unique_articles