from seleniumbase import Driver
from bs4 import BeautifulSoup
import os
import time

novel_url = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()

novel_id = novel_url.split("/")[-1].split("-")[0]
start, end = map(int, chapter_range.split("-"))
os.makedirs("downloaded_files", exist_ok=True)

print("Starting browser...")
driver = Driver(uc=True, headless=True, page_load_strategy="none")  

print("Fetching first chapter URL...")
driver.get(f"https://ranobes.top/chapters/{novel_id}/first")
time.sleep(3)
first_chapter_url = driver.current_url

base_url = first_chapter_url.rsplit("/", 1)[0]
first_id = int(first_chapter_url.rsplit("/", 1)[1].replace(".html", ""))
novel_name = base_url.split("/")[-1]

print(f"Base URL : {base_url}")
print(f"First chapter ID : {first_id}")

all_content = ""
for chapter_num in range(start, end + 1):
    chapter_id = first_id + (chapter_num - 1)
    url = f"{base_url}/{chapter_id}.html"
    print(f"\nScraping chapter {chapter_num}...")
    
    try:
        start_time = time.time()
        driver = Driver(uc=True, headless=True, page_load_strategy="none")
        driver.get(url)
        driver.wait_for_element("div#arrticle", timeout=15)
        load_time = time.time() - start_time

        print(f"  ⏱  Page loaded in {load_time:.2f}s")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        novel_div = soup.find("div", id="arrticle")

        if novel_div:
            chapter_title = soup.find("h1", class_="h4 title")
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
    except Exception as e:
        print(f"  ✗ Error: {e}")

driver.quit()

filename = f"downloaded_files/{chapter_range} {novel_name}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"✓ Saved to {filename}")



