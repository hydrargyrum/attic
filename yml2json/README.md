# yml2json

Convert YAML to JSON.

# Synopsis

	yml2json [FILE]

# Description

`yml2json` reads stdin or FILE (if given) input YAML and prints equivalent
JSON to stdout.

# Examples

Running

	yml2json << EOF
	- foo
	- bar: 1
	  qux: 2
	- other: yes
	EOF

will output

	["foo",{"bar":1,"qux":2},{"other":true}]

# License

This is free software, distributed under the WTFPL 2.0.
