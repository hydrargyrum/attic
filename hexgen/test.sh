#!/bin/sh -e

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./hexgen > "$got"
}

check () {
	h=$(md5sum "$got" | sed 's/ .*//')
	if [ "$h" != "$1" ]
	then
		echo "expected $1, got $h"
		return 1
	fi
}


init <<- EOF
	00 00 00 00 00
	00 00 00 00 00
EOF
check a63c90cc3684ad8b0a2176a6a8fe9005

init <<- EOF
	0000000000
	0
	0 0
	0 000 0 0 0
EOF
check a63c90cc3684ad8b0a2176a6a8fe9005

init <<- EOF
	000
	10
	20
	30
	40
	50
	6
EOF
check 9aa461e1eca4086f9230aa49c90b0c61
