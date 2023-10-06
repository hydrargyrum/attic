#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./boxuni > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	+----------+--------+
	| name     | color  |
	+----------+--------+
	| zucchini | green  |
	| tomato   | red    |
	| banana   | yellow |
	| orange   | orange |
	+----------+--------+
EOF

check <<- EOF
	┌──────────┬────────┐
	│ name     │ color  │
	├──────────┼────────┤
	│ zucchini │ green  │
	│ tomato   │ red    │
	│ banana   │ yellow │
	│ orange   │ orange │
	└──────────┴────────┘
EOF
