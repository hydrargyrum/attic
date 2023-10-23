#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import json
import locale
import signal
import subprocess
import shutil
import sys


def mediainfo_json(file: str) -> dict:
    return json.loads(
        subprocess.check_output(
            ["mediainfo", "--Output=JSON", file],
            encoding="utf-8",
        )
    )


def from_tracks(tracks, key):
    return list(filter(None, (track.get(key) for track in tracks)))


TRACK_SORT_KEY = {
    "General": 0,
    "Video": 1,
    "Audio": 2,
    "Image": 3,
}


def track_sort_key(track):
    return TRACK_SORT_KEY.get(track["@type"], 100)


def main():
    locale.setlocale(locale.LC_ALL, '')

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument("info", choices=["duration", "width", "height", "wxh"])
    parser.add_argument("file")
    args = parser.parse_args()

    if not shutil.which("mediainfo"):
        sys.exit("error: 'mediainfo' command could not be found")

    metadata = mediainfo_json(args.file)
    tracks = metadata["media"]["track"]
    tracks.sort(key=track_sort_key)  # useless? who knows

    if args.info == "duration":
        print(from_tracks(tracks, "Duration")[0])
    elif args.info == "width":
        print(from_tracks(tracks, "Width")[0])
    elif args.info == "height":
        print(from_tracks(tracks, "Height")[0])
    elif args.info == "wxh":
        width = from_tracks(tracks, "Width")[0]
        height = from_tracks(tracks, "Height")[0]
        print(f"{width}x{height}")


if __name__ == "__main__":
    main()
