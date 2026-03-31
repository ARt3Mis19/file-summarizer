import os
import sys
from github import Github
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Clients
gh = Github(os.getenv("GITHUB_TOKEN"))
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a senior software engineer doing a code review.
Analyse the git diff and look for:
1. Bugs or logic errors
2. Security issues
3. Bad variable names or unclear code
4. Missing error handling
5. Performance problems

For each issue respond like this:
- Line: (number or unknown)
- Severity: (low / medium / high)
- Issue: (one sentence)
- Fix: (one sentence)

If code looks good say: No issues found. Be concise."""

def review_pr(repo_name, pr_number):
    # Get the repo and PR
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    print(f"Reviewing PR #{pr_number}: {pr.title}")

    # Get the diff from all changed files
    full_diff = ""
    for file in pr.get_files():
        if file.patch:  # patch is the diff
            full_diff += f"\n--- {file.filename} ---\n"
            full_diff += file.patch

    if not full_diff:
        print("No changes found in this PR.")
        return

    # Send to Gemini
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nHere is the PR diff:\n\n{full_diff[:8000]}"
    )

    review_comment = response.text

    # Post comment on the PR
    pr.create_issue_comment(
        f"## 🤖 AI Code Review\n\n{review_comment}\n\n---\n*Reviewed by Gemini 2.5 Flash*"
    )

    print("Review posted successfully!")

if __name__ == "__main__":
    # Usage: python pr_review_bot.py owner/repo 1
    if len(sys.argv) != 3:
        print("Usage: python pr_review_bot.py owner/repo pr_number")
        sys.exit(1)

    repo_name = sys.argv[1]
    pr_number = int(sys.argv[2])
    review_pr(repo_name, pr_number)