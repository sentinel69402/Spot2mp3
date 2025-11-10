import os
import re

BASE_DIR = os.path.join(os.getcwd(),"playlists")

def clean_query(track: str,artist: str) -> str:
    """Clean track and artist names for search"""
    track_clean = re.sub(r'[^\w\s]','',track).strip()
    artist_clean = re.sub(r'[^\w\s]','',artist).strip()
    return f"{track_clean} - {artist_clean} official audio"

def get_track_path(artist: str,album: str,track: str) -> str:
    """Create folder structure: playlists/Artist/Album/Track.mp3"""
    artist_dir = os.path.join(BASE_DIR,artist)
    album_dir = os.path.join(BASE_DIR,album)
    os.makedirs(album_dir,exist_ok=True)
    safe_track = re.sub(r'[\\/:"*?<>|]+',"",track)
    return os.path.join(album_dir,f"{safe_track}.mp3")