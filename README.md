Gmail full thread to plain text

Setup (fast path):
1) Google Cloud Console -> enable Gmail API
2) Create OAuth Client (Desktop app)
3) Download OAuth JSON to this folder
4) Easiest: copy+edit template
   cp credentials.sample.json credentials.json
   # then paste your real values into credentials.json
5) No pip install needed: dependencies are in-file and uv handles them.

Usage:
- By message ID (from Gmail URL):
  uv run gmail_thread_to_text.py --message-id FMfcgzQdzcrhbbpvkRHTbGBCLpftmKTq --out thread.txt

- By search query (first match):
  uv run gmail_thread_to_text.py --query "ryan" --out thread.txt

Options:
- --thread-id <id>
- --include-html-fallback (if no text/plain part)

Notes:
- First run opens a browser to authenticate; token.json saved.
- Output is plain text with message separators.

Security:
- credentials.json and token.json are gitignored.

OAuth testing mode fix (Error 403: access_denied):
- In Google Cloud Console -> OAuth consent screen -> Test users
- Add the Gmail account you are logging in with (e.g., aadityalr123@gmail.com)
- Save, then re-run the command.

License:
- MIT (see LICENSE).
