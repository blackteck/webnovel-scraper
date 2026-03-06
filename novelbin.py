import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time
import re

# Get user input
novel_url = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()

# Parse novel name and domain from URL
novel_name = novel_url.rstrip("/").split("/")[-1]
parsed = urlparse(novel_url)
base_domain = f"{parsed.scheme}://{parsed.netloc}"

# Parse chapter range
start, end = map(int, chapter_range.split("-"))

# Create downloaded_files directory if it doesn't exist
os.makedirs("downloaded_files", exist_ok=True)

# Initialize cloudscraper session
scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

def fetch(url):
    try:
        response = scraper.get(url, timeout=25)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"  ✗ Error fetching {url}: {e}")
        return None

# Get all chapter URLs from the novel page
print("\nFetching chapter list...")
soup = fetch(novel_url)
all_chapter_urls = {}

if soup:
    for a in soup.select("a[href*='chapter-']"):
        href = a.get("href", "")
        match = re.search(r"chapter-(\d+)", href, re.I)
        if match:
            num = int(match.group(1))
            if start <= num <= end:
                all_chapter_urls[num] = urljoin(base_domain, href)

print(f"Found {len(all_chapter_urls)} chapters in range {chapter_range}")

# Scrape chapters
all_content = ""
for chapter_num in range(start, end + 1):
    url = all_chapter_urls.get(chapter_num)
    print(f"\nScraping chapter {chapter_num}...")

    if not url:
        print(f"  ✗ URL not found for chapter {chapter_num}")
        continue

    try:
        soup = fetch(url)
        if not soup:
            continue

        novel_div = (
            soup.find("div", id="chr-content") or
            soup.find("div", class_="chr-c") or
            soup.find("div", id="chapter-content") or
            soup.find("div", class_="chapter-content")
        )

        if novel_div:
            chapter_title = soup.find("h2") or soup.find("h1")
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