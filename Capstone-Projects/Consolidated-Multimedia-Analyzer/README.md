# Consolidated Multimedia Analyzer

A small command-line toolkit that inspects **image**, **audio**, and **video**
files and prints a clean metadata report — built for the Multimedia Systems
Lab (LAB 2, LAB 3, and the Final Project).

## Contents

| File                  | Purpose                                                              |
|------------------------|-----------------------------------------------------------------------|
| `file_utils.py`        | Shared helpers: file exists?, file size, extension, file type         |
| `image_analyzer.py`    | LAB 2 — Image metadata report (dimensions, format, EXIF)              |
| `audio_analyzer.py`    | Audio metadata report (duration, bit rate, sample rate, tags)         |
| `video_analyzer.py`    | LAB 3 — Video metadata report (container, video stream, audio stream) |
| `report_generator.py`  | Formats reports as text and saves them as JSON under `reports/`       |
| `main.py`              | Final Project — auto-detects file type and runs the right analyzer    |

## Architecture

```
User Input -> File Validation -> Identify File Type
    -> { ImageAnalyzer | AudioAnalyzer | VideoAnalyzer }
    -> Metadata Extraction -> Report Generator -> Consolidated Report
```

## Setup

```bash
pip install -r requirements.txt
```

Video analysis uses **ffprobe** (from ffmpeg) when available, for accurate
codec / frame-rate / bit-rate data. If ffmpeg isn't installed, it
automatically falls back to the pure-Python `hachoir` parser with reduced
detail.

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Usage

Run each analyzer standalone:

```bash
python image_analyzer.py samples/image.jpg
python audio_analyzer.py samples/song.mp3
python video_analyzer.py samples/video.mp4
```

Or let the consolidated analyzer auto-detect the file type:

```bash
python main.py samples/image.jpg
python main.py samples/video.mp4 --save          # also saves a JSON report
python main.py samples/video.mp4 --save custom.json
```

## Supported Formats

| Type  | Minimum          | Bonus                              |
|-------|-------------------|-------------------------------------|
| Image | JPG/JPEG, PNG     | TIFF, WEBP, BMP, GIF                |
| Audio | MP3, WAV          | FLAC, AAC/M4A, OGG                  |
| Video | MP4, AVI          | MKV, MOV, WEBM, WMV, FLV            |

## Sample Output

```
================================
IMAGE METADATA REPORT
================================
File Name       : image.jpg
File Size       : 5.30 KB
File Format     : JPEG
Width           : 640 px
Height          : 480 px
Resolution      : 640 x 480
Color Mode      : RGB
EXIF Metadata
--------------------------------
Camera          : N/A
Date Taken      : N/A
Orientation     : N/A
```

## Notes

- `file_utils.py` centralizes file validation so every analyzer (and
  `main.py`) shares the same logic for detecting whether a path is an
  image, audio, or video file.
- `report_generator.py` keeps text-formatting and JSON-saving logic out of
  `main.py`, so adding a new output format later (e.g. HTML/PDF) only
  touches one file.
- JSON reports are timestamped and saved under `reports/` so repeated runs
  never overwrite each other.
