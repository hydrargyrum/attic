#!/usr/bin/env python3

# /// script
# dependencies = ["lz4"]
# ///

import argparse
import locale
import signal
import sys

import lz4.block
import lz4.frame


__version__ = "0.1.0"


def do_block(args, in_fp, out_fp):
    data = in_fp.read()
    if args.moz:
        data = data[8:]
    data = lz4.block.decompress(data)
    out_fp.write(data)


def do_frame(args, in_fp, out_fp):
    with lz4.frame.LZ4FrameDecompressor() as decompressor:
        while True:
            buf = in_fp.read(10240)
            if not buf:
                break
            buf = decompressor.decompress(buf)
            out_fp.buffer.write(buf)


def main():
    locale.setlocale(locale.LC_ALL, "")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--block", action="store_true",
        help="Extract 'block' LZ4 instead of 'frame' LZ4",
    )
    parser.add_argument(
        "--moz", action="store_true",
        help="Extract Mozilla .jsonlz4 files",
    )
    parser.add_argument(
        "file", type=argparse.FileType(mode="rb"), nargs="?",
        default=sys.stdin.buffer,
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    if args.file.isatty():
        print(f"warning: {parser.prog} is reading stdin", file=sys.stderr)

    proc_func = do_frame
    if args.block:
        proc_func = do_block

    with args.file:
        proc_func(args, args.file, sys.stdout.buffer)


if __name__ == "__main__":
    main()
