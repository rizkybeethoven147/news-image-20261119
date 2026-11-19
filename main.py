#!/usr/bin/env python3
"""Write the one-image world news brief for 19 November 2026.

The finished image lives in this repository as `entry.png`. This program copies
it into /out so every run writes the same bytes. The runtime is Python 3.13
standard library only: no network, no clock, no randomness, no packages.
"""
import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"news brief: missing {SOURCE}")

    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"news brief: wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
