#!/bin/sh -eu

cd "$(dirname "$0")"

die () {
	echo "$*" >&2
	exit 1
}

./nicest -p $$ > /dev/null

./nicest true

if ./nicest false
then
	die "false should have exited with error"
fi
