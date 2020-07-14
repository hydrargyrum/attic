#!/bin/sh -e
# license: Do What The Fuck You Want To Public License version 2 [http://www.wtfpl.net/]

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

	currentcontext=-$context

	# change IFS to avoid field splitting on read lines
	# for example: don't let shell trim trailing whitespace from $line
	old="$IFS"
	IFS=

	sed -n "$((lineno - context)),$((lineno + context))p" "$file" | while read -r line
	do
		sep=-
		if [ "$currentcontext" -eq 0 ]
		then
			sep=:
		fi
		printf "%s%s%s%s%s\n" "$file" "$sep" "$((lineno + currentcontext))" "$sep" "$line"
		currentcontext=$((currentcontext + 1))
	done

	IFS="$old"

	index=$((index + 1))
done
