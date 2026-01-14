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

- By Gmail URL:
  uv run gmail_thread_to_text.py --gmail-url "https://mail.google.com/mail/u/0/#search/ryan/FMfcgzQdzcrhbbpvkRHTbGBCLpftmKTq" --out thread.txt

- By search query (first match):
  uv run gmail_thread_to_text.py --query "ryan" --out thread.txt

- By RFC822 Message-ID (from “Show original”):
  uv run gmail_thread_to_text.py --query "rfc822msgid:<Message-ID>" --out thread.txt

Options:
- --thread-id <id>
- --include-html-fallback (if no text/plain part)
- --all-threads (dump up to --max threads for a query into one file)

Notes:
- First run opens a browser to authenticate; token.json saved.
- Output is plain text with message separators.
- If you get "Invalid message id", use --query with subject/from or use Gmail "Show original" and pass:
  --query "rfc822msgid:<Message-ID>"
- If you used a subject/from query and got only one message but expect more, add:
  --all-threads --max 10

Security:
- credentials.json and token.json are gitignored.

OAuth testing mode fix (Error 403: access_denied):
- In Google Cloud Console -> OAuth consent screen -> Test users
- If the console redirects, open: https://console.cloud.google.com/auth/overview?project=<YOUR_PROJECT_ID>
- Add the Gmail account you are logging in with (e.g., aadityalr123@gmail.com)
- Save, then re-run the command.

License:
- MIT (see LICENSE).
