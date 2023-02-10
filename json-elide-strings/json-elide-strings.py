#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

from argparse import ArgumentParser
import json
import sys


def elide(s, n):
    if len(s) > n:
        # don't pass a negative index
        return s[:max(0, n - len(options.suffix))] + options.suffix
    return s


def elide_strings(node):
    if isinstance(node, dict):
        return {
            elide_strings(key) if options.keys else key: elide_strings(value)
            for key, value in node.items()
        }
    elif isinstance(node, list):
        return [elide_strings(value) for value in node]
    elif isinstance(node, str):
        return elide(node, options.length)
    return node


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--keys", action="store_true", help="also truncate dictionary keys (this may lead to key collisions)")
    parser.add_argument("-l", "--length", type=int, default=15)
    parser.add_argument("--suffix", default="...")
    parser.add_argument("file", default="-", nargs="?")
    options = parser.parse_args()

    if options.file == "-":
        fp = sys.stdin
    else:
        fp = open(options.file)

    with fp:
        data = json.load(fp)
    data = elide_strings(data)
    print(json.dumps(data, indent=2))
