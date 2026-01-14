Gmail full thread to plain text

Setup:
1) Google Cloud Console -> enable Gmail API
2) Create OAuth Client (Desktop app)
3) Download credentials.json into this folder
4) Install deps:
   uv pip install -r requirements.txt

Usage:
- By message ID (from Gmail URL):
  python gmail_thread_to_text.py --message-id FMfcgzQdzcrhbbpvkRHTbGBCLpftmKTq --out thread.txt

- By search query (first match):
  python gmail_thread_to_text.py --query "ryan" --out thread.txt

Options:
- --thread-id <id>
- --include-html-fallback (if no text/plain part)

Notes:
- First run opens a browser to authenticate; token.json saved.
- Output is plain text with message separators.

Security:
- credentials.json and token.json are gitignored.

License:
- MIT (see LICENSE).
