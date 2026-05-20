#!/usr/bin/env python3
"""
Search Feishu/Lark cloud documents through the official lark-cli.

Prerequisites:
  npm install -g @larksuite/cli
  lark-cli auth login --domain search --recommend

Usage:
  python tools/feishu_search_docs.py "CC1 异常噪音" --type wiki --type docx
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys


TYPE_MAP = {
    "doc": "doc",
    "docx": "docx",
    "sheet": "sheet",
    "wiki": "wiki",
    "file": "file",
    "folder": "folder",
    "slides": "slides",
}


def find_lark_cli() -> str:
    cmd = shutil.which("lark-cli") or shutil.which("lark-cli.cmd")
    if cmd:
        return cmd
    windows_default = r"C:\Users\Ginhy\AppData\Roaming\npm\lark-cli.cmd"
    if shutil.which(windows_default):
        return windows_default
    raise RuntimeError("lark-cli not found. Install it with: npm install -g @larksuite/cli")


def search(query: str, count: int, docs_types: list[str]) -> dict:
    cli = find_lark_cli()
    mapped_types = [TYPE_MAP[t.lower()] for t in docs_types]
    args = [
        cli,
        "drive",
        "+search",
        "--query",
        query,
        "--doc-types",
        ",".join(mapped_types),
        "--page-size",
        str(count),
        "--format",
        "json",
    ]
    proc = subprocess.run(args, text=True, capture_output=True, encoding="utf-8", check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def strip_highlight(value: str | None) -> str:
    if not value:
        return ""
    return value.replace("<h>", "").replace("</h>", "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Feishu/Lark docs and wiki through lark-cli.")
    parser.add_argument("query", help="Search keywords")
    parser.add_argument("--count", type=int, default=10, help="Number of results, 1-20")
    parser.add_argument("--type", action="append", dest="docs_types", default=["wiki", "docx"], help="Document type")
    args = parser.parse_args()

    result = search(args.query, args.count, args.docs_types)
    data = result.get("data", {})
    print(f"# Search Results: {args.query}")
    print(f"- total: {data.get('total', 0)}")
    print(f"- has_more: {data.get('has_more', False)}")
    print()

    for index, item in enumerate(data.get("results", []), start=1):
        meta = item.get("result_meta", {})
        title = strip_highlight(item.get("title_highlighted"))
        summary = strip_highlight(item.get("summary_highlighted"))
        print(f"## {index}. {title}")
        print(f"- entity_type: {item.get('entity_type')}")
        print(f"- doc_type: {meta.get('doc_types')}")
        print(f"- token: {meta.get('token')}")
        print(f"- url: {meta.get('url')}")
        print(f"- updated: {meta.get('update_time_iso')}")
        if summary:
            print(f"- summary: {summary}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
