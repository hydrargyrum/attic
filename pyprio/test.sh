#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp pyprio.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./pyprio.py "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init "1+2"

check <<- EOF
	1 + 2
EOF

#
init "1+2*3+4"

check <<- EOF
	(1 + (2 * 3)) + 4
EOF

# lazy, just check it doesn't crash
init "foo(123, *[bar], kw=val, **{qux: quuux})"
