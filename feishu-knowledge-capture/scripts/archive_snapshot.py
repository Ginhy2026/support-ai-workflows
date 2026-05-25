#!/usr/bin/env python3
"""Write versioned Markdown snapshots for Feishu knowledge candidates."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def slug(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^0-9A-Za-z._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def archive_dir(root: Path, source_scope: str, candidate_key: str, date: str) -> Path:
    if candidate_key.startswith("workorder:"):
        return root / "jswo" / slug(candidate_key.split(":", 1)[1])
    if candidate_key.startswith("thread:"):
        return root / "support-triage" / date / slug(candidate_key.split(":", 1)[1])
    return root / "manual-runs" / date / slug(candidate_key.replace(":", "-"))


def next_version(target_dir: Path) -> str:
    existing = sorted(target_dir.glob("v*.md"))
    if not existing:
        return "v001"
    latest = existing[-1].stem
    match = re.fullmatch(r"v(\d+)", latest)
    if not match:
        return f"v{len(existing) + 1:03d}"
    return f"v{int(match.group(1)) + 1:03d}"


def load_metadata(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dump_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_frontmatter(data: dict[str, str]) -> str:
    lines = ["---"]
    for key, value in data.items():
        safe = str(value).replace('"', '\\"')
        lines.append(f'{key}: "{safe}"')
    lines.append("---")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive a candidate Markdown snapshot.")
    parser.add_argument("--root", default="knowledge-archive")
    parser.add_argument("--candidate-key", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--source-scope", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--feishu-doc-url", default="")
    parser.add_argument("--review-status", default="待审核")
    parser.add_argument("--support-owner", default="待确认")
    parser.add_argument("--leader", default="待确认")
    parser.add_argument("--service-representative", default="待确认")
    parser.add_argument("--triggered-by", default="")
    parser.add_argument("--contributors", default="")
    parser.add_argument("--last-updated-by", default="")
    parser.add_argument("--date", default="")
    parser.add_argument("--content-file", required=True)
    args = parser.parse_args()

    now = datetime.now(timezone.utc).astimezone()
    date = args.date or now.strftime("%Y-%m-%d")
    root = Path(args.root)
    target_dir = archive_dir(root, args.source_scope, args.candidate_key, date)
    target_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = target_dir / "metadata.json"
    old_metadata = load_metadata(metadata_path)
    version = next_version(target_dir)
    created_at = old_metadata.get("created_at", now.isoformat(timespec="seconds"))
    updated_at = now.isoformat(timespec="seconds")

    frontmatter = build_frontmatter(
        {
            "candidate_key": args.candidate_key,
            "type": args.type,
            "version": version,
            "source": args.source_scope,
            "title": args.title,
            "feishu_doc_url": args.feishu_doc_url,
            "created_at": created_at,
            "updated_at": updated_at,
            "review_status": args.review_status,
            "support_owner": args.support_owner,
            "leader": args.leader,
            "service_representative": args.service_representative,
            "triggered_by": args.triggered_by,
            "contributors": args.contributors,
            "last_updated_by": args.last_updated_by,
        }
    )
    body = Path(args.content_file).read_text(encoding="utf-8").strip()
    snapshot_path = target_dir / f"{version}.md"
    snapshot_path.write_text(f"{frontmatter}\n\n{body}\n", encoding="utf-8")

    metadata = {
        **old_metadata,
        "candidate_key": args.candidate_key,
        "type": args.type,
        "source_scope": args.source_scope,
        "title": args.title,
        "feishu_doc_url": args.feishu_doc_url,
        "review_status": args.review_status,
        "support_owner": args.support_owner,
        "leader": args.leader,
        "service_representative": args.service_representative,
        "triggered_by": args.triggered_by,
        "contributors": args.contributors,
        "last_updated_by": args.last_updated_by,
        "created_at": created_at,
        "updated_at": updated_at,
        "latest_version": version,
        "latest_snapshot": str(snapshot_path).replace("\\", "/"),
    }
    dump_metadata(metadata_path, metadata)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
