#!/bin/sh -e

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap "rm '$got'" EXIT


init () {
	./sort-with-numbers "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# test string
LANG=C init <<- EOF
	foo
	bar
EOF

check <<- EOF
	bar
	foo
EOF


# basic test numbers
LANG=C init <<- EOF
	1
	10
	2
EOF

check <<- EOF
	1
	2
	10
EOF


# test multiple numbers
LANG=C init <<- EOF
	1
	10 10
	10 2
	2
EOF

check <<- EOF
	1
	2
	10 2
	10 10
EOF


# test numbers with strings
LANG=C init <<- EOF
	1
	10
	2
EOF

check <<- EOF
	1
	2
	10
EOF


# test strings with numbers
LANG=C init <<- EOF
	foo 1
	foo 10
	foo 2
	bar 3
EOF

check <<- EOF
	bar 3
	foo 1
	foo 2
	foo 10
EOF


# test mix
LANG=C init <<- EOF
	foo 1 foo
	foo 10 foo
	foo 10 bar
	foo 2 bar
	bar 3
EOF

check <<- EOF
	bar 3
	foo 1 foo
	foo 2 bar
	foo 10 bar
	foo 10 foo
EOF


# test collation (C)
LANG=C init <<- EOF
	z
	a
	é
EOF

check <<- EOF
	a
	z
	é
EOF


# test collation (fr_FR)
LANG=fr_FR.UTF-8 init <<- EOF
	z
	a
	é
EOF

check <<- EOF
	a
	é
	z
EOF

# NUL separator
printf "foo\000qux\000baz\000bar\000" | init -z
printf "bar\000baz\000foo\000qux\000" | check
