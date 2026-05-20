#!/usr/bin/env python3
"""
Read a Feishu/Lark wiki document through the official Open API.

Required environment variables:
  FEISHU_APP_ID
  FEISHU_APP_SECRET

Usage:
  python tools/feishu_read_wiki.py "https://pudutech.feishu.cn/wiki/..."
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://open.feishu.cn/open-apis"


def request_json(method: str, url: str, token: str | None = None, data: dict | None = None) -> dict:
    body = None
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc


def get_tenant_access_token() -> str:
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("Set FEISHU_APP_ID and FEISHU_APP_SECRET first.")

    result = request_json(
        "POST",
        f"{BASE_URL}/auth/v3/tenant_access_token/internal",
        data={"app_id": app_id, "app_secret": app_secret},
    )
    if result.get("code") != 0:
        raise RuntimeError(f"Failed to get tenant_access_token: {result}")
    return result["tenant_access_token"]


def extract_wiki_token(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        path = urllib.parse.urlparse(value).path
        match = re.search(r"/wiki/([^/?#]+)", path)
        if not match:
            raise RuntimeError("Could not find /wiki/{token} in URL.")
        return match.group(1)
    return value


def get_wiki_node(token: str, tenant_token: str) -> dict:
    quoted = urllib.parse.quote(token, safe="")
    result = request_json("GET", f"{BASE_URL}/wiki/v2/spaces/get_node?token={quoted}", token=tenant_token)
    if result.get("code") != 0:
        raise RuntimeError(f"Failed to get wiki node: {result}")
    return result["data"]["node"]


def list_wiki_nodes(space_id: str, tenant_token: str, parent_node_token: str | None = None) -> list[dict]:
    nodes: list[dict] = []
    page_token = ""
    while True:
        params = {"page_size": "50"}
        if page_token:
            params["page_token"] = page_token
        if parent_node_token:
            params["parent_node_token"] = parent_node_token
        query = urllib.parse.urlencode(params)
        result = request_json("GET", f"{BASE_URL}/wiki/v2/spaces/{space_id}/nodes?{query}", token=tenant_token)
        if result.get("code") != 0:
            raise RuntimeError(f"Failed to list wiki nodes: {result}")
        data = result.get("data", {})
        nodes.extend(data.get("items", []))
        if not data.get("has_more"):
            return nodes
        page_token = data.get("page_token", "")


def get_doc_raw_content(document_id: str, tenant_token: str) -> dict:
    quoted = urllib.parse.quote(document_id, safe="")
    result = request_json("GET", f"{BASE_URL}/docx/v1/documents/{quoted}/raw_content", token=tenant_token)
    if result.get("code") != 0:
        raise RuntimeError(f"Failed to get document raw content: {result}")
    return result.get("data", result)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/feishu_read_wiki.py <wiki-url-or-token>", file=sys.stderr)
        return 2

    wiki_token = extract_wiki_token(sys.argv[1])
    tenant_token = get_tenant_access_token()
    node = get_wiki_node(wiki_token, tenant_token)

    print(f"# Wiki Node")
    print(f"- title: {node.get('title')}")
    print(f"- obj_type: {node.get('obj_type')}")
    print(f"- obj_token: {node.get('obj_token')}")
    print()

    if node.get("has_child"):
        print("# Child Nodes")
        for child in list_wiki_nodes(node["space_id"], tenant_token, node["node_token"]):
            print(f"- {child.get('title')} | {child.get('obj_type')} | {child.get('node_token')}")
        print()

    obj_type = node.get("obj_type")
    obj_token = node.get("obj_token")
    if obj_type != "docx":
        print(f"Unsupported wiki obj_type for raw extraction: {obj_type}", file=sys.stderr)
        print(json.dumps(node, ensure_ascii=False, indent=2))
        return 1

    raw = get_doc_raw_content(obj_token, tenant_token)
    content = raw.get("content") or raw.get("raw_content") or json.dumps(raw, ensure_ascii=False, indent=2)
    print("# Raw Content")
    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
