#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp itertools.XXXXXX)
trap 'rm "$got"' EXIT


process () {
	cat
}

init () {
	./itertools.py "$@" | process > "$got"
}

check () {
	diff -u - "$got"
}


# plain permutations
init --out-plain --permutations foo bar baz

check <<- EOF
	foo bar baz
	foo baz bar
	bar foo baz
	bar baz foo
	baz foo bar
	baz bar foo
EOF

# CSV combinations
process () {
	sed 's/\r//'
}

init --out-csv --combinations 2 foo bar baz

check <<- EOF
	col_0,col_1
	foo,bar
	foo,baz
	bar,baz
EOF

# JSON combinations
process () {
	python3 -m json.tool --compact
}

init --out-json --combinations 2 foo bar baz

check <<- EOF
	[["foo","bar"],["foo","baz"],["bar","baz"]]
EOF
