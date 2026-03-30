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



def summarize_csv(filepath):
    """Handle .csv — show row/column count and first 3 rows"""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("  (empty CSV file)")
        return

    headers = rows[0]
    data_rows = rows[1:]

    print(f"  Type    : .csv (spreadsheet)")
    print(f"  Columns : {len(headers)}")
    print(f"  Rows    : {len(data_rows)} (excluding header)")
    print("=" * 40)
    print("  Headers :", ", ".join(headers))
    print()
    print("  Preview (first 3 rows):")
    print()
    for i, row in enumerate(data_rows[:3], 1):
        print(f"  {i}. {', '.join(row)}")


def summarize_json(filepath):
    """Handle .json — show structure and a peek inside"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"  Type    : .json")

    if isinstance(data, list):
        print(f"  Items   : {len(data)} (it's a list)")
        print("=" * 40)
        print("  Preview (first 3 items):")
        print()
        for i, item in enumerate(data[:3], 1):
            print(f"  {i}. {str(item)[:80]}")
    elif isinstance(data, dict):
        keys = list(data.keys())
        print(f"  Keys    : {len(keys)}")
        print("=" * 40)
        print("  Top-level keys:")
        print()
        for i, key in enumerate(keys[:5], 1):
            print(f"  {i}. {key}: {str(data[key])[:60]}")
    else:
        print("=" * 40)
        print(f"  Value: {str(data)[:100]}")


def summarize_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext not in SUPPORTED_TYPES:
        print(f"Error: '{ext}' files are not supported.")
        print(f"Supported types: {', '.join(SUPPORTED_TYPES)}")
        sys.exit(1)

    print("=" * 40)
    print(f"  File    : {os.path.basename(filepath)}")

    if ext in [".txt", ".md", ".log"]:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        summarize_txt_md_log(lines, ext)
    elif ext == ".csv":
        summarize_csv(filepath)
    elif ext == ".json":
        summarize_json(filepath)



