#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

die () {
	printf "%s\n" "$*" >&2
	exit 1
}

if [ $# -ne 1 ] || [ "$1" = -h ]
then
	die "usage: $0 IMAGE"
fi
command -v montage >/dev/null 2>/dev/null || die "error: imagemagick is not installed"

[ -f "$1" ] || die "error: $1 is not a file"

# main
sz=300
img=$1

tmpd=$(mktemp -d ${TMPDIR:-/tmp}/exiforienter.XXXXXX)
trap 'rm -rf "$tmpd"' EXIT

convert "$img" -resize "${sz}x${sz}>" -auto-orient "$tmpd/0.png"
convert "$img" -resize "${sz}x${sz}>" "$tmpd/1.png"
convert "$tmpd/1.png" -rotate 180 "$tmpd/2.png"
convert "$tmpd/1.png" -rotate 90 "$tmpd/3.png"
convert "$tmpd/1.png" -rotate 270 "$tmpd/4.png"

orientation=$({
	# correspond to 1 3 6 8 in exif
	cat <<- EOF
		$tmpd/0.png
		nothing
		$tmpd/1.png
		TopLeft
		$tmpd/2.png
		BottomRight
		$tmpd/3.png
		RightTop
		$tmpd/4.png
		LeftBottom
	EOF
} | zenity --list \
	--imagelist \
	--width=$(( sz + 100 )) \
	--height=$(( sz + sz / 2 )) \
	--title "EXIF orienter GUI" \
	--text "Choose orientation" \
	--column "Image" \
	--column "Orientation" \
	--hide-column 2 \
	--print-column 2 \
	2>/dev/null
)

if [ "$orientation" != nothing ]
then
	mogrify -orient "$orientation" "$img"
fi
