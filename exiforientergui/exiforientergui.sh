#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

die () {
	printf "%s\n" "$*" >&2
	exit 1
}

[ $# -eq 1 ] || die "usage: $0 IMAGE"
which montage >/dev/null 2>/dev/null || die "imagemagick is not installed"

# main
sz=300
img=$1

montage \
	-gravity center \
	-pointsize 64 \
	"$img" -resize "${sz}x${sz}>"  \
	\( -clone 0 -auto-orient -set label Current \) \
	\( -clone 0 -set label 1 \) \
	\( -clone 0 -rotate 180 -set label 2 \) \
	\( -clone 0 -rotate 90 -set label 3 \) \
	\( -clone 0 -rotate 270 -set label 4 \) \
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
	--column "Orientation" \
	--column "Image" \
	--hide-column=1 \
	TopLeft 1 BottomRight 2 RightTop 3 LeftBottom 4
)
# correspond to 1 3 6 8 in exif
if [ -n "$orientation" ]
then
	mogrify -orient "$orientation" "$img"
fi

