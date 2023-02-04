#!/bin/sh -eu

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./group-lines "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test (sort groups, keep lines order)
init "\b\d{4}-\d{2}\b" <<- EOF
	foo 2022-08-20
	baz 2022-09-01
	bar 2022-08-19
	qux 2021-08-20
EOF

check <<- EOF
	2021-08:
	qux 2021-08-20
	2022-08:
	foo 2022-08-20
	bar 2022-08-19
	2022-09:
	baz 2022-09-01
EOF

# capture groups
init " (\d{4})-(\d{2})-\d{2}" <<- EOF
	foo 2022-08-20
	baz 2022-09-01
	bar 2022-08-19
	qux 2021-08-20
EOF

check <<- EOF
	202108:
	qux 2021-08-20
	202208:
	foo 2022-08-20
	bar 2022-08-19
	202209:
	baz 2022-09-01
EOF
