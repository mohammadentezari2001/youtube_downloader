# YouTube Downloader CLI

A fully interactive command-line tool for downloading YouTube videos and playlists. Features dynamic quality selection, audio/video mode switching, playlist range control, and real-time progress tracking. Built on `yt-dlp` with a rich terminal interface.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)

## Features

- **Interactive Prompts** – Arrow-key navigable menus with input validation via `questionary`
- **Dynamic Quality Selection** – Choose video resolution or audio codec/bitrate at runtime from configurable presets
- **Smart Playlist Handling** – Auto-detects playlist URLs and offers full download, custom range, or single-video extraction
- **Audio Extraction** – Convert downloads to MP3, AAC, FLAC, or Opus with selectable bitrate
- **Resume Support** – Download archive tracking prevents re-downloading already completed files
- **Rich Terminal UI** – Color-coded panels, live progress bars with speed/ETA, and formatted summaries
- **Metadata Embedding** – Automatically embeds thumbnails, titles, and metadata into output files
- **Concurrent Downloads** – Fragment-level parallelism for faster large-file transfers
- **Error Resilience** – Skips private/deleted videos without crashing the entire batch

## Prerequisites

### Python

- Python 3.8 or higher

### FFmpeg (Required)

FFmpeg is mandatory for merging separate video/audio streams and for audio post-processing. The script will not function correctly without it.

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add the `bin` directory to your system PATH.

**Verify installation:**
```bash
ffmpeg -version
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mohammadentezari2001/youtube-downloader-cli.git
cd youtube-downloader-cli
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Launch the interactive downloader:

```bash
python yt_downloader.py
```

### Step-by-Step Workflow

| Step | Prompt | Description |
|------|--------|-------------|
| 1 | Paste URL | Enter any YouTube video or playlist URL |
| 2 | Download Type | Select `Video` or `Audio Only` |
| 3 | Quality/Format | Choose from available presets based on selected type |
| 4 | Playlist Scope | *(Only if playlist detected)* Full, Range, or Single Video |
| 5 | Save Location | Set or confirm the output directory |
| 6 | Confirmation | Review summary and confirm before downloading |

### Playlist Range Syntax

When selecting **Specific Range**, the following formats are supported:

| Input | Result |
|-------|--------|
| `1-10` | Downloads videos 1 through 10 inclusive |
| `5,8,12` | Downloads only videos at indices 5, 8, and 12 |
| `1-5,10,15-20` | Combines ranges and individual indices |
| `3` | Downloads only the video at index 3 |
| `-5` | Downloads the last 5 videos in the playlist |
| `3:` | Downloads from index 3 to the end |

### Output File Naming

Files are saved using the template:
```
{output_dir}/{playlist_index} - {title}.{ext}
```

For single videos (no playlist), the `playlist_index` field is omitted automatically by `yt-dlp`.

## Configuration

All configuration is done directly in `yt_downloader.py` through two dictionaries.

### Video Quality Presets

Edit `VIDEO_FORMATS` to add, remove, or modify resolution options:

```python
VIDEO_FORMATS = {
    "Best Available (4K/8K)": "bestvideo+bestaudio/best",
    "1080p MP4": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "720p MP4": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
    "480p MP4": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
    "Worst (Smallest Size)": "worstvideo+worstaudio/worst",
}
```

Refer to the [yt-dlp format selection documentation](https://github.com/yt-dlp/yt-dlp#format-selection) for advanced filter syntax.

### Audio Format Presets

Edit `AUDIO_FORMATS` to customize available codecs and bitrates:

```python
AUDIO_FORMATS = {
    "MP3 (192kbps)": {"codec": "mp3", "quality": "192"},
    "MP3 (320kbps)": {"codec": "mp3", "quality": "320"},
    "AAC (m4a)": {"codec": "aac", "quality": "192"},
    "FLAC (Lossless)": {"codec": "flac", "quality": "0"},
    "Opus (Best Efficiency)": {"codec": "opus", "quality": "192"},
}
```

### Age-Restricted / Members-Only Content

To access restricted content, add browser cookie extraction inside the `build_opts()` method:

```python
opts['cookiesfrombrowser'] = ('chrome',)  # Supported: chrome, firefox, edge, safari, opera
```

> Never commit cookie files or browser session data to version control.

### Rate Limiting

To avoid IP throttling on large playlist downloads, add sleep intervals in `build_opts()`:

```python
opts['sleep_interval'] = 2
opts['max_sleep_interval'] = 5
```

## Project Structure

```
youtube-downloader-cli/
├── yt_downloader.py       # Main application entry point
├── requirements.txt       # Python package dependencies
├── README.md              # This file
```

## Troubleshooting

### FFmpeg not found
Ensure FFmpeg is installed and accessible from your terminal:
```bash
ffmpeg -version
```
If installed but not recognized, verify it is added to your system PATH.

### Merging fails or produces no output
This typically indicates missing FFmpeg or an incompatible format combination. Ensure you are selecting MP4-compatible formats when merging video and audio.

### Playlist downloads incomplete videos
Private, deleted, or region-locked videos are skipped automatically (`ignoreerrors: True`). Check the terminal output for specific skip reasons.

### Re-downloading already completed files
The `.archive.txt` file tracks completed downloads. If it has been deleted or moved, all files will be re-evaluated. Keep this file intact in your output directory.

### Slow download speeds
YouTube may throttle connections. Enable rate limiting or reduce `concurrent_fragment_downloads` in `build_opts()` to stabilize throughput.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `yt-dlp` | >=2024.1.0 | Core download engine and format handling |
| `rich` | >=13.0.0 | Terminal formatting, panels, and progress display |
| `questionary` | >=2.0.0 | Interactive CLI prompts with arrow-key navigation |

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Disclaimer

This tool is provided for educational and personal use only. Users are solely responsible for ensuring their usage complies with [YouTube's Terms of Service](https://www.youtube.com/static?template=terms) and all applicable local, national, and international copyright laws. Always obtain proper authorization before downloading copyrighted material. The authors and contributors assume no liability for misuse of this software.