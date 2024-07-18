#!/bin/sh -eu

cd "$(dirname "$0")"

tmpd=$(mktemp -d "${TMPDIR:-/tmp}/zerotest.XXXXXX")
printf "foo\0" > "$tmpd/file"

for arg
do
	case $arg in
		find)
			./zeropipe find "$tmpd" > /dev/null
			;;
		locate)
			./zeropipe locate / > /dev/null
			;;
		xargs)
			./zeropipe xargs echo < "$tmpd/file" > /dev/null
			;;
		basename|dirname)
			./zeropipe "$arg" /foo/bar > /dev/null
			;;
		grep)
			./zeropipe grep foo "$tmpd/file" > /dev/null
			;;
		sort|uniq|head|tail)
			./zeropipe "$arg" "$tmpd/file" > /dev/null
			;;
		sed)
			./zeropipe sed -n s/foo/bar/ "$tmpd/file"
			;;
		ls)
			./zeropipe ls "$tmpd" > /dev/null
			;;
		fzf)
			./zeropipe fzf -1 < "$tmpd/file" > /dev/null
			;;
	esac
done
