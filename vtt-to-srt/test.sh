#!/bin/sh -eu
# SPDX-License-Identifier: WTFPL
# shellcheck enable=

cd "$(dirname "$0")"

got=$(mktemp vtt-to-srt.XXXXXX)
trap 'rm "$got"' EXIT

init () {
    ./vtt-to-srt - > "$got"
}

check () {
    diff -u - "$got"
}

init <<- EOF
	WEBVTT

	STYLE
	::cue(.bg_white) {
	 background-color: white;
	}

	00:00:07.160 --> 00:00:08.160 line:91% align:center
	foo bar

	00:00:08.800 --> 00:00:11.440 line:83% align:center
	baz qux
	grault
EOF

check <<- EOF
	1
	00:00:07.160 --> 00:00:08.160
	foo bar

	2
	00:00:08.800 --> 00:00:11.440
	baz qux
	grault
EOF

# ok the third one is stupid
