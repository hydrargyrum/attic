#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# uniq-unsorted: like uniq(1) but does not require lines to be sorted

import signal
import sys
from fileinput import input


seen = set()


signal.signal(signal.SIGINT, signal.SIG_DFL)

# open in binary because:
# - we don't care about their encoding
# - it avoids errors because of an incorrect setting
# - it's faster if we avoid decoding/encoding
# it won't work with utf-16 though
for line in input(mode="rb"):
    if line in seen:
        continue

    # input() keeps newlines, so don't append one
    try:
        sys.stdout.buffer.write(line)
    except BrokenPipeError:
        # BrokenPipeError is when stdout is piped and the process exits
        # but when we exit(), python will try to flush stdout and raise
        # another error...
        # so we make it fail now, under our control, so it doesn't fail later
        try:
            sys.stdout.close()
        except BrokenPipeError:
            pass
        break

    seen.add(line)
