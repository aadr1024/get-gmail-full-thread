#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-api-python-client",
#   "google-auth-oauthlib",
# ]
# ///
"""Fetch Gmail thread(s) and export plain-text transcript.

Requires OAuth Desktop app credentials.json.
Writes token.json on first run.
"""

import argparse
import base64
import os
from email.utils import getaddresses
from typing import Dict, List, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def _decode_body(part: Dict) -> str:
    data = part.get("body", {}).get("data")
    if not data:
        return ""
    return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")


def _extract_text(payload: Dict) -> str:
    if payload.get("mimeType") == "text/plain":
        return _decode_body(payload)
    text_parts: List[str] = []
    for part in payload.get("parts", []) or []:
        if part.get("mimeType") == "text/plain":
            text_parts.append(_decode_body(part))
        elif part.get("parts"):
            nested = _extract_text(part)
            if nested:
                text_parts.append(nested)
    return "\n".join([t for t in text_parts if t])


def _header_map(headers: List[Dict]) -> Dict[str, str]:
    return {h["name"].lower(): h["value"] for h in headers}


def _format_recipients(value: str) -> str:
    addrs = getaddresses([value])
    return ", ".join([f"{name} <{addr}>" if name else addr for name, addr in addrs])


def _resolve_thread_id(service, message_id: Optional[str], thread_id: Optional[str], query: Optional[str], max_results: int) -> str:
    if thread_id:
        return thread_id
    if message_id:
        msg = service.users().messages().get(userId="me", id=message_id, format="metadata").execute()
        return msg["threadId"]
    if query:
        resp = service.users().threads().list(userId="me", q=query, maxResults=max_results).execute()
        threads = resp.get("threads", [])
        if not threads:
            raise SystemExit("No threads found for query")
        return threads[0]["id"]
    raise SystemExit("Need --thread-id, --message-id, or --query")


def main():
    ap = argparse.ArgumentParser(description="Export Gmail thread to plain text")
    ap.add_argument("--message-id", help="Gmail message ID (from URL)")
    ap.add_argument("--thread-id", help="Gmail thread ID")
    ap.add_argument("--query", help="Gmail search query (uses first match)")
    ap.add_argument("--max", type=int, default=1, help="Max threads to search (default 1)")
    ap.add_argument("--out", default="thread.txt", help="Output file")
    ap.add_argument("--include-html-fallback", action="store_true", help="Fallback to text from HTML when text/plain missing")
    args = ap.parse_args()

    service = _get_service()
    thread_id = _resolve_thread_id(service, args.message_id, args.thread_id, args.query, args.max)

    thread = service.users().threads().get(userId="me", id=thread_id, format="full").execute()

    out_lines: List[str] = []
    for msg in thread.get("messages", []):
        headers = _header_map(msg["payload"]["headers"])
        out_lines.append("=" * 72)
        out_lines.append(f"From: {_format_recipients(headers.get('from',''))}")
        out_lines.append(f"To: {_format_recipients(headers.get('to',''))}")
        out_lines.append(f"Date: {headers.get('date','')}")
        out_lines.append(f"Subject: {headers.get('subject','')}")
        out_lines.append("")
        body = _extract_text(msg["payload"]).strip()
        if not body and args.include_html_fallback:
            # naive fallback: decode first text/html part
            for part in msg["payload"].get("parts", []) or []:
                if part.get("mimeType") == "text/html":
                    body = _decode_body(part).strip()
                    break
        out_lines.append(body or "[no text/plain body]")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines).strip() + "\n")


if __name__ == "__main__":
    main()
