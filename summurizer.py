import sys
import os
import csv
import json

# All file types we support
SUPPORTED_TYPES = [".txt", ".md", ".log", ".csv", ".json"]

def summarize_txt_md_log(lines, ext):
    """Handle .txt, .md, .log — all plain text files"""
    full_text = "".join(lines)
    word_count = len(full_text.split())
    preview = [line.rstrip() for line in lines if line.strip()][:3]

    print(f"  Type    : {ext} (plain text)")
    print(f"  Words   : {word_count}")
    print(f"  Lines   : {len(lines)}")
    print("=" * 40)
    print("  Preview (first 3 lines):")
    print()
    for i, line in enumerate(preview, 1):
        print(f"  {i}. {line}")

def summarize_file(filepath):
    # Validate file exists and is a .txt file
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    if not filepath.endswith(".txt"):
        print(f"Error: '{filepath}' is not a .txt file.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Word count across entire file
    full_text = "".join(lines)
    word_count = len(full_text.split())

    # First 3 non-empty lines
    preview_lines = [line.rstrip() for line in lines if line.strip()][:3]

    # Output
    print("=" * 40)
    print(f"  File    : {os.path.basename(filepath)}")
    print(f"  Words   : {word_count}")
    print(f"  Lines   : {len(lines)}")
    print("=" * 40)
    print("  Preview (first 3 lines):")
    print()
    for i, line in enumerate(preview_lines, 1):
        print(f"  {i}. {line}")
    print("=" * 40)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize.py <path-to-file.txt>")
        sys.exit(1)

    summarize_file(sys.argv[1])