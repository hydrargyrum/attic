#!/bin/awk -f
# SPDX-License-Identifier: WTFPL

BEGIN {
	if (OFS == " ") {
		OFS = ","
	}
	for (i = 1; i < ARGC; i++) {
		if (i > 1) {
			printf("%s", OFS)
		}
		gsub("\"", "\"\"", ARGV[i])
		printf("\"%s\"", ARGV[i])
	}
	print ""
	exit
}
