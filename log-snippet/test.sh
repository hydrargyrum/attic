#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

snipdir=$(mktemp -d logsnip.XXXXXX)
got=$snipdir/got.txt

# line 4 has intentional trailing space
cat > "$snipdir/data1.txt" <<- EOF
	lorem ipsum
	dolor
	sit amet
	consectuetur 
	 adipiscing
	elit.
EOF
trap 'rm -rf "$snipdir"' EXIT

init () {
	./log-snippet.sh "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init -C 1 <<- EOF
	$snipdir/data1.txt:4:whatever
EOF

check <<- EOF
	$snipdir/data1.txt-3-sit amet
	$snipdir/data1.txt:4:consectuetur 
	$snipdir/data1.txt-5- adipiscing
EOF

