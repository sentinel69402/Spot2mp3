# Spotify2Media

A fast, console-based Python tool to download songs from a Spotify playlist via YouTube.  
Optimized for speed with parallel downloads, batch searches, and automatic query cleaning.  

> **Note:** This is for educational purposes only. Respect copyright laws when using downloaded content.

---

## Features

- Works with **Spotify playlist CSVs** (exportable via [Exportify](https://watsonbox.github.io/exportify/)).  
- **Console-based**, cancelable at any time with `Ctrl+C`.  
- **Parallel downloads** using multiple threads for faster performance.  
- **Batch YouTube searches** to reduce HTTP requests.  
- **Query cleaning** to improve search results (removes special characters, adds "official audio").  
- Converts audio to **MP3** using `yt-dlp` + `ffmpeg`.  

---

## Requirements

- Python 3.10+  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [ffmpeg](https://ffmpeg.org/)  

Install Python dependencies:

```bash
pip install yt-dlp
```