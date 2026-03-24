import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os, time, re

novel_url     = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()
start, end    = map(int, chapter_range.split("-"))
novel_slug    = novel_url.rstrip("/").split("/")[-1]
parsed        = urlparse(novel_url)
base_domain   = f"{parsed.scheme}://{parsed.netloc}"
os.makedirs("downloaded_files", exist_ok=True)

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

print("Fetching novel page...")
scraper.get(novel_url, timeout=25)


print("Fetching chapter list...")
ajax_url = f"{base_domain}/ajax/chapter-option?novelId={novel_slug}"
ajax_r   = scraper.get(ajax_url, headers={
    "X-Requested-With": "XMLHttpRequest",
    "Referer"         : novel_url,
}, timeout=25)

soup    = BeautifulSoup(ajax_r.text, "html.parser")
options = soup.find_all("option")
print(f"  Total chapters : {len(options)}")

if not options:
    print("  ✗ No chapters found — exiting")
    exit()

chapter_urls = {}
for opt in options:
    href  = opt.get("value", "")
    match = re.search(r"chapter-(\d+)", href, re.I)
    if match:
        num = int(match.group(1))
        chapter_urls[num] = href if href.startswith("http") else f"{base_domain}{href}"

in_range = {k: v for k, v in chapter_urls.items() if start <= k <= end}
print(f"  Chapters in range [{chapter_range}] : {len(in_range)}")

all_content     = ""
failed_chapters = []

for chapter_num in range(start, end + 1):
    url = in_range.get(chapter_num)
    print(f"\nScraping chapter {chapter_num}...")

    if not url:
        print(f"  ✗ URL not found")
        failed_chapters.append(chapter_num)
        continue

    try:
        soup = BeautifulSoup(scraper.get(url, timeout=25).text, "html.parser")

        novel_div = (
            soup.find("div", id="chr-content")     or
            soup.find("div", id="chapter-content") or
            soup.find("div", class_="chr-c")       or
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

            all_content += "\n" + "=" * 50 + "\n\n"
        else:
            print("  ✗ Content div not found!")
            failed_chapters.append(chapter_num)

    except Exception as e:
        print(f"  ✗ Error: {e}")
        failed_chapters.append(chapter_num)

    time.sleep(1)


filename = f"downloaded_files/{chapter_range} {novel_slug}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"\n✓ Saved to {filename}")
if failed_chapters:
    print(f"✗ Failed: {failed_chapters}")
