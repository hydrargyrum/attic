#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp json2table.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./json2table "$@" > "$got"
}

check () {
	diff -u - "$got"
}

table1 () {
	echo '[{"name": "zucchini", "color": "green"}, {"name": "tomato", "color": "red"}, {"name": "banana", "color": "yellow"}, {"name": "orange", "color": "orange"}]'
}


# basic test
table1 | init

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

# markdown
table1 | init --markdown

check <<- EOF
	| name     | color  |
	| :--------| :------|
	| zucchini | green  |
	| tomato   | red    |
	| banana   | yellow |
	| orange   | orange |
EOF
