#!/bin/sh -eu
# shellcheck enable=

cd "$(dirname "$0")"

assertequals () {
	if [ "$1" != "$2" ]
	then
		printf "Expected: %s\nGot: %s\n" "$1" "$2"
		exit 1
	fi
}

assertequals "9ef61f95" "$(printf foobar | ./crc.py --hex -4)"
assertequals "b025" "$(printf foobar | ./crc.py --hex -2)"

