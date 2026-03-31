import sys
import os
import csv
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SUPPORTED_TYPES = [".txt", ".md", ".log", ".csv", ".json", ".py"]

def ask_gemini(content, filetype):
    """Send file content to Gemini and get a plain English explanation"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"You are a helpful assistant. Explain what this {filetype} file contains in simple plain English. Keep it under 100 words.\n\n{content}"
    )
    return response.text

def summarize_txt_md_log(lines, ext):
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
    print("=" * 40)
    print("  AI Summary:")
    print()
    print(ask_gemini(full_text[:3000], ext))

def summarize_csv(filepath):
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
    print("=" * 40)
    print("  AI Summary:")
    print()
    sample = "\n".join([",".join(headers)] + [",".join(r) for r in data_rows[:10]])
    print(ask_gemini(sample, ".csv"))

def summarize_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        data = json.loads(content)
    print(f"  Type    : .json")
    if isinstance(data, list):
        print(f"  Items   : {len(data)} (it's a list)")
    elif isinstance(data, dict):
        print(f"  Keys    : {len(data.keys())}")
    print("=" * 40)
    print("  AI Summary:")
    print()
    print(ask_gemini(content[:3000], ".json"))

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
    if ext in [".txt", ".md", ".log", ".py"]:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        summarize_txt_md_log(lines, ext)
    elif ext == ".csv":
        summarize_csv(filepath)
    elif ext == ".json":
        summarize_json(filepath)
    print("=" * 40)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize.py <file>")
        print(f"Supported: {', '.join(SUPPORTED_TYPES)}")
        sys.exit(1)
    summarize_file(sys.argv[1])



