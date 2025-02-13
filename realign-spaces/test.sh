#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

cd "$(dirname "$0")"

got=$(mktemp realign-spaces.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./realign-spaces.py "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	a bbb
	aaaa b
	c
EOF

check <<- EOF
	a    bbb
	aaaa b
	c
EOF

# shell split
init --shell-split <<- EOF
	'a b' bbb
	aaa b
	c
EOF

check <<- EOF
	'a b' bbb
	aaa   b
	c
EOF

# -i
cat > "$got" <<- EOF
	a bbb
	aaa b
	c
EOF
# set a weird mode to check umask does not affect it
chmod 623 "$got"
./realign-spaces.py -i "$got"

check <<- EOF
	a   bbb
	aaa b
	c
EOF
# check our mode was preserved
ls -l "$got" | grep -q rw--w--wx
