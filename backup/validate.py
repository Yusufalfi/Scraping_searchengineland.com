# file ini untuk validasi setiap sitemap ada berapa url 
# https://searchengineland.com/post-sitemap.xml = This XML Sitemap contains 101 URLs.

import time
import httpx
import re

index_url = "https://searchengineland.com/sitemap_index.xml"

# Header agar skrip kamu terdeteksi sebagai browser asli
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

with httpx.Client(verify=False, follow_redirects=True, timeout=30.0) as client:
    res = client.get(index_url, headers=headers)
    
    sitemaps = re.findall(r'<sitemap>.*?<loc>(.*?)</loc>.*?<lastmod>(.*?)</lastmod>.*?</sitemap>', res.text, re.DOTALL)
    
    print("=== REKAP JUMLAH URL PER SITEMAP (2024-2026) ===\n")
    
    total_artikel_semua = 0
    
    for loc, lastmod in sitemaps:
        if "post-sitemap" in loc and any(year in lastmod for year in ["2024", "2025", "2026"]):
            try:
                # Jeda 1.5 detik setiap download sitemap baru agar tidak dianggap spam/bot
                time.sleep(1.5)
                
                sub_res = client.get(loc, headers=headers)
                
                # Cek jika terkena blokir Cloudflare / HTTP Error
                if sub_res.status_code != 200:
                    print(f"Sitemap: {loc} -> ERROR HTTP {sub_res.status_code} (Kena Blokir/Rate Limit)")
                    continue
                
                # Hitung tag <url> atau <loc> di dalam sitemap
                urls = re.findall(r'<loc>', sub_res.text)
                # Dikurangi 1 karena tag <loc> pertama milik image/stylesheet sitemap Yoast
                count_url = max(0, len(urls) - 1) if '<url>' in sub_res.text else len(urls)
                
                total_artikel_semua += count_url
                
                print(f"Sitemap: {loc}")
                print(f"Last Mod: {lastmod}")
                print(f"Jumlah: {count_url} URLs")
                print("-" * 50)
            except Exception as e:
                print(f"Error fetching {loc}: {e}")

    print(f"\nTOTAL SELURUH ARTIKEL (2024-2026): {total_artikel_semua}")