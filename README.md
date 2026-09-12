# Multimedia-Systems-Lab

> Repository: `Roll_No-MS-Your_Name` — rename to your actual roll number and
> name before pushing, e.g. `21CS1234-MS-JohnDoe`.

Coursework and lab assignments for the Multimedia Systems Lab.

## Repository Structure

```
Multimedia-Systems-Lab/
├── Cluster01-Multimedia-Fundamentals/
├── Cluster02-Image-Processing/
│   └── Lab02-Image-Metadata-Analyzer/      <- LAB 2
├── Cluster03-Audio-Processing/
│   └── Audio-Metadata-Analyzer/
├── Cluster04-Video-Processing/
│   └── Lab03-Video-Metadata-Analyzer/      <- LAB 3
├── Cluster05-Compression/
├── Cluster06-Multimedia-Communication/
├── Cluster07-Interactive-Multimedia/
├── Cluster08-Advanced-Multimedia-AI/
├── Capstone-Projects/
│   └── Consolidated-Multimedia-Analyzer/   <- Final Project
│
├── datasets/
├── docs/
│   ├── diagrams/
│   ├── architecture/
│   ├── experimental-results/
│   ├── complexity-analysis.pdf
│   └── final-report.pdf
├── README.md
└── .gitignore
```

## Completed Work

| Lab | Folder | Description |
|---|---|---|
| LAB 2 | [Cluster02-Image-Processing/Lab02-Image-Metadata-Analyzer](Cluster02-Image-Processing/Lab02-Image-Metadata-Analyzer) | Reads JPG/PNG (+ TIFF/WEBP/BMP) images and reports dimensions, format, color mode, and EXIF metadata |
| — | [Cluster03-Audio-Processing/Audio-Metadata-Analyzer](Cluster03-Audio-Processing/Audio-Metadata-Analyzer) | Reads MP3/WAV (+ FLAC/AAC/OGG) audio and reports duration, bit rate, sample rate, and tags |
| LAB 3 | [Cluster04-Video-Processing/Lab03-Video-Metadata-Analyzer](Cluster04-Video-Processing/Lab03-Video-Metadata-Analyzer) | Reads MP4/AVI (+ MKV/MOV/WEBM) video and reports container, video-stream, and audio-stream metadata |
| Final Project | [Capstone-Projects/Consolidated-Multimedia-Analyzer](Capstone-Projects/Consolidated-Multimedia-Analyzer) | Combines all three analyzers behind one CLI (`main.py`) that auto-detects file type and routes to the correct analyzer |

## Quick Start (Final Project)

```bash
cd Capstone-Projects/Consolidated-Multimedia-Analyzer
pip install -r requirements.txt
python main.py samples/image.jpg
python main.py samples/song.mp3
python main.py samples/video.mp4 --save
```

## Author

- **Name:** Your Name
- **Roll No:** Roll_No
- **Course:** Multimedia Systems Lab
