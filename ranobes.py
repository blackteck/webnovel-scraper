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

try:
    print("Fetching first chapter URL...")
    driver.get(f"https://ranobes.top/chapters/{novel_id}/first")
    driver.wait_for_element("div#arrticle", timeout=15)  
    first_chapter_url = driver.current_url

    base_url = first_chapter_url.rsplit("/", 1)[0]
    first_id = int(first_chapter_url.rsplit("/", 1)[1].replace(".html", ""))
    novel_name = base_url.split("/")[-1]

    print(f"Base URL     : {base_url}")
    print(f"First chap ID: {first_id}")

    all_content = ""
    failed_chapters = []

    for chapter_num in range(start, end + 1):
        chapter_id = first_id + (chapter_num - 1)
        url = f"{base_url}/{chapter_id}.html"
        print(f"\nScraping chapter {chapter_num}...")

        retries = 3
        for attempt in range(retries):
            try:
                start_time = time.time()

                
                driver.get(url)
                driver.wait_for_element("div#arrticle", timeout=15)
                load_time = time.time() - start_time
                print(f"  ⏱  Loaded in {load_time:.2f}s")

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

                    all_content += "\n" + "=" * 50 + "\n\n"
                else:
                    print("  ✗ Content div not found!")

                break  

            except Exception as e:
                print(f"  ✗ Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    print("  Retrying in 5s...")
                    time.sleep(5)
                else:
                    print(f"  ✗ Chapter {chapter_num} skipped after {retries} attempts.")
                    failed_chapters.append(chapter_num)

finally:
    driver.quit()  

filename = f"downloaded_files/{chapter_range} {novel_name}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"\n✓ Saved to {filename}")
if failed_chapters:
    print(f"✗ Failed chapters: {failed_chapters}")

