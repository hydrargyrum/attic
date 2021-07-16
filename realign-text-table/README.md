# Name

`realign-text-table` - redraws malformed ASCII-drawn tables

# Synopsis

	realign-text-table [--markdown] [FILE]

# Description

`realign-text-table` reads stdin or argument file. stdin should contain ASCII
tables. `realign-text-table` will print on stdout the same table but properly
aligned.

If `--markdown` is given, will output Gitlab/Github-flavored Markdown tables.

# Example

When given this table as stdin:

    +-----+-----+
    | foo | bar |
    +-----+-----+
    | a long cell | short |
    | x | longer cell ? |
    +--+--+

it will output a well-formed table:

    +-------------+---------------+
    |     foo     |      bar      |
    +-------------+---------------+
    | a long cell |     short     |
    |      x      | longer cell ? |
    +-------------+---------------+

# Dependencies

`realign-text-table` uses Python and PrettyTable.

# License

This is free software, distributed under the WTFPL 2.0.
