# Audio Metadata Analyzer

Extracts and reports metadata (duration, bit rate, sampling rate, channels,
tags) from audio files. Built as the audio counterpart to LAB 2 (image) and
LAB 3 (video), feeding into the Final Project's Consolidated Multimedia
Analyzer.

## Files
- `audio_analyzer.py` — main script
- `file_utils.py` — shared file validation helpers
- `samples/` — sample test audio

## Run
```bash
pip install mutagen
python audio_analyzer.py samples/song.mp3
```

## Supported Formats
- Minimum: MP3, WAV
- Bonus: FLAC, AAC/M4A, OGG

See the [Capstone-Projects/Consolidated-Multimedia-Analyzer](../../Capstone-Projects/Consolidated-Multimedia-Analyzer)
for the full write-up and the combined final project that builds on this lab.
