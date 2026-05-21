#!/usr/bin/env python3
"""Generate deterministic keys for Feishu knowledge candidates."""

from __future__ import annotations

import argparse
import hashlib
import re


def normalize(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def candidate_key(
    *,
    thread_id: str = "",
    work_order_id: str = "",
    product: str = "",
    module: str = "",
    title: str = "",
    symptom: str = "",
) -> str:
    if thread_id:
        return f"thread:{thread_id.strip()}"
    if work_order_id:
        return f"workorder:{work_order_id.strip().upper()}"

    seed = "|".join(
        normalize(part) for part in (product, module, title, symptom) if part.strip()
    )
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
    return f"hash:{digest}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a knowledge candidate key.")
    parser.add_argument("--thread-id", default="")
    parser.add_argument("--work-order-id", default="")
    parser.add_argument("--product", default="")
    parser.add_argument("--module", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--symptom", default="")
    args = parser.parse_args()
    print(
        candidate_key(
            thread_id=args.thread_id,
            work_order_id=args.work_order_id,
            product=args.product,
            module=args.module,
            title=args.title,
            symptom=args.symptom,
        )
    )


if __name__ == "__main__":
    main()
