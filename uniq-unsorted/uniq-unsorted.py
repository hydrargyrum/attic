#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# uniq-unsorted: like uniq(1) but does not require lines to be sorted

import sys
from fileinput import input


seen = set()

# open in binary because:
# - we don't care about their encoding
# - it avoids errors because of an incorrect setting
# - it's faster if we avoid decoding/encoding
# it won't work with utf-16 though
for line in input(mode="rb"):
    if line in seen:
        continue

    # input() keeps newlines, so don't append one
    sys.stdout.buffer.write(line)
    seen.add(line)
