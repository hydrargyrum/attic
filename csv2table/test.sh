#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp csv2table.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./csv2table.py "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init --header <<- EOF
	name,color
	zucchini,green
	tomato,red
	banana,yellow
	orange,orange
EOF

check <<- EOF
	+----------+--------+
	| name     | color  |
	+----------+--------+
	| zucchini | green  |
	| tomato   | red    |
	| banana   | yellow |
	| orange   | orange |
	+----------+--------+
EOF

