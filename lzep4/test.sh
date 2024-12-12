#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp lzep4.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./lzep4.py "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
printf '\025\000\000\000\033A\001\000PAAAA\n' | init --block

echo AAAAAAAAAAAAAAAAAAAA | check
