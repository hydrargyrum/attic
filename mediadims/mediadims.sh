#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

EX_USAGE=64

usage () {
	echo "usage: $0 [duration | width | height | wxh] FILE" >&2
	exit $1
}

if [ $# -ne 2 ]
then
	usage $EX_USAGE
fi

if command -v ffprobe >/dev/null 2>&1
then

	ffq () {
		ffprobe -loglevel error -show_"$1" -output_format flat "$3" | grep -F ".$2=" | head -1 | sed -e 's/.*=//' -e 's/"//g' | grep .
	}

	case $1 in
		duration)
			ffq format duration "$2"
			;;

		width)
			ffq streams width "$2"
			;;

		height)
			ffq streams height "$2"
			;;

		wxh)
			echo "$("$0" width "$2")x$("$0" height "$2")"
			;;

	esac

elif command -v mediainfo >/dev/null 2>&1
then

	case $1 in
		duration)
			val=$(mediainfo '--Inform=General;%Duration%' "$2")
			echo $((val / 1000))
			;;

		# mediainfo can extract static image dimensions, but we can't query both
		# at the same time
		width)
			mediainfo '--Inform=Video;%Width%' "$2"
			;;

		height)
			mediainfo '--Inform=Video;%Height%' "$2"
			;;

		wxh)
			echo "$("$0" width "$2")x$("$0" height "$2")"
			;;

		*)
			usage $EX_USAGE
			exit 1
			;;
	esac

else
	echo "error: $0 requires at least mediainfo or ffprobe to be installed" >&2
	exit 1
fi
