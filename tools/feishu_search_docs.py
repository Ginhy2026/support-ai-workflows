#!/usr/bin/env python3
"""
Search Feishu/Lark cloud documents through the official docs search API.

Required environment variables:
  FEISHU_APP_ID
  FEISHU_APP_SECRET

Usage:
  python tools/feishu_search_docs.py "CC1 异常噪音" --type docx --type doc
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request

from feishu_read_wiki import get_tenant_access_token


SEARCH_URL = "https://open.feishu.cn/open-apis/suite/docs-api/search/object"


def search_docs(query: str, count: int = 10, offset: int = 0, docs_types: list[str] | None = None) -> dict:
    token = get_tenant_access_token()
    payload: dict = {
        "search_key": query,
        "count": count,
        "offset": offset,
    }
    if docs_types:
        payload["docs_types"] = docs_types

    req = urllib.request.Request(
        SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Feishu cloud documents.")
    parser.add_argument("query", help="Search keywords")
    parser.add_argument("--count", type=int, default=10, help="Number of results")
    parser.add_argument("--offset", type=int, default=0, help="Search offset")
    parser.add_argument("--type", action="append", dest="docs_types", help="Document type, e.g. docx, doc, sheet")
    args = parser.parse_args()

    result = search_docs(args.query, args.count, args.offset, args.docs_types)
    if result.get("code") != 0:
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))

    data = result.get("data", {})
    print(f"# Search Results: {args.query}")
    print(f"- total: {data.get('total')}")
    print(f"- has_more: {data.get('has_more')}")
    print()
    for item in data.get("docs_entities", []):
        print(f"- {item.get('title')} | {item.get('docs_type')} | {item.get('docs_token')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
