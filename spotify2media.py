import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp
import re

# Config
OUT_DIR = "downloads"
os.makedirs(OUT_DIR,exist_ok=True)

MAX_WORKERS = 4
SLEEP_BETWEEN_TRACK = 0.5
BATCH_SEARCH = 20

# csv input
csv_path = input("Enter path to Spotify CSV file: ").strip()

if not csv_path or not os.path.isfile(csv_path):
    print("File not found or invalid path. Exiting.")
    exit(1)

print(f"Selected file: {csv_path}")

# yt-dlp download func
def download_audio(url,outdir):
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def clean_query(track,artist):
    # Rem special characters and spaces
    track_clean = re.sub(r'[^\w\s]','',track).strip()
    artist_clean = re.sub(r'[^\w\s]','',artist).strip()

    return f"{track_clean} - {artist_clean} official audio"

# Process a single track
def process_track(row,index):
    track_name = row["Track Name"]
    artists = row["Artist Name(s)"]
    query = clean_query(row["Track Name"], row["Artist Name(s)"])
    print(f"[{index}] Searching YouTube for: {query}")

    try:
        ydl_opts = {"quiet": True, "extract_flat": "in_playlist"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{BATCH_SEARCH}: {query}",download=False)
            entries = info.get("entries",[])
            if not entries:
                print(f"   No results for '{query}', skipping.")

            url = f"https://www.youtube.com/watch?v={entries[0]['id']}"
            title = entries[0]["title"]
            print(f"   Found: {title} -> {url}")

            download_audio(url,OUT_DIR)
            
    except Exception as e:
        print(f"  Error processing '{query}': {e}")

# Read CSV and run
with open(csv_path,newline='',encoding='utf-8') as f:
    reader = list(csv.DictReader(f))
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_track,row,i+1): i+1 for i,row in enumerate(reader)}
        for future in as_completed(futures):
            try:
                future.result()
            except KeyboardInterrupt:
                print("\nDownload canceled by user.")
                executor.shutdown(wait=False)
                break