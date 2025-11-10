import csv
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from downloader.youtube import download_track

MAX_WORKERS = 4

def load_playlist(csv_path):
    if not os.path.isfile(csv_path):
        print("CSV file not found.")
        sys.exit(1)
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def process_playlist(tracks, auto_confirm=False):
    futures = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for row in tracks:
            track_name = row.get("Track Name")
            artist_name = row.get("Artist Name(s)")
            album_name = row.get("Album Name")
            if not track_name or not artist_name:
                continue

            # Prompt if not auto
            if not auto_confirm:
                confirm = input(f"Download '{track_name}' by {artist_name}? [y/N]: ").strip().lower()
                if confirm != "y":
                    continue

            futures.append(executor.submit(download_track, track_name, artist_name, album_name))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading track: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Spotify playlist tracks via YouTube")
    parser.add_argument("csv", help="Path to Spotify playlist CSV")
    parser.add_argument("--all", action="store_true", help="Download all tracks without prompting")
    args = parser.parse_args()

    playlist = load_playlist(args.csv)
    process_playlist(playlist, auto_confirm=args.all)
