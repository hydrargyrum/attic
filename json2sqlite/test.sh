#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp json2sqlite.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./json2sqlite "$@" -d "$got"
}

check () {
	test -f "$got"
}


# basic test
init -f - -t test --create <<- EOF
	[{"col1": "1,1", "col2": "2,1"}, {"col1": "1,2", "col2": "2,2"}]
EOF
