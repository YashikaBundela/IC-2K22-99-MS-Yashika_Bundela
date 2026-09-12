"""
video_analyzer.py
------------------
LAB 3 — Video Metadata Analyzer

Accepts a video path and prints a VIDEO METADATA REPORT covering the
container, video stream, and audio stream.

Primary engine : ffprobe (part of the ffmpeg suite) — gives accurate codec,
                  frame rate, bit rate and audio-stream details.
Fallback engine : hachoir (pure-Python parser) — used automatically if
                  ffprobe/ffmpeg is not installed on the system, so the
                  script still runs, just with fewer fields populated.

Minimum supported formats : MP4, AVI
Bonus supported formats   : MKV, MOV, WEBM, WMV, FLV

Requires ffmpeg/ffprobe on PATH for full results:
    Ubuntu/Debian : sudo apt install ffmpeg
    macOS         : brew install ffmpeg
    Windows       : https://ffmpeg.org/download.html

Usage:
    python video_analyzer.py <path-to-video>
"""

import json
import shutil
import subprocess
import sys

from file_utils import validate_file

SUPPORTED_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"}


def _format_duration(seconds) -> str:
    try:
        seconds = float(seconds)
    except (TypeError, ValueError):
        return "N/A"
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _ffprobe_available() -> bool:
    return shutil.which("ffprobe") is not None


def _run_ffprobe(file_path: str) -> dict:
    """Run ffprobe and return the parsed JSON (format + streams)."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        file_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise ValueError(f"ffprobe failed to read the file: {result.stderr.strip()}")
    return json.loads(result.stdout)


def _analyze_with_ffprobe(file_path: str, file_info: dict, ext: str) -> dict:
    probe = _run_ffprobe(file_path)
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

    width = video_stream.get("width", "N/A")
    height = video_stream.get("height", "N/A")
    resolution = f"{width} x {height}" if width != "N/A" else "N/A"

    # frame rate comes as a fraction string like "30000/1001"
    frame_rate = "N/A"
    fr_raw = video_stream.get("r_frame_rate")
    if fr_raw and fr_raw != "0/0":
        try:
            num, den = fr_raw.split("/")
            frame_rate = f"{float(num) / float(den):.2f} fps"
        except (ValueError, ZeroDivisionError):
            frame_rate = fr_raw

    v_bitrate = video_stream.get("bit_rate") or fmt.get("bit_rate")
    a_bitrate = audio_stream.get("bit_rate")

    return {
        "File Name": file_info["file_name"],
        "File Size": file_info["size"],
        "Container": (fmt.get("format_long_name") or ext.lstrip(".").upper()),
        "Duration": _format_duration(fmt.get("duration")),
        "Video": {
            "Resolution": resolution,
            "Frame Rate": frame_rate,
            "Bit Rate": f"{int(v_bitrate) // 1000} kbps" if v_bitrate else "N/A",
            "Codec": video_stream.get("codec_name", "N/A").upper() if video_stream else "N/A",
        },
        "Audio": {
            "Codec": audio_stream.get("codec_name", "N/A").upper() if audio_stream else "N/A",
            "Channels": audio_stream.get("channels", "N/A"),
            "Sampling Rate": f"{audio_stream.get('sample_rate')} Hz" if audio_stream.get("sample_rate") else "N/A",
            "Bit Rate": f"{int(a_bitrate) // 1000} kbps" if a_bitrate else "N/A",
        },
        "Extra": {
            "Creation Date": fmt.get("tags", {}).get("creation_time", "N/A"),
            "Producer": fmt.get("tags", {}).get("encoder", "N/A"),
        },
    }


def _analyze_with_hachoir(file_path: str, file_info: dict, ext: str) -> dict:
    """Fallback path when ffprobe/ffmpeg isn't installed on the system."""
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata

    def _get(flat, *keys, default="N/A"):
        for key in keys:
            for existing_key in flat:
                if existing_key.lower() == key.lower():
                    return flat[existing_key]
        return default

    parser = createParser(file_path)
    if parser is None:
        raise ValueError("Could not parse video file (unsupported or corrupt).")

    with parser:
        metadata = extractMetadata(parser)
    if metadata is None:
        raise ValueError("No metadata could be extracted from this video file.")

    flat = {}
    for line in metadata.exportPlaintext():
        line = line.lstrip("- ").strip()
        if ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if key and key not in flat:
                flat[key] = value

    width = _get(flat, "Image width", "Width")
    height = _get(flat, "Image height", "Height")
    resolution = f"{width} x {height}" if width != "N/A" and height != "N/A" else "N/A"

    return {
        "File Name": file_info["file_name"],
        "File Size": file_info["size"],
        "Container": ext.lstrip(".").upper(),
        "Duration": _get(flat, "Duration"),
        "Video": {
            "Resolution": resolution,
            "Frame Rate": _get(flat, "Frame rate"),
            "Bit Rate": _get(flat, "Bit rate"),
            "Codec": _get(flat, "Compression", "Codec"),
        },
        "Audio": {
            "Codec": _get(flat, "Audio codec", "Compression"),
            "Channels": _get(flat, "Channel", "Nb channel"),
            "Sampling Rate": _get(flat, "Sample rate"),
            "Bit Rate": _get(flat, "Bit rate"),
        },
        "Extra": {
            "Creation Date": _get(flat, "Creation date", "Last modification"),
            "Producer": _get(flat, "Producer"),
        },
    }


def analyze_video(file_path: str) -> dict:
    """Extract metadata from a video file and return it as a structured dict."""
    file_info = validate_file(file_path)

    ext = file_info["extension"]
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported video format '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if _ffprobe_available():
        return _analyze_with_ffprobe(file_path, file_info, ext)
    return _analyze_with_hachoir(file_path, file_info, ext)


def format_report(report: dict) -> str:
    lines = []
    lines.append("=" * 32)
    lines.append("VIDEO METADATA REPORT")
    lines.append("=" * 32)
    lines.append(f"File Name       : {report['File Name']}")
    lines.append(f"File Size       : {report['File Size']}")
    lines.append(f"Container       : {report['Container']}")
    lines.append(f"Duration        : {report['Duration']}")
    lines.append("")
    lines.append("VIDEO")
    lines.append("-" * 32)
    v = report["Video"]
    lines.append(f"Resolution      : {v['Resolution']}")
    lines.append(f"Frame Rate      : {v['Frame Rate']}")
    lines.append(f"Bit Rate        : {v['Bit Rate']}")
    lines.append(f"Codec           : {v['Codec']}")
    lines.append("")
    lines.append("AUDIO")
    lines.append("-" * 32)
    a = report["Audio"]
    lines.append(f"Codec           : {a['Codec']}")
    lines.append(f"Channels        : {a['Channels']}")
    lines.append(f"Sampling Rate   : {a['Sampling Rate']}")
    lines.append(f"Bit Rate        : {a['Bit Rate']}")
    lines.append("")
    lines.append("METADATA")
    lines.append("-" * 32)
    ex = report["Extra"]
    lines.append(f"Creation Date   : {ex['Creation Date']}")
    lines.append(f"Producer        : {ex['Producer']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python video_analyzer.py <path-to-video>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        report = analyze_video(file_path)
        print(format_report(report))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
