"""
file_utils.py
-------------
Shared helper functions used by every analyzer (image / audio / video).

Responsibilities (as per lab spec):
    - Does the file exist?
    - What is the file size?
    - What is the file extension?
    - What "type" of multimedia file is it (image / audio / video / unknown)?
"""

import os
import mimetypes


# Extension -> broad multimedia category.
# Used as a fast, dependency-free fallback / cross-check for mimetypes.
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".bmp", ".gif"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"}


def file_exists(file_path: str) -> bool:
    """Return True if file_path points to an existing, regular file."""
    return os.path.isfile(file_path)


def get_file_size(file_path: str, human_readable: bool = True):
    """
    Return the file size in bytes, or a human readable string
    (e.g. '2.35 MB') when human_readable=True.
    """
    size_bytes = os.path.getsize(file_path)
    if not human_readable:
        return size_bytes

    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def get_file_extension(file_path: str) -> str:
    """Return the lower-cased file extension, including the leading dot."""
    return os.path.splitext(file_path)[1].lower()


def get_file_type(file_path: str) -> str:
    """
    Identify whether a file is an 'image', 'audio', 'video', or 'unknown'
    type. Tries the standard mimetypes module first, then falls back to a
    manual extension lookup (mimetypes does not know every container, e.g.
    .mkv, .webp on some systems).
    """
    ext = get_file_extension(file_path)

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        broad = mime_type.split("/")[0]
        if broad in ("image", "audio", "video"):
            return broad

    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in VIDEO_EXTENSIONS:
        return "video"

    return "unknown"


def validate_file(file_path: str) -> dict:
    """
    Run all validation checks in one call. Returns a dict summary that
    main.py / other analyzers can use, e.g.:

        {
            "exists": True,
            "size": "1.20 MB",
            "size_bytes": 1258291,
            "extension": ".jpg",
            "file_type": "image",
            "file_name": "photo.jpg",
        }

    Raises FileNotFoundError if the file does not exist.
    """
    if not file_exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return {
        "exists": True,
        "size": get_file_size(file_path),
        "size_bytes": get_file_size(file_path, human_readable=False),
        "extension": get_file_extension(file_path),
        "file_type": get_file_type(file_path),
        "file_name": os.path.basename(file_path),
    }


if __name__ == "__main__":
    # Quick manual test
    import sys
    if len(sys.argv) > 1:
        import json
        print(json.dumps(validate_file(sys.argv[1]), indent=2))
    else:
        print("Usage: python file_utils.py <path-to-file>")
