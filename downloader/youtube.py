from yt_dlp import YoutubeDL
from .utils import clean_query, get_track_path
from .get_progress import get_progress
import os
from time import sleep
import logging

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BATCH_SEARCH = 10

class DownloadProgressHook:
    """Progress hook for yt-dlp to show download progress"""
    def __init__(self, track_name,task_id=None):
        self.track_name = track_name
        self.started = False
        self.last_percent = 0
        self.task_id = task_id
        
    @property
    def progress(self):
        return get_progress()
    
    def __call__(self, d):
        status = d.get('status')
        if status == 'downloading':
            if not self.started:
                logger.info("Downloading: %s",self.track_name[:50])
                self.started = True
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes',0)
            if total:
                percent = int((downloaded/total) * 100)
                if percent >= self.last_percent + 1:
                    self.last_percent = percent
                    if self.progress and self.task_id is not None:
                        try:
                            self.progress.update(self.task_id,completed=percent,total=100)
                        except Exception:
                            pass
                    else:
                        logger.info("Progress: %d%%",percent)
        elif status == 'finished':
            logger.info("Converting to MP3...")
            if self.progress and self.task_id is not None:
                try:
                    self.progress.update(self.task_id,completed=100,total=100)
                except Exception:
                    pass

def download_track(track: str, artist: str, album: str,task_id=None):
    path = get_track_path(artist, album, track)
    
    if os.path.exists(path):
        logger.info("Skipping '%s' (already downloaded).", track)
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
        'progress_hooks': [DownloadProgressHook(track,task_id=task_id)],
    }
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Searching for '%s' (attempt %d)", track, attempt)
            with YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(search_url, download=False)
                entries = info.get('entries', [])
                
                if not entries:
                    logger.error("No results found, skipping.")
                    return
                
                video = entries[0]
                url = f"https://www.youtube.com/watch?v={video['id']}"
                title = video.get('title', 'Unknown')
                duration = video.get('duration', 0)
                
                logger.info("Found: %s (%ds)", title, duration)
                logger.info("Saving to: %s", os.path.basename(path))
                
                # Download the track
                ydl.download([url])
                logger.info("Successfully downloaded '%s'", track)
                break
                
        except Exception as e:
            logger.warning("Attempt %d failed: %s", attempt, e)
            sleep(2)
            if attempt == MAX_RETRIES:
                logger.error("Failed after %d attempts.", MAX_RETRIES)