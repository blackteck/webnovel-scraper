import subprocess
import sys

def get_script(url):
    if "ranobes.top" in url:
        return "ranobes.py"
    elif "royalroad.com" in url:
        return "royalroad.py"
    elif "novelbin" in url:
        return "novelbin.py"
    elif "empirenovel" in url:
        return "empirenovel.py"
    else:
        return None

def main():
    print("=" * 50)
    print("         📚 Novel Scraper")
    print("=" * 50)

    novel_url     = input("Enter novel URL : ").strip()
    chapter_range = input("Enter chapter range (e.g., 1-5): ").strip()

    script = get_script(novel_url)

    if not script:
        print("\n✗ Unsupported website.")
        print("Supported: empirenovel, ranobes.top, royalroad.com, novelbin")
        sys.exit(1)

    print(f"\n✓ Detected → running {script}\n")
    print("=" * 50)

    # Pass inputs to the selected script via stdin
    subprocess.run(
        [sys.executable, script],
        input=f"{novel_url}\n{chapter_range}\n",
        text=True
    )

if __name__ == "__main__":
    main()