# LAB 3 — Video Metadata Analyzer

Extracts and reports container, video-stream, and audio-stream metadata
from video files.

## Files
- `video_analyzer.py` — main script
- `file_utils.py` — shared file validation helpers
- `samples/` — sample test video

## Run
```bash
pip install hachoir   # pure-Python fallback parser
# Recommended: also install ffmpeg for full accuracy (codec/framerate/bitrate)
#   Ubuntu/Debian: sudo apt install ffmpeg
#   macOS:         brew install ffmpeg
python video_analyzer.py samples/video.mp4
```

## Supported Formats
- Minimum: MP4, AVI
- Bonus: MKV, MOV, WEBM, WMV, FLV

## Notes
`video_analyzer.py` uses `ffprobe` when available for accurate codec, frame
rate, and bit rate data, and automatically falls back to the pure-Python
`hachoir` library if ffmpeg is not installed.

See the [Capstone-Projects/Consolidated-Multimedia-Analyzer](../../Capstone-Projects/Consolidated-Multimedia-Analyzer)
for the full write-up and the combined final project that builds on this lab.
