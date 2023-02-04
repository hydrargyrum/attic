#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

cd "$(dirname "$0")"

tmp1=$(mktemp test.XXXXXX)
tmp2=$(mktemp test.XXXXXX)

trap 'rm -f "$tmp1" "$tmp2"' EXIT

# check stdin = stdout
seq 10 > "$tmp1"
seq 10 | ./catsponge > "$tmp2"
diff -u "$tmp1" "$tmp2"

# check stdout is not written before EOF is reached
: > "$tmp1"
: > "$tmp2"
{
	# big size to make sure the pipe content is not buffered
	seq 50000
	sleep 1
	if [ -s "$tmp1" ]
	then
		echo "$tmp1 should be empty" >&2
		echo fail > "$tmp2"  # poor man's pipefail
		exit 1
	fi
} | ./catsponge > "$tmp1"

if [ -s "$tmp2" ]
then
	exit 1
fi

[ -s "$tmp1" ]
