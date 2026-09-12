"""
main.py
-------
Final Project — Consolidated Multimedia Analyzer

Accepts an Image, Audio, or Video file, automatically decides which
analyzer to run, and prints + saves a consolidated metadata report.

Architecture:

    User Input -> File Validation -> Identify File Type
        -> {ImageAnalyzer | AudioAnalyzer | VideoAnalyzer}
        -> Metadata Extraction -> Report Generator -> Consolidated Report

Usage:
    python main.py <path-to-file>
    python main.py <path-to-file> --save          # also save JSON report
    python main.py <path-to-file> --save out.json # save to a specific path
"""

import argparse
import sys

from file_utils import validate_file
from report_generator import get_analyzer, generate_text_report, save_json_report


def run(file_path: str, save: bool = False, save_path: str = None) -> int:
    # Step 1: File validation (existence, size, extension, type)
    try:
        file_info = validate_file(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    file_type = file_info["file_type"]

    # Step 2: Identify file type -> pick the right analyzer
    analyze_fn, _ = get_analyzer(file_type)
    if analyze_fn is None:
        print(
            f"Error: Unsupported or unrecognized file type '{file_type}' "
            f"for '{file_info['file_name']}'. "
            f"Supported categories: image, audio, video."
        )
        return 1

    # Step 3: Metadata extraction (delegated to the matching analyzer)
    try:
        report = analyze_fn(file_path)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Step 4: Report generation
    text_report = generate_text_report(file_type, report)
    print(text_report)

    # Step 5 (optional): Save consolidated report as JSON
    if save:
        output_path = save_json_report(file_type, report, file_path, save_path)
        print(f"\nJSON report saved to: {output_path}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Consolidated Multimedia Analyzer — auto-detects Image / "
                     "Audio / Video files and extracts their metadata."
    )
    parser.add_argument("file", help="Path to the image, audio, or video file")
    parser.add_argument(
        "--save", nargs="?", const=True, default=False, metavar="OUTPUT.json",
        help="Save the report as JSON under reports/ (optionally give a custom path)"
    )
    args = parser.parse_args()

    save_flag = bool(args.save)
    save_path = args.save if isinstance(args.save, str) else None

    sys.exit(run(args.file, save=save_flag, save_path=save_path))


if __name__ == "__main__":
    main()
