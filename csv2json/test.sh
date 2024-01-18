#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp csv2json.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./csv2json "$@" | python3 -m json.tool > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init --header <<- EOF
	name,color
	zucchini,green
	tomato,red
	banana,yellow
	orange,orange
EOF

check <<- EOF
	[
	    {
	        "name": "zucchini",
	        "color": "green"
	    },
	    {
	        "name": "tomato",
	        "color": "red"
	    },
	    {
	        "name": "banana",
	        "color": "yellow"
	    },
	    {
	        "name": "orange",
	        "color": "orange"
	    }
	]
EOF

