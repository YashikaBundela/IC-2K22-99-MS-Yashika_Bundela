"""
image_analyzer.py
------------------
LAB 2 — Image Metadata Analyzer

Accepts an image path and prints an IMAGE METADATA REPORT.

Minimum supported formats : JPG/JPEG, PNG
Bonus supported formats   : TIFF, WEBP, BMP  (also GIF, works via Pillow)

Usage:
    python image_analyzer.py <path-to-image>
"""

import os
import sys

from PIL import Image
from PIL.ExifTags import TAGS

from file_utils import validate_file, get_file_size

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".bmp", ".gif"}


def _get_exif_data(img: Image.Image) -> dict:
    """Return a dict of human-readable EXIF tag -> value, or {} if none."""
    exif_data = {}
    try:
        raw_exif = img.getexif()
    except Exception:
        raw_exif = None

    if not raw_exif:
        return exif_data

    for tag_id, value in raw_exif.items():
        tag_name = TAGS.get(tag_id, tag_id)
        # Some EXIF values are bytes; decode where possible for clean printing.
        if isinstance(value, bytes):
            try:
                value = value.decode(errors="replace")
            except Exception:
                value = str(value)
        exif_data[tag_name] = value

    return exif_data


ORIENTATION_MAP = {
    1: "Normal",
    2: "Mirrored horizontal",
    3: "Rotated 180",
    4: "Mirrored vertical",
    5: "Mirrored horizontal, rotated 90 CCW",
    6: "Rotated 90 CW",
    7: "Mirrored horizontal, rotated 90 CW",
    8: "Rotated 90 CCW",
}


def analyze_image(file_path: str) -> dict:
    """
    Extract metadata from an image file and return it as a structured dict.
    Raises FileNotFoundError / ValueError for missing or unsupported files.
    """
    file_info = validate_file(file_path)

    ext = file_info["extension"]
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    with Image.open(file_path) as img:
        width, height = img.size
        color_mode = img.mode
        img_format = img.format

        exif = _get_exif_data(img)

    camera_make = exif.get("Make", "N/A")
    camera_model = exif.get("Model", "N/A")
    camera = f"{camera_make} {camera_model}".strip()
    if camera in ("N/A N/A", ""):
        camera = "N/A"

    date_taken = exif.get("DateTime") or exif.get("DateTimeOriginal") or "N/A"

    orientation_raw = exif.get("Orientation", None)
    orientation = ORIENTATION_MAP.get(orientation_raw, "N/A")

    report = {
        "File Name": file_info["file_name"],
        "File Size": file_info["size"],
        "File Format": img_format,
        "Width": f"{width} px",
        "Height": f"{height} px",
        "Resolution": f"{width} x {height}",
        "Color Mode": color_mode,
        "EXIF": {
            "Camera": camera,
            "Date Taken": date_taken,
            "Orientation": orientation,
        },
    }
    return report


def format_report(report: dict) -> str:
    """Render the report dict as the plain-text layout the lab asks for."""
    lines = []
    lines.append("=" * 32)
    lines.append("IMAGE METADATA REPORT")
    lines.append("=" * 32)
    lines.append(f"File Name       : {report['File Name']}")
    lines.append(f"File Size       : {report['File Size']}")
    lines.append(f"File Format     : {report['File Format']}")
    lines.append(f"Width           : {report['Width']}")
    lines.append(f"Height          : {report['Height']}")
    lines.append(f"Resolution      : {report['Resolution']}")
    lines.append(f"Color Mode      : {report['Color Mode']}")
    lines.append("EXIF Metadata")
    lines.append("-" * 32)
    exif = report["EXIF"]
    lines.append(f"Camera          : {exif['Camera']}")
    lines.append(f"Date Taken      : {exif['Date Taken']}")
    lines.append(f"Orientation     : {exif['Orientation']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python image_analyzer.py <path-to-image>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        report = analyze_image(file_path)
        print(format_report(report))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
