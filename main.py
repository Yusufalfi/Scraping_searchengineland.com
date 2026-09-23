from sitemap_parser import get_target_sitemaps, download_sitemaps, extract_valid_articles

def main():
    print("==========================================")
    print("STARTING SEARCH ENGINE LAND SCRAPER")
    print("==========================================\n")

    # Step 1: Ambil daftar sitemap target
    target_sitemaps = get_target_sitemaps()
    if not target_sitemaps:
        return

    # Step 2: Download & Cache XML
    download_sitemaps(target_sitemaps)

    # Step 3: Parse Artikel & Filter Tanggal
    articles = extract_valid_articles()

    print("\n==========================================")
    print("PROSES SITEMAP & DISCOVERY SELESAI!")
    print("==========================================")

if __name__ == "__main__":
    main()