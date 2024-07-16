#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp vhd.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./vhd "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	foo bar
	baz é
EOF

check <<- EOF
	f  o  o  sp b  a  r  \n
	b  a  z  sp C3 A9 \n
EOF

# lines
init -L <<- EOF
	foo bar
	baz é
EOF

check <<- EOF
	00000001 f  o  o  sp b  a  r  \n
	00000002 b  a  z  sp C3 A9 \n
EOF

# hex lines
init --line-addresses <<- EOF
	foo bar
	baz é
EOF

check <<- EOF
	00000000 f  o  o  sp b  a  r  \n
	00000008 b  a  z  sp C3 A9 \n
EOF

# null-char
printf "foo\0bar" | init -0

check <<- EOF
	f  o  o  \0
	b  a  r 
EOF
