#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./elidelong "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init -l 4 <<- EOF
	a
	bc
	def
	ghij
	klmno
	pqrstu
	vwxyz

	012345
EOF

check <<- EOF
	a
	bc
	def
	ghij
	klmn
	pqrs
	vwxy

	0123
EOF
