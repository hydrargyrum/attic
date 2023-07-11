#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


indent () {
	python3 -m json.tool --indent 2
}

init () {
	./flatten-json.py "$@" | indent > "$got"
}

check () {
	indent | diff -u - "$got"
}

# flatten
init < example-normal.json
check < example-flat.json

# --expand
init --expand < example-flat.json
check < example-normal.json

# --separator, flatten
# XXX unfortunately there are slashes in json value so a basic sed isn't enough
init --separator : < example-normal.json
sed -e s@/@:@g -e "s@<:@</@" < example-flat.json | check

# --separator, --expand
sed -e s@/@:@g -e "s@<:@</@" < example-normal.json | init --expand --separator :
check < example-normal.json

# --indent
init --indent < example-normal.json
cat < example-flat.json | diff -u - "$got"

# --no-lists
init --expand --no-lists < example-flat.json
check < example-normal-no-lists.json 

