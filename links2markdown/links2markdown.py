#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import re
import signal
import sys
from html.parser import HTMLParser

import requests


LINK_RE = re.compile(r"""https?://[^])'">\s]+""")


class TitleFetchParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = []
        self.title = None

    def handle_starttag(self, tag, attrs):
        self.path.insert(0, tag)

    def handle_endtag(self, tag):
        try:
            idx = self.path.index(tag)
        except ValueError:
            return
            raise AssertionError(f"{self.path[0]!r} != {tag!r}")
        del self.path[:idx + 1]

    def handle_data(self, data):
        if self.title:
            return

        if self.path and self.path[0] == "title" and "head" in self.path:
            self.title = data


def fetch_title(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
            },
            timeout=120,
        )
    except requests.exceptions.RequestException:
        return None

    parser = TitleFetchParser(convert_charrefs=True)

    try:
        parser.feed(response.text)
        parser.close()
    except AssertionError as exc:
        print(f"failed on {url}: {exc}", file=sys.stderr)
        return None
    else:
        return parser.title


def link_to_markdown(m):
    url = m[0]

    if m.start() > 2 and m.string[m.start() - 1] == "(" and m.string[m.start() - 2] == "]":
        return url

    title = fetch_title(url) or url
    title = re.sub(r"\s+", " ", title.strip())

    return f"[{title}]({url})"


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument("file", default="-", nargs="?")
    args = parser.parse_args()

    if args.file == "-":
        fp = sys.stdin
    else:
        fp = open(args.file)

    with fp:
        for line in fp:
            line = LINK_RE.sub(link_to_markdown, line)
            print(line, end="")


if __name__ == "__main__":
    main()
