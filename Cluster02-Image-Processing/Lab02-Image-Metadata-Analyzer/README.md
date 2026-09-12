# LAB 2 — Image Metadata Analyzer

Extracts and reports metadata (dimensions, format, color mode, EXIF data)
from image files.

## Files
- `image_analyzer.py` — main script
- `file_utils.py` — shared file validation helpers
- `samples/` — sample test images

## Run
```bash
pip install Pillow
python image_analyzer.py samples/image.jpg
```

## Supported Formats
- Minimum: JPG/JPEG, PNG
- Bonus: TIFF, WEBP, BMP

See the [Capstone-Projects/Consolidated-Multimedia-Analyzer](../../Capstone-Projects/Consolidated-Multimedia-Analyzer)
for the full write-up and the combined final project that builds on this lab.
