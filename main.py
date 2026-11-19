#!/usr/bin/env python3
"""Entry point for news-image-20261119.

Copies the pre-rendered front-page image (entry.png, sitting next to
this file) to the output directory as entry.png.

Respects MAKEFUN_OUTPUT_DIR when set, otherwise writes to /output.
Standard library only; no network; fully deterministic.
The image is shipped in the repo; the program never draws at grade time.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
