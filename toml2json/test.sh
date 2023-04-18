#!/bin/sh -eu

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./toml2json "$@" > "$got"
}

check () {
	diff -u - "$got"
}


# basic test
init sample.toml
check < sample.json
