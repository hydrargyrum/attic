#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import re
import sys

from prettytable import PrettyTable, SINGLE_BORDER


# TODO: accept ANSI-colored entries, where width != number of codepoints

lines = sys.stdin.read().strip("\n").split("\n")
splitpoints = [
	{mtc.start() for mtc in re.finditer(r"^\S|(?<=\s)\S", line)}
	for line in lines
]
intersect = splitpoints[0]
for sp in splitpoints[1:]:
	intersect &= sp

intersect = sorted(intersect)


def split_at(line, points):
	ret = []
	for a, b in zip(points, points[1:]):
		ret.append(line[a:b])
	ret.append(line[b:])
	return ret


table = PrettyTable([cell.strip() for cell in split_at(lines[0], intersect)])
table.set_style(SINGLE_BORDER)
for line in lines[1:]:
	table.add_row([cell.strip() for cell in split_at(line, intersect)])
print(table)
