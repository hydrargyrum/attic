#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

die () {
	printf "%s\n" "$*" >&2
	exit 1
}

[ $# -eq 1 ] || die "usage: $0 IMAGE"
which exiftool >/dev/null 2>/dev/null || die "exiftool is not installed"

# main
sz=300
img=$1

montage \
	-gravity center \
	-pointsize 64 \
	"$img" -resize "${sz}x${sz}>"  \
	\( -clone 0 -auto-orient -set label Current \) \
	\( -clone 0 -set label 1 \) \
	\( -clone 0 -rotate 180 -set label 3 \) \
	\( -clone 0 -rotate 90 -set label 6 \) \
	\( -clone 0 -rotate 270 -set label 8 \) \
	-delete 0 \
	-tile 5x \
	-geometry "${sz}x${sz}+0+0" \
	x: &
# passing $img each time would reread and resize the file 5 times
# so using -clone is much faster
imgpid=$!

trap 'kill $imgpid' EXIT

sleep 1
orientation=$(zenity --list \
	--text "Choose orientation" \
	--column "Orientation" 1 3 6 8
)
if [ "$orientation" -gt 0 ]
then
	exiftool -n -Orientation="$orientation" "$img"
fi

