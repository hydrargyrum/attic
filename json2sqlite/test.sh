#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

TRUNC=
got=$(mktemp json2sqlite.XXXXXX)
csv=$(mktemp json2sqlite.XXXXXX)
trap 'rm "$got" "$csv"' EXIT

trunc () {
	: > "$got"
}

run () {
	[ -n "${TRUNC-}" ] && trunc
	./json2sqlite -d "$got" "$@"
}

check () {
	sqlite3 -csv "$got" -header "$@" > "$csv"
	diff -u - "$csv"
}

# basic test input as list[dict]
TRUNC=y run -f - -t test --create <<- EOF
	[{"col1": "1.1", "col2": "1.2"}, {"col1": "2.1", "col2": "2.2"}]
EOF

check "select * from test" <<- EOF
	col1,col2
	1.1,1.2
	2.1,2.2
EOF

# basic test input as list[dict] as arguments
TRUNC=y run -t test --create -j '[{"col1": "1.1", "col2": "1.2"}, {"col1": "2.1", "col2": "2.2"}]'

check "select * from test" <<- EOF
	col1,col2
	1.1,1.2
	2.1,2.2
EOF

# test input as dict (single entry)
TRUNC=y run -f - -t test --create <<- EOF
	{"col1": "1.1", "col2": "1.2"}
EOF

check "select * from test" <<- EOF
	col1,col2
	1.1,1.2
EOF

# test input as list[list]
trunc
sqlite3 "$got" "create table test(foo, bar)"
run -f - -t test --create <<- EOF
	[["1.1", "1.2"], ["2.1", "2.2"]]
EOF

check "select * from test" <<- EOF
	foo,bar
	1.1,1.2
	2.1,2.2
EOF

# test --update
TRUNC=y run -f - -t test --create <<- EOF
	[{"col1": "1.1", "col2": "1.2"}, {"col1": "2.1", "col2": "2.2"}]
EOF
run --file - --table test --update col1 <<- EOF
	[{"col1": "1.1", "col2": "new1"}, {"col1": "2.1", "col2": "new2"}]
EOF

check "select * from test" <<- EOF
	col1,col2
	1.1,new1
	2.1,new2
EOF
