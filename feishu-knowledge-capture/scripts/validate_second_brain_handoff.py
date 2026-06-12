#!/usr/bin/env python3
"""Verify that a Feishu second-brain handoff commit only adds safe candidates."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List


PREFIX = "knowledge-intake/feishu/"
SECRET_PATTERNS = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("generic_secret", re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}")),
]


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def metadata_value(text: str, key: str) -> str:
    match = re.search(r"(?m)^{}\s*:\s*[\"']?([^\"'\r\n]+)".format(re.escape(key)), text)
    return match.group(1).strip().lower() if match else ""


def inspect(repo: Path, base: str, head: str) -> Dict[str, Any]:
    diff = git(repo, "-c", "core.quotepath=false", "diff", "--name-status", base, head)
    if diff.returncode != 0:
        return {"valid": False, "errors": ["cannot_read_diff"], "message": diff.stderr.strip(), "changes": []}
    errors: List[str] = []
    changes: List[Dict[str, Any]] = []
    for line in diff.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status = fields[0]
        path = fields[-1].replace("\\", "/")
        item_errors: List[str] = []
        if status != "A":
            item_errors.append("change_must_be_addition")
        if not path.startswith(PREFIX):
            item_errors.append("path_outside_intake")
        if not path.lower().endswith(".md"):
            item_errors.append("candidate_must_be_markdown")
        content = ""
        shown = git(repo, "show", "{}:{}".format(head, path)) if status != "D" else None
        if shown is None or shown.returncode != 0:
            item_errors.append("cannot_read_candidate")
        else:
            content = shown.stdout
            if metadata_value(content, "type") != "knowledge-candidate":
                item_errors.append("invalid_type")
            if metadata_value(content, "candidate_status") != "pending":
                item_errors.append("candidate_not_pending")
            if metadata_value(content, "status") == "active":
                item_errors.append("candidate_marked_active")
            if metadata_value(content, "confidence") == "verified":
                item_errors.append("candidate_marked_verified")
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(content):
                    item_errors.append("possible_secret:{}".format(name))
        changes.append({"status": status, "path": path, "errors": item_errors})
        errors.extend("{}:{}".format(path, error) for error in item_errors)
    if not changes:
        errors.append("no_changes")
    return {"valid": not errors, "base": base, "head": head, "changes": changes, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    repo = args.repository.resolve()
    if not repo.is_dir():
        parser.error("repository is not a directory: {}".format(repo))
    report = inspect(repo, args.base, args.head)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["valid"]:
        print("第二大脑候选交接验证通过：只新增了安全的 pending 候选。")
    else:
        print("第二大脑候选交接验证失败：{}".format("、".join(report["errors"])))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
