import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    user_data_dir = os.path.join(os.getcwd(), "playwright_user_data")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        url = "https://searchengineland.com/post-sitemap299.xml"
        print(f"Membuka {url}...")
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(4)
        
        content = await page.content()
        
        # Simpan isi mentah ke file teks
        with open("sitemap_debug.txt", "w", encoding="utf-8") as f:
            f.write(content)
            
        print(" Selesai! Isi halaman berhasil disimpan ke 'sitemap_debug.txt'")
        await context.close()

asyncio.run(main())