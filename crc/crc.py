#!/usr/bin/env python3
# license: Do What The Fuck You Want To Public License version 2 [http://www.wtfpl.net/]

from binascii import crc32, crc_hqx
import sys
from argparse import ArgumentParser


def out_hex(v):
    print('%x' % v)


def out_dec(v):
    print(v)


parser = ArgumentParser()

parser.add_argument(
    '--hex', action='store_const', dest='print', const=out_hex,
    help="Display CRC value as hexadecimal",
)

fgroup = parser.add_mutually_exclusive_group()
parser.add_argument(
    '-2', '--crc16',
    help="Perform CRC-CCITT algorithm with 16 bits output",
    dest='fn', action='store_const', const=crc_hqx,
)
fgroup.add_argument(
    '-4', '--crc32',
    help="Perform CRC32 algorithm with 32 bits output (default)",
    dest='fn', action='store_const', const=crc32,
)
parser.set_defaults(fn=crc32, print=out_dec)

args = parser.parse_args()

crc = args.fn

v = crc(b'', 0)
while True:
    buf = sys.stdin.buffer.read(512)
    if not buf:
        break
    v = crc(buf, v)
v = v & 0xffffffff

args.print(v)
