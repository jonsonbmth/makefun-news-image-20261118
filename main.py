#!/usr/bin/env python3
"""Entry for make.fun news-image-20261118: one image, one day of world news.

The front page for Wednesday 18 November 2026 ("THE WORLD TODAY") is
composed ahead of time by build_page.py and stored in this repository as
entry.png (1024x1024, under 1 MiB). This program is the entrypoint the
harness runs: it copies that exact image to the output directory.

Deterministic by construction: a pure byte copy of a fixed file, so two
runs produce byte-identical output. Standard library only, no network.
"""

import hashlib
import os
import shutil
import struct
import sys

IMAGE_NAME = "entry.png"
EXPECTED_SIZE = (1024, 1024)
MAX_BYTES = 1_048_576  # 1 MiB, the competition limit


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _png_dimensions(path):
    """Read width/height from a PNG header without any image library."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path}: missing IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(source):
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    width, height = _png_dimensions(source)
    if (width, height) != EXPECTED_SIZE:
        print(f"error: {source} is {width}x{height}, "
              f"expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    if os.path.getsize(target) > MAX_BYTES:
        print(f"error: {target} exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    if _sha256(target) != _sha256(source):
        print(f"error: {target} does not match {source}", file=sys.stderr)
        return 1
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
