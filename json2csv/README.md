# json2csv

Convert a JSON to CSV.

Accept an array of objects:

	[
	  {"foo": 1, "bar": 4},
	  {"foo": 2, "bar": 5},
	  {"bar": 6, "foo": 3}
	]

Or an object with array values:

	{
	  "foo": [1, 2, 3],
	  "bar": [4, 5, 6]
	}

Or [JSON lines](https://jsonlines.org/):

	{"foo": 1, "bar": 4}
	{"foo": 2, "bar": 5}
	{"bar": 6, "foo": 3}

Or another format of JSON lines:

	["foo", "bar"]
	[1, 4]
	[2, 5]
	[3, 6]

Both inputs will be converted to this CSV:

	foo,bar
	1,4
	2,5
	3,6

# License

This is free software, distributed under the WTFPL 2.0.
