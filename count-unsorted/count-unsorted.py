#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# count-unsorted: like uniq(1)'s -c but does not require lines to be sorted

import signal
import sys
from argparse import ArgumentParser
from collections import Counter
from fileinput import input


signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def reversed_by_count(iterator):
    # most_common return DESC for count, and ASC for occurence order with same
    # count.
    # so if we want ASC for count and we simply use reversed(), it will be
    # DESC for occurence order as a side-effect!
    # hence this function that reverses (again) occurence order if same count
    group = []
    for key, count in iterator:
        if not group or group[0][1] == count:
            group.append((key, count))
            continue

        yield from reversed(group)
        group = [(key, count)]

    yield from reversed(group)


parser = ArgumentParser()
parser.add_argument(
    "-S", "--no-sort", action="store_false", default=True, dest="sort",
    help="Sort in reverse (descending) order",
)
parser.add_argument(
    "-r", "--reverse", action="store_true", dest="desc",
    help="Sort in reverse (descending) order",
)
parser.add_argument("files", nargs="*")
args = parser.parse_args()

counter = Counter()

# open in binary because:
# - we don't care about their encoding
# - it avoids errors because of an incorrect setting
# - it's faster if we avoid decoding/encoding
# it won't work with utf-16 though
for line in input(args.files, mode="rb"):
    counter[line] += 1

if args.sort:
    elems = counter.most_common()
    if not args.desc:
        elems = reversed_by_count(reversed(elems))
else:
    elems = counter.items()

for line, count in elems:
    # input() keeps newlines, so don't append one
    sys.stdout.buffer.write(f"{count}: ".encode() + line)
