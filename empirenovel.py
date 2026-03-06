from seleniumbase import Driver
from bs4 import BeautifulSoup
import os
import time

# Get user input
novel_url = input("Enter novel URL : ").strip()
chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()

# Parse novel name from URL
novel_name = novel_url.split("/")[-1]

# Parse chapter range
start, end = map(int, chapter_range.split("-"))

# Create downloaded_files directory if it doesn't exist
os.makedirs("downloaded_files", exist_ok=True)

# Initialize driver
print("Starting browser...")
driver = Driver(uc=True, headless=True)

# Scrape chapters
all_content = ""
for chapter_num in range(start, end + 1):
    url = f"{novel_url}/{chapter_num}"
    print(f"\nScraping chapter {chapter_num}...")
    
    try:
        start_time = time.time()
        driver.get(url)
        
        # Wait for content to load (up to 15 seconds)
        driver.wait_for_element("div#read-novel", timeout=15)
        load_time = time.time() - start_time
        
        print(f"  ⏱  Page loaded in {load_time:.2f}s")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
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
            
            all_content += "\n" + "="*50 + "\n\n"
        else:
            print(f"  ✗ Div not found!")
    except Exception as e:
        print(f"  ✗ Error: {e}")

driver.quit()

# Save to file
filename = f"downloaded_files/{chapter_range} {novel_name}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"✓ Saved to {filename}")