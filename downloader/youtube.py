from yt_dlp import YoutubeDL
from .utils import clean_query, get_track_path
import os
from time import sleep

MAX_RETRIES = 3
BATCH_SEARCH = 10

class DownloadProgressHook:
    """Progress hook for yt-dlp to show download progress"""
    def __init__(self, track_name):
        self.track_name = track_name
        self.started = False
        self.last_percent = 0
    
    def __call__(self, d):
        if d['status'] == 'downloading':
            if not self.started:
                print(f"  [INFO] Downloading: {self.track_name[:50]}")
                self.started = True
            if 'total_bytes' in d or 'total_bytes_estimate' in d:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int((downloaded / total) * 100)
                    if percent >= self.last_percent + 10:
                        print(f"     Progress: {percent}%")
                        self.last_percent = percent
        elif d['status'] == 'finished':
            print(f"  [INFO] Converting to MP3...")

def download_track(track: str, artist: str, album: str):
    path = get_track_path(artist, album, track)
    
    if os.path.exists(path):
        print(f"Skipping '{track}' (already downloaded).")
        return
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    query = clean_query(track, artist)
    search_url = f"ytsearch{BATCH_SEARCH}:{query}"
    
    YDL_OPTS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': path.replace('.mp3', ''),
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'progress_hooks': [DownloadProgressHook(track)],
    }
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[INFO] Searching for '{track}' (attempt {attempt})")
            with YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(search_url, download=False)
                entries = info.get('entries', [])
                
                if not entries:
                    print(f"  [ERROR] No results found, skipping.\n")
                    return
                
                video = entries[0]
                url = f"https://www.youtube.com/watch?v={video['id']}"
                title = video.get('title', 'Unknown')
                duration = video.get('duration', 0)
                
                print(f"  [SUCCESS] Found: {title} ({duration}s)")
                print(f"  [INFO] Saving to: {os.path.basename(path)}")
                
                # Download the track
                ydl.download([url])
                print(f"[SUCCESS] Successfully downloaded '{track}'\n")
                break
                
        except Exception as e:
            print(f"  [WARN]  Attempt {attempt} failed: {e}")
            sleep(2)
            if attempt == MAX_RETRIES:
                print(f"  [FATAL] Failed after {MAX_RETRIES} attempts.\n")