"""
report_generator.py
--------------------
Responsible for:
    - Taking the raw metadata dict produced by an analyzer
      (image_analyzer / audio_analyzer / video_analyzer)
    - Rendering it as a human-readable text report (reuses each
      analyzer's own format_report function for consistent layout)
    - Saving the raw structured data as JSON under reports/

Keeping this logic in one place means main.py doesn't need to know the
formatting details of each analyzer.
"""

import json
import os
from datetime import datetime

import image_analyzer
import audio_analyzer
import video_analyzer

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")

# Maps file_type -> (analyze_function, format_function)
_ANALYZER_MAP = {
    "image": (image_analyzer.analyze_image, image_analyzer.format_report),
    "audio": (audio_analyzer.analyze_audio, audio_analyzer.format_report),
    "video": (video_analyzer.analyze_video, video_analyzer.format_report),
}


def get_analyzer(file_type: str):
    """Return (analyze_fn, format_fn) for a given file_type, or (None, None)."""
    return _ANALYZER_MAP.get(file_type, (None, None))


def generate_text_report(file_type: str, report: dict) -> str:
    """Render the structured metadata dict as plain text."""
    _, format_fn = get_analyzer(file_type)
    if format_fn is None:
        raise ValueError(f"No formatter available for file type '{file_type}'")
    return format_fn(report)


def save_json_report(file_type: str, report: dict, source_path: str,
                      output_path: str = None) -> str:
    """
    Save the metadata dict as JSON under reports/ (or a custom output_path).
    Returns the path the file was written to.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if output_path is None:
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(REPORTS_DIR, f"{base_name}_{file_type}_{timestamp}.json")

    payload = {
        "source_file": source_path,
        "file_type": file_type,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "metadata": report,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    return output_path
