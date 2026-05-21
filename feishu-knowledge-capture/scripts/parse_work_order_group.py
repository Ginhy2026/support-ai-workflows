#!/usr/bin/env python3
"""Parse Feishu support work-order group names into structured metadata."""

from __future__ import annotations

import argparse
import json
import re
from typing import Any


WORK_ORDER_RE = re.compile(r"([A-Z]{2,10}WO-\d{8,})", re.IGNORECASE)
BRACKET_RE = re.compile(r"^【([^】]+)】\s*(.*)$")


def parse_group_name(name: str) -> dict[str, Any]:
    raw = name.strip()
    status = ""
    remainder = raw

    bracket_match = BRACKET_RE.match(raw)
    if bracket_match:
        status = bracket_match.group(1).strip()
        remainder = bracket_match.group(2).strip()

    work_order_match = WORK_ORDER_RE.search(remainder)
    work_order_id = work_order_match.group(1).upper() if work_order_match else ""

    descriptor = remainder
    if work_order_match:
        descriptor = (
            remainder[: work_order_match.start()] + remainder[work_order_match.end() :]
        ).strip(" -_")

    return {
        "raw_name": raw,
        "status": status,
        "descriptor": descriptor,
        "work_order_id": work_order_id,
        "is_work_order_group": bool(work_order_id),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a Feishu support work-order group name."
    )
    parser.add_argument("name", help="Feishu group name to parse")
    args = parser.parse_args()
    print(json.dumps(parse_group_name(args.name), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
