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

case $1 in
	duration)
		val=$(mediainfo '--Inform=General;%Duration%' "$2")
		echo $((val / 1000))
		;;

	width)
		mediainfo '--Inform=Video;%Width%' "$2"
		;;

	height)
		mediainfo '--Inform=Video;%Height%' "$2"
		;;

	wxh)
		echo "$("$0" width "$2")x$("$0" height "$2")"
		#mediainfo '--Inform=General;%Duration%' "$2"
		;;

	*)
		usage $EX_USAGE
		exit 1
		;;
esac
