#!/bin/sh -eu
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./ini2json "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init sample.ini
check < sample.json
