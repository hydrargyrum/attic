#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp yml2json.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./yml2json.py "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	foo:
	- bar
	- baz: bazbaz
	  qux: true
EOF

check <<- EOF
	{"foo": ["bar", {"baz": "bazbaz", "qux": true}]}
EOF

# multi-document
init -a <<- EOF
	---
	foo: 42
	---
	foo: 43
EOF

check <<- EOF
	[{"foo": 42}, {"foo": 43}]
EOF
