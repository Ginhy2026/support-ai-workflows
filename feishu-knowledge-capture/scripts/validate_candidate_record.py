#!/usr/bin/env python3
"""Validate Feishu knowledge candidate Base records before writing."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_KEY_RE = re.compile(
    r"^(thread:om[ta]?_[A-Za-z0-9]+|workorder:[A-Z0-9_-]+|node:[A-Za-z0-9]+|hash:[0-9a-f]{8,40})$"
)
LEGACY_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{3,}$")

EMPTY_VALUES = {"", "-", "待确认", "unknown", "null", "none"}


def load_fields(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    fields = payload.get("fields", payload)
    if not isinstance(fields, dict):
        raise ValueError("payload.fields must be a JSON object")
    return fields


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in EMPTY_VALUES
    return False


def validate_candidate_key(value: Any, *, allow_legacy: bool = False) -> list[str]:
    if is_empty(value):
        return ["唯一键 is required and cannot be blank"]
    if not isinstance(value, str):
        return ["唯一键 must be a string"]
    candidate_key = value.strip()
    if not VALID_KEY_RE.fullmatch(candidate_key):
        if allow_legacy and LEGACY_KEY_RE.fullmatch(candidate_key):
            return []
        return [
            "唯一键 must use thread:<thread_id>, workorder:<JSWO-id>, "
            "node:<wiki_node_token>, or hash:<sha1>"
        ]
    return []


def validate_fields(fields: dict[str, Any], *, allow_legacy: bool = False) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_candidate_key(fields.get("唯一键"), allow_legacy=allow_legacy))

    source_thread = fields.get("来源 thread")
    if isinstance(source_thread, str) and source_thread.strip().startswith("thread:"):
        errors.append("来源 thread should contain the raw thread/message id, not the prefixed 唯一键")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a candidate Base record JSON file.")
    parser.add_argument("json_file", help="Path to candidate-base-record.json")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--allow-legacy",
        action="store_true",
        help="Allow existing non-prefixed legacy keys while repairing old records.",
    )
    args = parser.parse_args()

    try:
        fields = load_fields(Path(args.json_file))
        errors = validate_fields(fields, allow_legacy=args.allow_legacy)
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    result = {"ok": not errors, "errors": errors}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print("OK")

    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
