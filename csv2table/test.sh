#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp csv2table.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./csv2table.py "$@" > "$got"
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
	+----------+--------+
	| name     | color  |
	+----------+--------+
	| zucchini | green  |
	| tomato   | red    |
	| banana   | yellow |
	| orange   | orange |
	+----------+--------+
EOF

# markdown
init --header --markdown <<- EOF
	name,color
	zucchini,green
	tomato,red
	banana,yellow
	orange,orange
EOF

check <<- EOF
	| name     | color  |
	| :--------| :------|
	| zucchini | green  |
	| tomato   | red    |
	| banana   | yellow |
	| orange   | orange |
EOF

# html
init --header --html <<- EOF
	name,color
	zucchini,green
	tomato,red
	banana,yellow
	orange,orange
EOF

check <<- EOF
	<table>
	    <thead>
	        <tr>
	            <th>name</th>
	            <th>color</th>
	        </tr>
	    </thead>
	    <tbody>
	        <tr>
	            <td>zucchini</td>
	            <td>green</td>
	        </tr>
	        <tr>
	            <td>tomato</td>
	            <td>red</td>
	        </tr>
	        <tr>
	            <td>banana</td>
	            <td>yellow</td>
	        </tr>
	        <tr>
	            <td>orange</td>
	            <td>orange</td>
	        </tr>
	    </tbody>
	</table>
EOF
