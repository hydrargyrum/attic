#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp favail.XXXXXX)
trap 'rm "$got"' EXIT


init () {
	./first-avail-command "$@" > "$got"
}

check () {
	diff -u - "$got"
}

error () {
	printf "%s\n" "$*"
	exit 1
}

# extra args
init sh -- -c "echo foo"
echo foo | check

# extra args 2
init "sh -c" -- "echo foo"
echo foo | check

# ignore non-existing command
init DOESNOTEXIST sh -- -c "echo foo"
echo foo | check

# run "true" first
init true false --

# run "false" first, propagate code
if init false true --
then
	error "should have returned 1"
fi

# missing "--"
if init sh 2>/dev/null
then
	error "should have failed because of missing --"
fi

# only non-existing commands
if init DOESNOTEXIST -- 2>/dev/null
then
	error "should have failed because no command exists"
fi
