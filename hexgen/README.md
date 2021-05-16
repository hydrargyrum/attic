# hexgen

Generate bytes from ASCII hexadecimal dump.

# Synopsis

	hexgen

# Description

`hexgen` reads hexadecimal numbers on stdin and writes bytes with values
corresponding to the numbers.

Whitespace (spaces, tabs, newlines) are simply ignored when read. Any other
character that is not a hex digit will quit `hexgen` with an error.

# Examples

Running

	echo "4865 6c6c 6f20 776f 726c 64 21 0a" | hexgen

will output `Hello world!`

# See also

`hd(1)` and `xxd(1)`
