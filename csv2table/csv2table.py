#!/usr/bin/env python3
# license: WTFPLv2 [http://www.wtfpl.net/]

from argparse import ArgumentParser
from collections import OrderedDict
import csv
import sys

from prettytable import PrettyTable


def sniff(fn):
	with open(fn) as fd:
		sn = csv.Sniffer()
		return sn.sniff(fd.read(1024))


def read_rows(fd, args):
	if args.header:
		for row in csv.DictReader(fd, delimiter=args.delimiter):
			yield row
	else:
		for row in csv.reader(fd, delimiter=args.delimiter):
			yield OrderedDict((str(n), v) for n, v in enumerate(row))


def main():
	parser = ArgumentParser()
	parser.add_argument('--header', action='store_true')
	parser.add_argument('-d', '--delimiter', default=',')
	parser.add_argument('--sniff', action='store_true')
	parser.add_argument('file')
	args = parser.parse_args()

	with open(args.file) as fd:
		data = list(read_rows(fd, args))
	table = PrettyTable()
	for row in data:
		table.add_row(row)
	print(table)

main()
