#!/usr/bin/env python3
"""THE WORLD TODAY — front page for Wednesday 18 November 2026.

This program writes the finished front page to the output directory. The
page itself is the committed file entry.png next to this script; it was
composed ahead of time from verified reporting on the full day of
18 November 2026 (Gulf war widening, the APEC summit in Shenzhen, and
Cyclone Xavier over the northern Cook Islands) plus 35 further stories.

Stdlib only. The output is deterministic: the same committed bytes are
copied on every run, and the copy is verified byte-for-byte before exit.
"""

import hashlib
import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def png_dimensions(data):
    """Read width and height out of a PNG's IHDR chunk (stdlib only)."""
    if data[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_entry(data):
    """Refuse to ship anything that is not exactly one 1024x1024 image."""
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit"
        )
    width, height = png_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(f"entry.png is {width}x{height}, expected 1024x1024")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    with open(SOURCE, "rb") as f:
        data = f.read()
    check_entry(data)

    dest = output_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)

    with open(dest, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        raise ValueError("output does not match the committed entry.png")

    print(f"wrote {dest} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
