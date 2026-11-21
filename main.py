#!/usr/bin/env python3
"""Publish the contest entry image for 21 November 2026 world news.

The bundled artwork ``bundled_entry.png`` is a single image that sums up the
day's headline story: a Houthi projectile struck Riyadh's tallest skyscraper
and set it ablaze. This program reads that image from the repository root and
writes it verbatim as ``entry.png`` inside the directory named by
``MAKEFUN_OUTPUT_DIR`` (default: ``./output``), refusing to proceed if the
source is missing or exceeds 1 MiB.

The program performs no network access, uses only the Python standard
library, and is fully deterministic: identical input always produces an
identical output file.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

BUNDLED_NAME = "bundled_entry.png"
OUTPUT_NAME = "entry.png"
MAX_BUNDLED_BYTES = 1024 * 1024  # 1 MiB


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    source = repo_root / BUNDLED_NAME

    if not source.is_file():
        print(
            f"error: bundled image not found: {source}",
            file=sys.stderr,
        )
        return 1

    source_size = source.stat().st_size
    if source_size > MAX_BUNDLED_BYTES:
        print(
            f"error: {source} is {source_size} bytes, "
            f"exceeding the {MAX_BUNDLED_BYTES}-byte (1 MiB) limit",
            file=sys.stderr,
        )
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / OUTPUT_NAME

    payload = source.read_bytes()
    destination.write_bytes(payload)

    print(f"wrote {destination.resolve()} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
