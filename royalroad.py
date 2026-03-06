import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
import re

# Get user input
novel_url = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()

# Parse novel name from URL
novel_name = novel_url.split("/")[-1]

# Parse chapter range
start, end = map(int, chapter_range.split("-"))

# Create downloaded_files directory if it doesn't exist
os.makedirs("downloaded_files", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"  ✗ Error fetching {url}: {e}")
        return None

# Get all chapter URLs from the novel page
print("\nFetching chapter list...")
soup = fetch(novel_url)
all_chapter_urls = []

if soup:
    chapter_table = soup.find("table", id="chapters")
    if chapter_table:
        for row in chapter_table.find_all("tr", class_="chapter-row"):
            relative_url = row.get("data-url")
            if relative_url:
                all_chapter_urls.append(urljoin(novel_url, relative_url))

print(f"Found {len(all_chapter_urls)} chapters total")

# Filter by chapter number extracted from URL
filtered = []
for url in all_chapter_urls:
    match = re.search(r"/chapter-(\d+)", url)
    if match:
        num = int(match.group(1))
        if start <= num <= end:
            filtered.append((num, url))

filtered.sort(key=lambda x: x[0])
filtered = [url for num, url in filtered]
print(f"Scraping {len(filtered)} chapters in range {chapter_range}...")

# Scrape chapters
all_content = ""
for chapter_num, url in zip(range(start, end + 1), filtered):
    print(f"\nScraping chapter {chapter_num}...")

    try:
        soup = fetch(url)
        if not soup:
            continue

        novel_div = soup.find("div", class_="chapter-content")

        if novel_div:
            chapter_title = soup.find("h1") or soup.find("h2")
            if chapter_title:
                all_content += f"=== {chapter_title.text.strip()} ===\n\n"

            paragraphs = novel_div.find_all("p")
            print(f"  ✓ Extracted {len(paragraphs)} paragraphs")

            for p in paragraphs:
                text = p.text.strip()
                if text:
                    all_content += text + "\n\n"

            all_content += "\n" + "="*50 + "\n\n"
        else:
            print(f"  ✗ Div not found!")

        time.sleep(1)

    except Exception as e:
        print(f"  ✗ Error: {e}")

# Save to file
filename = f"downloaded_files/{chapter_range} {novel_name}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"✓ Saved to {filename}")