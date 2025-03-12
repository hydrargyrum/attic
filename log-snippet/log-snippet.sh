#!/bin/sh -e
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

usage () {
	cat <<- EOF
	Usage: $0: [-C CTXLINES]

	Takes a compilation-log input on stdin (as output by gcc, pyflakes,
	etc.) and output snippets from files mentioned in the log.

	Expected input lines format:

	    PATH/TO/FILE:LINENUMBER:ANYTHING...

	For each input line, output the content of PATH/TO/FILE
	at line LINENUMBER with a context of CTXLINES lines
	(by default: 5).
	EOF
}


# sysexits
EX_USAGE=64

context=5
while getopts C: name
do
	case $name in
	C)
		context=$OPTARG;;
	?)
		usage >&2
		exit $EX_USAGE;;
	esac
done
shift $((OPTIND - 1))

if ! [ "$context" -ge 0 ]
then
	usage >&2
	exit $EX_USAGE
fi

index=0
while read -r result
do
	file=${result%%:*}
	wofile=${result#*:}
	lineno=${wofile%%:*}

	if [ $index -gt 0 ]
	then
		printf "%s\n" "--"
	fi

	awk "NR >= $((lineno - context)) && NR <= $((lineno + context)) {
		if (NR == $lineno) { sep=\":\" }
		else { sep=\"-\" }
		printf(\"%s%s%s%s%s\n\", FILENAME, sep, NR, sep, \$0)
		#print
	}" "$file"

	index=$((index + 1))
done
