#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# /// script
# dependencies = ["prettytable"]
# ///

from argparse import ArgumentParser
import csv
import sys

from prettytable import PrettyTable, TableStyle


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
			yield {str(n): v for n, v in enumerate(row)}


def main():
	parser = ArgumentParser()
	parser.add_argument('-H', '--header', action='store_true')
	parser.add_argument('-d', '--delimiter', default=',')
	parser.add_argument(
		'-b', '--box', action='store_true',
		help='Use Unicode pretty characters instead of plain ASCII table',
	)
	parser.add_argument(
		'--markdown', action='store_true',
		help='Output markdown table',
	)
	parser.add_argument(
		"--html", action="store_true",
		help="Output HTML table",
	)
	parser.add_argument('--sniff', action='store_true')
	parser.add_argument('file', nargs='?', default='-')
	args = parser.parse_args()

	if args.file == "-":
		fd = sys.stdin
	else:
		fd = open(args.file)

	with fd:
		data = list(read_rows(fd, args))

	table = PrettyTable()
	if args.box:
		table.set_style(TableStyle.SINGLE_BORDER)
	elif args.markdown:
		table.set_style(TableStyle.MARKDOWN)
	table.field_names = data[0].keys()
	table.header = args.header
	table.align = "l"

	for row in data:
		table.add_row([row.get(col) for col in table.field_names])

	if args.html:
		print(table.get_html_string())
	else:
		print(table.get_string())


if __name__ == "__main__":
	main()
