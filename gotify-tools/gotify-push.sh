#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL

die () {
	printf "error: %s\n" "$@" >&2
	exit 1
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
			cat >&2 <<-EOF
				usage: $0 [-u URL] [-k TOKEN] [-K TOKENFILE] [-t TITLE] [-p PRIORITY] MESSAGE

				\$GOTIFY_URL can be used instead of -u
				\$GOTIFY_TOKEN can be used instead of -k
			EOF
			exit 64
			;;
	esac
done
shift $(( $OPTIND - 1 ))

if [ -z "${GOTIFY_URL:-}" ]
then
	die 'missing $GOTIFY_URL or -u URL'
fi

if [ -z "${GOTIFY_TOKEN:-}" ]
then
	die 'missing $GOTIFY_TOKEN or -t TOKEN or -T TOKENFILE'
fi

if ! PRIORITY=$(printf %d "$PRIORITY" 2>/dev/null)
then
	die 'bad -p PRIORITY number'
fi

message=$(printf %s "$*" | jsonstr)
TITLE=$(printf %s "$TITLE" | jsonstr)

curl \
	-s -S -f \
	-H 'Content-Type: application/json' \
	-H "X-Gotify-Key: $GOTIFY_TOKEN" \
	-d "{\"message\": \"$message\", \"title\": \"${TITLE}\", \"priority\": ${PRIORITY}}" \
	"${GOTIFY_URL%/}/message"
