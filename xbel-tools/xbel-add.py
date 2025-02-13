#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# /// script
# dependencies = ["lxml"]
# ///

import argparse
import datetime
import locale
import mimetypes
import os
from pathlib import Path
import sys

import lxml.etree


def xdg_share():
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))


DEFAULT_PATH = xdg_share() / "recently-used.xbel"


def add_bookmark(url, xbel):
    when_add = datetime.datetime.now(datetime.timezone.utc)
    bookmark = lxml.etree.SubElement(xbel, "bookmark")
    bookmark.attrib["href"] = url
    bookmark.attrib["added"] = (
        when_add.isoformat("T").replace("+00:00", "Z")
    )
    bookmark.attrib["modified"] = bookmark.attrib["added"]
    bookmark.attrib["visited"] = bookmark.attrib["added"]

    info = lxml.etree.SubElement(bookmark, "info")

    metadata = lxml.etree.SubElement(info, "metadata")
    metadata.attrib["owner"] = "http://freedesktop.org"

    mime = lxml.etree.SubElement(
        metadata,
        "{http://www.freedesktop.org/standards/shared-mime-info}mime-type",
    )
    try:
        mime.attrib["type"] = mimetypes.guess_type(url)[0]
    except (TypeError, IndexError):
        mime.attrib["type"] = "application/octet-stream"

    # not sure if all of this is required, but it seems apps tend to discard
    # the whole XBEL if some of it is missing...
    apps = lxml.etree.SubElement(
        metadata,
        "{http://www.freedesktop.org/standards/desktop-bookmarks}applications",
    )
    app = lxml.etree.SubElement(
        apps,
        "{http://www.freedesktop.org/standards/desktop-bookmarks}application",
    )
    app.attrib["name"] = "xbel-add"
    app.attrib["exec"] = "false"
    app.attrib["modified"] = bookmark.attrib["added"]
    app.attrib["count"] = "1"


def main():
    locale.setlocale(locale.LC_ALL, "")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=Path,
        help="Path to add as recently used in XBEL file",
    )
    parser.add_argument(
        "--xbel", default=DEFAULT_PATH,
        help=f"Path of XBEL file (default: {DEFAULT_PATH})",
    )
    args = parser.parse_args()

    args.path = args.path.resolve()

    if args.xbel == "-":
        fp = sys.stdin
    else:
        fp = open(args.xbel)

    with fp:
        tree = lxml.etree.parse(fp)

    root = tree.getroot()
    if root.tag != "xbel":
        sys.exit(f"error: expect 'xbel' root tag, got {xbel.tag!r}")

    add_bookmark(args.path.as_uri(), root)

    if args.xbel == "-":
        tree.write(sys.stdout.buffer)
    else:
        tree.write(args.xbel)


if __name__ == "__main__":
    main()
