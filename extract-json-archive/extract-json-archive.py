#!/usr/bin/env python3

import argparse
import base64
import json
import locale
import os
from pathlib import Path
import signal
import sys


__version__ = "0.1.0"


def has_colors(fp=sys.stdout):
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("CLICOLOR_FORCE") or os.environ.get("FORCE_COLOR"):
        return True
    return fp.isatty()


def to_path(root: Path, name: str) -> Path:
    name = os.path.normpath(name)
    if name.startswith("/") or name.startswith(".."):
        raise ValueError(f"cannot evade {root}")
    result = root / name
    result = result.resolve()
    if result.relative_to(root) == Path("."):
        raise ValueError(f"cannot evade {root}")
    return result


def test_to_path():
    import pytest
    assert to_path(Path("/foo"), "bar/baz") == Path("/foo/bar/baz")

    for invalid in ["/bar", "../bar", "bar/../..", "."]:
        with pytest.raises(ValueError):
            print(to_path(Path("/foo"), invalid))


def main():
    locale.setlocale(locale.LC_ALL, "")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", type=Path, default=Path.cwd(),
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "file", type=argparse.FileType(mode="r"), nargs="?",
        default=sys.stdin,
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    if args.file.isatty():
        print(f"warning: {parser.prog} is reading stdin", file=sys.stderr)

    with args.file:
        jdata = json.load(args.file)

    args.output = args.output.resolve()
    for entry in jdata:
        print(f"Extracting {entry['filename']!r}")
        target = to_path(args.output, entry["filename"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(entry["data"]))


if __name__ == "__main__":
    main()
