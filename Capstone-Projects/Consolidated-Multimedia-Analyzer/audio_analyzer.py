"""
audio_analyzer.py
------------------
Audio Metadata Analyzer (companion to image_analyzer.py / video_analyzer.py
for the Consolidated Multimedia Analyzer final project).

Accepts an audio path and prints an AUDIO METADATA REPORT.

Minimum supported formats : MP3, WAV
Bonus supported formats   : FLAC, AAC/M4A, OGG

Usage:
    python audio_analyzer.py <path-to-audio>
"""

import sys

import mutagen

from file_utils import validate_file

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}


def _format_duration(seconds) -> str:
    if seconds is None:
        return "N/A"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _tag(tags, *keys, default="N/A"):
    """Try several possible tag keys (formats differ) and return the first hit."""
    if not tags:
        return default
    for key in keys:
        if key in tags:
            value = tags[key]
            if isinstance(value, list):
                value = value[0] if value else default
            return str(value)
    return default


def analyze_audio(file_path: str) -> dict:
    """Extract metadata from an audio file and return it as a structured dict."""
    file_info = validate_file(file_path)

    ext = file_info["extension"]
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    audio = mutagen.File(file_path, easy=True)
    if audio is None:
        raise ValueError("Could not parse audio file (unsupported or corrupt).")

    info = audio.info
    duration = getattr(info, "length", None)
    bitrate = getattr(info, "bitrate", None)
    sample_rate = getattr(info, "sample_rate", None)
    channels = getattr(info, "channels", None)

    tags = audio.tags

    report = {
        "File Name": file_info["file_name"],
        "File Size": file_info["size"],
        "Format": ext.lstrip(".").upper(),
        "Duration": _format_duration(duration),
        "Bit Rate": f"{bitrate // 1000} kbps" if bitrate else "N/A",
        "Sampling Rate": f"{sample_rate} Hz" if sample_rate else "N/A",
        "Channels": channels if channels else "N/A",
        "Tags": {
            "Title": _tag(tags, "title"),
            "Artist": _tag(tags, "artist"),
            "Album": _tag(tags, "album"),
            "Date": _tag(tags, "date"),
        },
    }
    return report


def format_report(report: dict) -> str:
    lines = []
    lines.append("=" * 32)
    lines.append("AUDIO METADATA REPORT")
    lines.append("=" * 32)
    lines.append(f"File Name       : {report['File Name']}")
    lines.append(f"File Size       : {report['File Size']}")
    lines.append(f"Format          : {report['Format']}")
    lines.append(f"Duration        : {report['Duration']}")
    lines.append("")
    lines.append("AUDIO")
    lines.append("-" * 32)
    lines.append(f"Bit Rate        : {report['Bit Rate']}")
    lines.append(f"Sampling Rate   : {report['Sampling Rate']}")
    lines.append(f"Channels        : {report['Channels']}")
    lines.append("")
    lines.append("METADATA")
    lines.append("-" * 32)
    tags = report["Tags"]
    lines.append(f"Title           : {tags['Title']}")
    lines.append(f"Artist          : {tags['Artist']}")
    lines.append(f"Album           : {tags['Album']}")
    lines.append(f"Date            : {tags['Date']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python audio_analyzer.py <path-to-audio>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        report = analyze_audio(file_path)
        print(format_report(report))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
