#!/bin/sh -eu

cd "$(dirname "$0")"

got=$(mktemp -t test.XXXXXX)
exp=$(mktemp -t test.XXXXXX || rm -f "$got")

trap 'rm -f "$got" "$exp"' EXIT


# basic BOM
printf "\357\273\277foobar\n" | ./no-utf8-bom > "$got"
printf "foobar\n" > "$exp"
diff "$got" "$exp"

# basic BOM (no newline at end of file)
printf "\357\273\277foobar" | ./no-utf8-bom > "$got"
printf "foobar" > "$exp"
diff "$got" "$exp"

# no-op (no BOM)
printf "foobar\n" | ./no-utf8-bom > "$got"
printf "foobar\n" > "$exp"
diff "$got" "$exp"

# no-op (BOM mid-file)
printf "foo\357\273\277bar\n" | ./no-utf8-bom > "$got"
printf "foo\357\273\277bar\n" > "$exp"
diff "$got" "$exp"

# no-op (BOM mid-file)
printf "foo\n\357\273\277bar\n" | ./no-utf8-bom > "$got"
printf "foo\n\357\273\277bar\n" > "$exp"
diff "$got" "$exp"
