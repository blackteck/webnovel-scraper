from seleniumbase import Driver
from bs4 import BeautifulSoup
import os, time

novel_url     = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()
novel_name    = novel_url.split("/")[-1]
start, end    = map(int, chapter_range.split("-"))
os.makedirs("downloaded_files", exist_ok=True)

def create_driver():
    return Driver(uc=True, headless=True)

def is_driver_alive(driver):
    try:
        _ = driver.current_url  
        return True
    except:
        return False

print("Starting browser...")
driver = Driver(uc=True, headless=True)

all_content     = ""
failed_chapters = []

for chapter_num in range(start, end + 1):
    url = f"{novel_url}/{chapter_num}"
    print(f"\nScraping chapter {chapter_num}...")

    retries = 3
    success = False

    for attempt in range(retries):
        try:
            
            if not is_driver_alive(driver):
                print(f"  ⚠ Browser crashed — restarting...")
                try:
                    driver.quit()
                except:
                    pass
                time.sleep(2)
                driver = create_driver()
                print(f"  ✓ Browser restarted")

            start_time = time.time()
            driver.get(url)
            driver.wait_for_element("div#read-novel", timeout=15)
            load_time = time.time() - start_time
            print(f"  ⏱  Page loaded in {load_time:.2f}s")

            soup      = BeautifulSoup(driver.page_source, "html.parser")
            novel_div = soup.find("div", id="read-novel")

            if novel_div:
                chapter_title = novel_div.find("h3")
                if chapter_title:
                    all_content += f"=== {chapter_title.text.strip()} ===\n\n"

                paragraphs = novel_div.find_all("p")
                print(f"  ✓ Extracted {len(paragraphs)} paragraphs")

                for p in paragraphs:
                    text = p.text.strip()
                    if text:
                        all_content += text + "\n\n"

                all_content += "\n" + "=" * 50 + "\n\n"
                success = True
                break  

            else:
                print(f"  ✗ Div not found on attempt {attempt + 1}")

        except Exception as e:
            print(f"  ✗ Attempt {attempt + 1} failed: {e}")

        if not success and attempt < retries - 1:
            wait = 5 * (attempt + 1)  # 5s, 10s, 15s
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)

    if not success:
        print(f"  ✗ Chapter {chapter_num} skipped after {retries} attempts.")
        failed_chapters.append(chapter_num)


try:
    driver.quit()
except:
    pass

filename = f"downloaded_files/{chapter_range} {novel_name}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"\n✓ Saved to {filename}")
if failed_chapters:
    print(f"✗ Failed chapters : {failed_chapters}")
