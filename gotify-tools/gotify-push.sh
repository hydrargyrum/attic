#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

usage () {
	cat >&2 <<-EOF
		usage: $0 [-u URL] [-k TOKEN] [-K TOKENFILE] [-t TITLE] [-p PRIORITY] MESSAGE

		\$GOTIFY_URL can be used instead of -u
		\$GOTIFY_TOKEN can be used instead of -k
	EOF
	exit 64
}

jsonstr () {
	# crude but sufficient?
	# will probably chomp trailing newlines
	# will not escape control chars (except newlines)
	sed -n '
		s/\\/\\\\/g
		s/"/\\"/g

		1 h
		2,$ H
		$ {
			x
			s/\n/\\n/g
			p
		}
	'
}

PRIORITY=1
TITLE=

while getopts p:u:k:K:t: f
do
	case $f in
		p)
			PRIORITY=$OPTARG
			;;
		u)
			GOTIFY_URL=$OPTARG
			;;
		k)
			GOTIFY_TOKEN=$OPTARG
			;;
		K)
			GOTIFY_TOKEN=$(cat "$OPTARG")
			;;
		t)
			TITLE=$OPTARG
			;;
		\?)
			usage
			;;
	esac
done
shift $(( $OPTIND - 1 ))

if [ -z "${GOTIFY_URL:-}" ]
then
	printf 'error: missing $GOTIFY_URL or -u URL\n\n' >&2
	usage
fi

if [ -z "${GOTIFY_TOKEN:-}" ]
then
	printf 'error: missing $GOTIFY_TOKEN or -t TOKEN or -T TOKENFILE\n\n' >&2
	usage
fi

if ! PRIORITY=$(printf %d "$PRIORITY" 2>/dev/null)
then
	printf 'error: bad -p PRIORITY number\n\n' >&2
	usage
fi

if [ -z "$*" ]
then
	usage
fi

message=$(printf %s "$*" | jsonstr)
TITLE=$(printf %s "$TITLE" | jsonstr)

curl \
	-s -S -f \
	-H 'Content-Type: application/json' \
	-H "X-Gotify-Key: $GOTIFY_TOKEN" \
	-d "{\"message\": \"$message\", \"title\": \"${TITLE}\", \"priority\": ${PRIORITY}}" \
	"${GOTIFY_URL%/}/message"
