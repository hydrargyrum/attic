#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp -d extract-json-archive.XXXXXX)
trap 'rm -rf "$got"' EXIT


init () {
	./extract-json-archive.py -o "$got" "$@" >/dev/null
}

check () {
	diff -u - "$got/$1"
}


# basic test
init <<- EOF
	[{"filename": "foo/hello.txt", "data": "SGVsbG8gd29ybGQhCg=="}]
EOF

check foo/hello.txt <<- EOF
	Hello world!
EOF

if echo '[{"filename": "/tmp/test.txt", "data": "SGVsbG8gd29ybGQhCg=="}]' | init 2>/dev/null
then
	echo should have failed >&2
	exit 1
fi
