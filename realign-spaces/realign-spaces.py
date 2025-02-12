#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import locale
import os
from pathlib import Path
import signal
import sys
import shlex
import shutil
import tempfile

__version__ = "0.1.0"


def process(args, splitfunc, quotefunc):
    data = []
    width = []
    for line in args.file:
        data.append([quotefunc(part) for part in splitfunc(line)])

        linewidth = [len(part) for part in data[-1]]
        width.extend([0] * (len(data[-1]) - len(width)))
        for n, partwidth in enumerate(linewidth):
            width[n] = max(width[n], partwidth)

    outfile = sys.stdout
    if args.inplace:
        outfile = tempfile.NamedTemporaryFile("w+", encoding="utf8", dir=Path(args.file.name).parent)

    for lineparts in data:
        line = " ".join(f"{part:{width[n]}s}" for n, part in enumerate(lineparts))
        line = line.strip()
        print(line, file=outfile)

    if args.inplace:
        # we want to copy permissions etc. but still mark file as modified now
        shutil.copystat(args.file.name, outfile.name)
        os.utime(outfile.name)
        os.replace(outfile.name, args.file.name)


def main():
    locale.setlocale(locale.LC_ALL, "")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type=argparse.FileType(mode="r"), nargs="?", default=sys.stdin,
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--shell-split", action="store_true",
    )
    parser.add_argument(
        "-i", "--inplace", action="store_true",
    )
    args = parser.parse_args()

    if args.file is sys.stdin:
        args.inplace = False

    with args.file:
        if args.shell_split:
            process(args, shlex.split, shlex.quote)
        else:
            process(args, str.split, str)


if __name__ == "__main__":
    main()
