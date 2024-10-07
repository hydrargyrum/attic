#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp htmlesc.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./htmlesc > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	<b>foo</b>
EOF

check <<- EOF
	&lt;b&gt;foo&lt;/b&gt;
EOF
