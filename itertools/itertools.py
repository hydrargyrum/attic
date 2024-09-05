#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import csv
import itertools
import json
import locale
import signal
import sys


def output_csv(iterable, args):
    writer = csv.writer(sys.stdout)

    it = iter(iterable)
    row = next(it)
    writer.writerow(f"{args.column_prefix}{i}" for i in range(len(row)))  # header
    writer.writerow(row)
    for row in it:
        writer.writerow(row)


def output_plain(iterable, args):
    for row in iterable:
        print(*row)


def output_json(iterable, args):
    print("[")
    first = True
    for row in iterable:
        if not first:
            print(",")

        print(json.dumps(list(row)), end="")
        first = False
    print()
    print("]")


def main():
    locale.setlocale(locale.LC_ALL, "")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--out-plain", action="store_const", dest="output_func", const=output_plain,
        help="Output rows as space-separated entries"
    )
    group.add_argument(
        "--out-csv", action="store_const", dest="output_func", const=output_csv,
        help="Output rows as CSV",
    )
    group.add_argument(
        "--out-json", action="store_const", dest="output_func", const=output_json,
        help="Output rows as JSON",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--permutations", action="store_true",
        help="Compute permutations of ARGS",
    )
    group.add_argument(
        "--combinations", type=int, metavar="N",
        help="Compute combinations of N elements of ARGS",
    )

    parser.add_argument(
        "--column-prefix", default="col_",
        help="Column name prefix for CSV",
    )
    parser.add_argument(
        "args", nargs="+",
        help="Entries on which to operate",
    )
    args = parser.parse_args()

    if args.permutations:
        args.output_func(itertools.permutations(args.args), args)
    elif args.combinations:
        args.output_func(itertools.combinations(args.args, args.combinations), args)


if __name__ == "__main__":
    main()
