#!/usr/bin/env python3
# license: Do What The Fuck You Want To Public License version 2 [http://www.wtfpl.net/]

from argparse import ArgumentParser
import sys

from PyQt5.QtGui import QClipboard, QGuiApplication


def get_clips_of_mode(mode):
	ret = {}

	qmime = clipboard.mimeData(mode)
	for mime in qmime.formats():
		ret[mime] = bytes(qmime.data(mime))
	return ret


def do_mode(mode):
	all_data = get_clips_of_mode(mode)
	if args.mime:
		try:
			data = all_data[args.mime]
		except KeyError:
			pass
		else:
			sys.stdout.buffer.write(data)
	else:
		for mime in all_data:
			if mime.startswith("text"):
				print(f"{mime}: {all_data[mime].decode()}")
			else:
				print(f"{mime}: {all_data[mime]!r}")


parser = ArgumentParser()
parser.add_argument(
	"--clipboard", action="store_true",
	help="Use clipboard (the default)",
)
parser.add_argument(
	"--selection", action="store_true",
	help="Use X11 selection",
)
parser.add_argument(
	"--mime",
	help="Only display clipboard data with type MIME (instead of everything)",
)

args = parser.parse_args()

if not (args.clipboard or args.selection):
	args.clipboard = True
if args.clipboard and args.selection and args.mime:
	parser.error("cannot pass --mime when both --clipboard and --selection are passed")

app = QGuiApplication([])
clipboard = app.clipboard()

if args.clipboard:
	do_mode(QClipboard.Clipboard)
if args.selection:
	do_mode(QClipboard.Selection)
