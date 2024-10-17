#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import json
import locale
import signal
import sys

import yaml

__version__ = "0.2.0"


def main():
    locale.setlocale(locale.LC_ALL, "")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser(
        description="Convert YAML to JSON",
    )
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="Read all YAML documents (separated by '---') and return them in a list",
    )
    parser.add_argument(
        "file", type=argparse.FileType(mode="r"), nargs="?", default=sys.stdin,
        help="input YAML file",
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    if args.file.isatty():
        print(f"warning: {parser.prog} program is reading stdin", file=sys.stderr)

    with args.file:
        if args.all:
            data = list(yaml.safe_load_all(args.file))
        else:
            data = yaml.safe_load(args.file)

    json.dump(data, sys.stdout)
    print()  # final newline


if __name__ == "__main__":
    main()
