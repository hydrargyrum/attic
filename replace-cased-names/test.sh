#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

cd "$(dirname "$0")"

got=$(mktemp replace.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	cat > "$got"
	./replace-cased-names "$@" "$got"
}

check () {
	diff -u - "$got"
}


init foo_bar baz_qux_quxx <<- EOF
	this should not change
	but this: foo_bar should FOO_BAR change
	nope
	FooBar.fooBar(FOO_BAR, foo_bar, "foo-bar")
EOF

check <<- EOF
	this should not change
	but this: baz_qux_quxx should BAZ_QUX_QUXX change
	nope
	BazQuxQuxx.bazQuxQuxx(BAZ_QUX_QUXX, baz_qux_quxx, "baz-qux-quxx")
EOF

if echo | init FOO bar 2>/dev/null
then
	echo "should have failed with non snake_case argument" >&2
	exit 1
fi
