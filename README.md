# 📚 Novel Scraper Collection

A fun side project for novel enthusiasts who want to read their favorite web novels offline!
Just run main.py, paste your novel URL, enter a chapter range, and your chapters are saved
to a .txt file automatically.


## 🚀 Quick Start

pip install seleniumbase beautifulsoup4 requests cloudscraper lxml

python main.py

- Enter novel URL      →  paste the main novel page URL
- Enter chapter range  →  e.g. 1-10 or 1-500 for the entire novel

download single chapter to an entire novel in one go.
For very large novels, download in batches (1-100, 101-200) to avoid long uninterrupted runs.

## 🌐 Supported Sites

 Ranobes.top 
 Royal Road 
 NovelBin 
 EmpireNovel

## 💡 What To Do With Your Downloaded File

- 🎧 Audiobook — convert with Balabolka (Windows), say command (Mac), or TTSMaker.com
- 📖 Kindle — convert to EPUB/MOBI with Calibre and send to your device
- 📱 Phone — open in Moon+ Reader or FBReader for offline reading
- 🌍 Translate — use DeepL or deep-translator Python library
- 🤖 AI Chat — load into Claude or NotebookLM and ask questions about the story
- 🖨️ Print — format in Word, add a cover, print and bind at a local shop


## 📁 Output

Saved to downloaded_files/{chapter_range} {novel_name}.txt


## 🗂️ Project Structure

project/
├── main.py               # Auto-detects site and runs the right scraper
├── empirenovel.py        
├── ranobes.py            
├── royalroad.py          
├── novelbin.py           
├── README.md             
└── downloaded_files/     # Output directory (auto-created)


## ⚖️ Disclaimer
This project is for personal offline reading only.
Please support the original authors and translators by
visiting the websites and do not redistribute downloaded content.

