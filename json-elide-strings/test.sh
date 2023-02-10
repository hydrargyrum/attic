#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


indent () {
	python3 -m json.tool --indent 2
}

init () {
	./json-elide-strings.py "$@" | indent > "$got"
}

check () {
	indent | diff -u - "$got"
}

# basic structure
init -l6 <<- EOF
	["foooooooooooooooooooooooooo", "bar", "bazqux", "bazbaz1"]
EOF
check <<- EOF
	["foo...", "bar", "bazqux", "baz..."]
EOF

# nested structure, and key unmodified
init -l6 <<- EOF
	{"fooooooooooooo": ["bar", {"baz": "quuuuuuuuuuuuuuux"}]}
EOF
check <<- EOF
	{"fooooooooooooo": ["bar", {"baz": "quu..."}]}
EOF

# nested structure, and key modified
init -l6 --keys <<- EOF
	{"fooooooooooooo": ["bar", {"baz": "quuuuuuuuuuuuuuux"}]}
EOF
check <<- EOF
	{"foo...": ["bar", {"baz": "quu..."}]}
EOF

# nested structure, and key unmodified, and change suffix
init -l6 --keys --suffix=@ <<- EOF
	{"fooooooooooooo": ["bar", {"baz": "quuuuuuuuuuuuuuux"}]}
EOF
check <<- EOF
	{"foooo@": ["bar", {"baz": "quuuu@"}]}
EOF
