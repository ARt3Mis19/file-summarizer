import sys
import os
import subprocess
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a senior software engineer doing a code review.
Analyse the git diff provided and look for:
1. Bugs or logic errors
2. Security issues (hardcoded secrets, SQL injection, etc)
3. Bad variable names or unclear code
4. Missing error handling
5. Performance problems

For each issue found, respond in this exact format:
- Line: (line number or unknown)
- Severity: (low / medium / high)
- Issue: (one sentence describing the problem)
- Fix: (one sentence suggestion)

If the code looks good, say No issues found. Keep it concise."""

def get_diff():
    """Get the current git diff"""
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )
    return result.stdout

def review_diff(diff):
    """Send diff to Gemini for review"""
    if not diff.strip():
        print("No changes detected. Make some edits first!")
        return

    print("Reviewing your changes...\n")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nHere is the git diff to review:\n\n{diff}"
    )

    print("=" * 40)
    print("  CODE REVIEW RESULTS")
    print("=" * 40)
    print(response.text)
    print("=" * 40)

if __name__ == "__main__":
    # Option 1: pass a diff file as argument
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            diff = f.read()
    # Option 2: auto get diff from current git repo
    else:
        diff = get_diff()

    review_diff(diff)