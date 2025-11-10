# Spotify2Media

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)

A fast, console-based Python tool to download songs from a Spotify playlist via YouTube.

**Optimized for speed** with parallel downloads, batch searches, and automatic query cleaning.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration)

</div>

---

> **⚠️ Disclaimer:** This tool is for educational purposes only. Respect copyright laws when using downloaded content.

---

## Features

- Works with **Spotify playlist CSVs** (exportable via [Exportify](https://exportify.net/))
- **Console-based** interface, cancelable at any time with `Ctrl+C`
- **Parallel downloads** using multiple threads for faster performance
- **Batch YouTube searches** to reduce HTTP requests
- **Query cleaning** to improve search results (removes special characters, adds "official audio")
- Converts audio to **MP3** using `yt-dlp` + `ffmpeg`
- Organizes downloads in **Artist/Album** folder structure
- **Smart skip** - avoids re-downloading existing tracks

---

## Installation

### Prerequisites

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-007808?logo=ffmpeg&logoColor=white)

- **Python 3.10+**
- **ffmpeg** - [Download here](https://ffmpeg.org/download.html)

### Install Dependencies

```bash
pip install yt-dlp
```

### Clone Repository

```bash
git clone https://github.com/yourusername/spotify2media.git
cd spotify2media
```

---

## Usage

### 1. Export Your Spotify Playlist

Visit [Exportify](https://exportify.net/) and export your playlist as a CSV file.

### 2. Run the Downloader

**Download all tracks automatically:**
```bash
python main.py playlist.csv --all
```

**Download with confirmation prompts:**
```bash
python main.py playlist.csv
```

### 3. Find Your Music

Downloaded tracks are organized in:
```
playlists/
├── Artist Name/
│   └── Album Name/
│       └── Track Name.mp3
```

---

## Configuration

### Adjust Download Settings

Edit the configuration variables in `main.py`:

```python
MAX_WORKERS = 4  # Number of parallel downloads (adjust based on your CPU)
```

Edit search settings in `downloader/youtube.py`:

```python
BATCH_SEARCH = 5   # Number of search results to fetch
MAX_RETRIES = 3    # Retry attempts for failed downloads
```

---

## Command Line Arguments

| Argument | Description |
|----------|-------------|
| `csv` | Path to Spotify playlist CSV file (required) |
| `--all` | Download all tracks without prompting |

### Examples

```bash
# Download with prompts
python main.py my_playlist.csv

# Download all automatically
python main.py my_playlist.csv --all
```

---

## Troubleshooting

**Issue: "FFmpeg not found"**
- Install FFmpeg and ensure it's in your system PATH
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/) and add to PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

**Issue: Downloads are slow**
- Increase `MAX_WORKERS` in `main.py` (e.g., to 8 or 16)
- Check your internet connection

**Issue: Wrong songs downloaded**
- The tool searches YouTube automatically
- Results depend on YouTube's search algorithm
- Consider manually verifying important tracks

---

## License

![License](https://img.shields.io/badge/license-MIT-green.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [Exportify](https://exportify.net/) - Spotify playlist exporter
- [FFmpeg](https://ffmpeg.org/) - Audio processing

---

<div align="center">

Made with ❤️ for music lovers

**Star this repo if you find it useful!**

</div>
