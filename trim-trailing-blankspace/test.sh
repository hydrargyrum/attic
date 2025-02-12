#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

cd "$(dirname "$0")"

got=$(mktemp trim.XXXXXX)
trap 'rm "$got"' EXIT

init () {
	./trim-trailing-blankspace "$@" > "$got"
}

check () {
	diff -u - "$got"
}

printf "foo\n\n  b a r\n baz   \t\nqux \n" | init
printf "foo\n\n  b a r\n baz\nqux\n" | check

# test without newline at EOF
printf "foo\n\n  b a r\n baz   \t\nqux " | init
printf "foo\n\n  b a r\n baz\nqux" | check

