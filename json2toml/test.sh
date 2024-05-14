#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp json2toml.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./json2toml "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init <<- EOF
	{"foo": "bar\nbar", "baz": {"qux": 42, "quux": [43]}}
EOF

check <<- EOF
	foo = "bar\nbar"

	[baz]
	qux = 42
	quux = [43]
EOF

# multiline string
init --multiline-strings <<- EOF
	{"foo": "bar\nbar\n"}
EOF

check <<- EOF
	foo = """bar
	bar
	"""
EOF
