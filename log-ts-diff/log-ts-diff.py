#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL
# parse log and replace timestamps with diff to previous timestamp

# /// script
# dependencies = ["python-dateutil"]
# ///

import argparse
import datetime
from fileinput import input
import re

from dateutil.parser import parse as parse_base
from dateutil.relativedelta import relativedelta


def parse(line):
    # permissive various formats:
    # 2021-05-16T19:50:42
    # 2021-05-16 19:50:42,123
    # 2021-05-16 19:50:42+0200
    m = re.match(r'[\dT\s:,.Z+-]+', line)
    if not m:
        # format: May 16 19:50:42
        m = re.match(r'[A-Za-z]+\s+\d{1,2}\s+\d\d:\d\d(:\d\d)?\s', line)
        if not m:
            return {}

    try:
        ts, toks = parse_base(m[0], fuzzy_with_tokens=True)
    except ValueError:
        return {}

    return {
        'timestamp': ts,
        'rest': (''.join(toks) + line[m.end():]).strip(),
    }


def duration_to_str(duration):
    attrs = {
        'years': 'y',
        'months': 'mo',
        'days': 'd',
        'hours': 'h',
        'minutes': 'm',
    }
    parts = []
    for attr in attrs:
        factor = getattr(duration, attr)
        if factor:
            parts.append(f'{factor:=+2d}{attrs[attr]}')

    if duration.microseconds:
        secs = duration.seconds + duration.microseconds / 1_000_000
        parts.append(f'{secs:=+7.3f}s')
    elif duration.seconds:
        parts.append(f'{duration.seconds:=+3d}s')

    if not parts:
        parts.append('+0')

    return ', '.join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="parse log and replace timestamps with diff to previous timestamp",
    )
    args = parser.parse_args()

    old_time = None

    for line in input():
        line = line.rstrip()
        info = parse(line.lstrip())

        if not info:
            print(line)
            continue

        time = info['timestamp']
        if not old_time:
            old_time = time
            print(line)
            continue

        print(duration_to_str(relativedelta(time, old_time)), info['rest'])

        old_time = time


if __name__ == '__main__':
    main()
