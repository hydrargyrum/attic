#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp sorted.XXXXXX)
trap 'rm "$got"' EXIT


init () {
    ./urlunquote "$@" > "$got"
}

check () {
    diff -u - "$got"
}


init https%3A//foo%40example.com%3A443/%3Bspecial%3Fkey%5B%5D%3Dvalue
echo "https://foo@example.com:443/;special?key[]=value" | check

init "foo%20/%20bar"
echo  "foo / bar" | check

init --plus "foo+%2F+bar"
echo  "foo / bar" | check
