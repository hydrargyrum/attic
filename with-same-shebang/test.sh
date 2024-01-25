#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp shebang.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./with-same-shebang "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init ./with-same-shebang -c "echo foo"
check <<- EOF
	foo
EOF

# -n
init -n ./with-same-shebang -c "echo foo"
check <<- EOF
	/bin/sh -eu -c echo foo
EOF

# -n -c
init -n -c ./with-same-shebang -c "echo foo"
check <<- EOF
	/bin/sh -c echo foo
EOF
